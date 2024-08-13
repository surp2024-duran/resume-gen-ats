// frontend/src/components/Chart.js
import React, { useMemo, useState } from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  BarElement,
  ArcElement,
} from 'chart.js';
import useFetchCollectionData from '../hooks/useFetchCollectionData';

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  BarElement,
  ArcElement
);

const Chart = ({ collectionName }) => {
  const { data: documents, loading, error } = useFetchCollectionData(collectionName);
  const [showFullPrompt, setShowFullPrompt] = useState(false);

  const stats = useMemo(() => {
    if (!documents.length) return null;

    const labeledDocs = documents.filter(doc => doc.score !== undefined);
    const scores = labeledDocs.map(doc => doc.score);
    const avgScore = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : 'N/A';
    const stdDev = scores.length ? Math.sqrt(scores.reduce((sq, n) => sq + Math.pow(n - avgScore, 2), 0) / scores.length) : 'N/A';
    const zScores = scores.length ? scores.map(score => (score - avgScore) / stdDev) : [];

    // const labelers = documents.filter(doc => doc.didBy).map(doc => doc.didBy);
    const labelerScores = {};
    labeledDocs.forEach(doc => {
      if (doc.didBy && doc.score !== undefined) {
        if (!labelerScores[doc.didBy]) {
          labelerScores[doc.didBy] = { totalScore: 0, count: 0 };
        }
        labelerScores[doc.didBy].totalScore += doc.score;
        labelerScores[doc.didBy].count += 1;
      }
    });

    let topLabeler = 'N/A';
    let topScore = -Infinity;
    for (const [labeler, data] of Object.entries(labelerScores)) {
      const avgScore = data.totalScore / data.count;
      if (avgScore > topScore) {
        topScore = avgScore;
        topLabeler = labeler;
      }
    }

    const truthfulnessCount = documents.filter(doc => doc.truthfulness).length;

    const fullPrompt = documents[0]?.prompt || 'No prompt available';
    const shortPrompt = fullPrompt.length > 400 ? fullPrompt.substring(0, 400) + '...' : fullPrompt;

    return { 
      avgScore, 
      stdDev, 
      zScores, 
      topLabeler, 
      truthfulnessCount, 
      fullPrompt, 
      shortPrompt,
      labeledCount: labeledDocs.length,
      totalCount: documents.length
    };
  }, [documents]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div uk-spinner="ratio: 3"></div>
      </div>
    );
  }

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }

  const labels = documents.filter(doc => doc.created_at).map(doc => new Date(doc.created_at).toLocaleDateString());
  const scores = documents.filter(doc => doc.score !== undefined).map(doc => doc.score);

  const lineData = {
    labels,
    datasets: [
      {
        label: `Scores Over Time`,
        data: scores,
        fill: false,
        backgroundColor: 'rgba(75,192,192,1)',
        borderColor: 'rgba(75,192,192,1)',
      },
      {
        label: 'Z-Scores',
        data: stats.zScores,
        fill: false,
        backgroundColor: 'rgba(255,99,132,1)',
        borderColor: 'rgba(255,99,132,1)',
      },
    ],
  };

  const barData = {
    labels: ['Truthful', 'Not Truthful', 'Unlabeled'],
    datasets: [
      {
        label: 'Truthfulness',
        data: [
          stats.truthfulnessCount, 
          stats.labeledCount - stats.truthfulnessCount,
          stats.totalCount - stats.labeledCount
        ],
        backgroundColor: ['rgba(75,192,192,0.6)', 'rgba(255,99,132,0.6)', 'rgba(200,200,200,0.6)'],
      },
    ],
  };

  const pieData = {
    labels: ['Truthful', 'Not Truthful', 'Unlabeled'],
    datasets: [
      {
        data: [
          stats.truthfulnessCount, 
          stats.labeledCount - stats.truthfulnessCount,
          stats.totalCount - stats.labeledCount
        ],
        backgroundColor: ['rgba(75,192,192,0.6)', 'rgba(255,99,132,0.6)', 'rgba(200,200,200,0.6)'],
      },
    ],
  };

  return (
    <div className="uk-grid uk-grid-match" uk-grid>
      <div className="uk-width-1-1">
        <div className="uk-card uk-card-default uk-card-body">
          <h3 className="uk-card-title">Statistics for {collectionName}</h3>
          <p>Average Score: {typeof stats.avgScore === 'number' ? stats.avgScore.toFixed(2) : stats.avgScore}</p>
          <p>Top Scorer: {stats.topLabeler}</p>
          <p>Labeled Entries: {stats.labeledCount} / {stats.totalCount}</p>
          <p>Truthful Entries: {stats.truthfulnessCount} / {stats.labeledCount} (of labeled entries)</p>
          <p>
            Prompt: {showFullPrompt ? stats.fullPrompt : stats.shortPrompt}
            {stats.fullPrompt.length > 400 && (
             <div>
             <button 
               className="uk-button uk-button-link block mt-4" 
               onClick={() => setShowFullPrompt(!showFullPrompt)}
             >
               {showFullPrompt ? 'Show Less' : 'Show More'}
             </button>
           </div>
            )}
          </p>
        </div>
      </div>
      <div className="uk-width-1-1 uk-margin">
  <div className="uk-card uk-card-default uk-card-body">
    <h3 className="uk-card-title">Scores and Z-Scores Over Time</h3>
    <Line data={lineData} />
  </div>
</div>
<div className="uk-width-1-2@m uk-margin">
  <div className="uk-card uk-card-default uk-card-body">
    <h3 className="uk-card-title">Truthfulness Distribution</h3>
    <Bar data={barData} />
  </div>
</div>
<div className="uk-width-1-2@m uk-margin">
  <div className="uk-card uk-card-default uk-card-body">
    <h3 className="uk-card-title">Truthfulness Pie Chart</h3>
    <Pie data={pieData} />
  </div>
</div>

    </div>
  );
};

export default Chart;