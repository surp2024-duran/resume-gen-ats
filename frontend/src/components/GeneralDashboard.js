// frontend/src/components/GeneralDashboard.js
import React, { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import { Line, Bar, Pie, Scatter } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'uikit/dist/css/uikit.min.css';
import 'uikit/dist/js/uikit.min.js';

ChartJS.register(...registerables);

const GeneralDashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [documentCount, setDocumentCount] = useState(0);
  const [collectionCount, setCollectionCount] = useState(0);
  const [percentage, setPercentage] = useState(0);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    onResize: null,
  };

  useEffect(() => {
    const fetchDataFromAPI = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/data`);
        const collections = response.data.collections.filter((collection) => collection !== 'Resumes');
        setCollectionCount(collections.length);

        let totalDocs = 0;
        const allDocuments = await Promise.all(
          collections.map(async (collection, index) => {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/data/${collection}`);
            totalDocs += res.data.length;
            setDocumentCount(totalDocs);
            setPercentage(Math.floor(((index + 1) / collections.length) * 100));
            return res.data;
          })
        );

        setData(allDocuments.flat());
      } catch (error) {
        console.error('Error fetching general dashboard data', error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchDataFromAPI();
  }, []);

  const stats = useMemo(() => {
    if (!data.length) return null;

    const labeledData = data.filter(doc => doc.score !== undefined);
    const scores = labeledData.map((doc) => doc.score);
    const avgScore = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : 'N/A';
    const stdDev = scores.length ? Math.sqrt(scores.reduce((sq, n) => sq + Math.pow(n - avgScore, 2), 0) / scores.length) : 'N/A';
    const median = scores.length ? scores.sort((a, b) => a - b)[Math.floor(scores.length / 2)] : 'N/A';
    const minScore = scores.length ? Math.min(...scores) : 'N/A';
    const maxScore = scores.length ? Math.max(...scores) : 'N/A';

    const labelers = labeledData.map((doc) => doc.didBy);
    const uniqueLabelers = [...new Set(labelers)];
    const labelerProductivity = uniqueLabelers
      .map((labeler) => ({
        name: labeler,
        count: labelers.filter((l) => l === labeler).length,
      }))
      .sort((a, b) => b.count - a.count);

    const truthfulnessCount = labeledData.filter((doc) => doc.truthfulness).length;
    const truthfulnessPercentage = labeledData.length ? (truthfulnessCount / labeledData.length) * 100 : 'N/A';

    const dateRange = {
      start: new Date(Math.min(...data.filter(doc => doc.created_at).map((doc) => new Date(doc.created_at)))),
      end: new Date(Math.max(...data.filter(doc => doc.created_at).map((doc) => new Date(doc.created_at)))),
    };

    return {
      avgScore,
      stdDev,
      median,
      minScore,
      maxScore,
      labelerProductivity,
      truthfulnessCount,
      truthfulnessPercentage,
      dateRange,
      labeledCount: labeledData.length,
      totalCount: data.length,
    };
  }, [data]);

  if (loading) {
    return (
      <div className="uk-flex uk-flex-center uk-flex-middle uk-height-viewport">
        <div className="uk-text-center">
          <div uk-spinner="ratio: 3"></div>
          <p className="uk-margin-top">Fetching documents from {collectionCount} collections...</p>
          <p>{percentage}% completed</p>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className="uk-alert-danger" uk-alert>Error fetching data: {error.message}</div>;
  }

  if (!data.length || !stats) {
    return <div className="uk-alert-warning" uk-alert>No data available</div>;
  }

  const timeSeriesData = data.reduce((acc, doc) => {
    if (doc.created_at && doc.score !== undefined) {
      const date = new Date(doc.created_at).toLocaleDateString();
      if (!acc[date]) acc[date] = { score: 0, count: 0 };
      acc[date].score += doc.score;
      acc[date].count += 1;
    }
    return acc;
  }, {});

  const chartData = {
    timeSeries: {
      labels: Object.keys(timeSeriesData),
      datasets: [
        {
          label: 'Average Score',
          data: Object.values(timeSeriesData).map((d) => d.score / d.count),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
        {
          label: 'Document Count',
          data: Object.values(timeSeriesData).map((d) => d.count),
          borderColor: 'rgb(255, 99, 132)',
          tension: 0.1,
        },
      ],
    },
    labelerProductivity: {
      labels: stats.labelerProductivity.map((l) => l.name),
      datasets: [
        {
          label: 'Documents Labeled',
          data: stats.labelerProductivity.map((l) => l.count),
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
        },
      ],
    },
    truthfulness: {
      labels: ['Truthful', 'Not Truthful', 'Unlabeled'],
      datasets: [
        {
          data: [
            stats.truthfulnessCount, 
            stats.labeledCount - stats.truthfulnessCount,
            stats.totalCount - stats.labeledCount
          ],
          backgroundColor: ['rgba(75, 192, 192, 0.5)', 'rgba(255, 99, 132, 0.5)', 'rgba(200, 200, 200, 0.5)'],
        },
      ],
    },
    scoreDistribution: {
      labels: ['0-20', '21-40', '41-60', '61-80', '81-100', 'Unlabeled'],
      datasets: [
        {
          label: 'Score Distribution',
          data: [
            data.filter((d) => d.score !== undefined && d.score <= 20).length,
            data.filter((d) => d.score !== undefined && d.score > 20 && d.score <= 40).length,
            data.filter((d) => d.score !== undefined && d.score > 40 && d.score <= 60).length,
            data.filter((d) => d.score !== undefined && d.score > 60 && d.score <= 80).length,
            data.filter((d) => d.score !== undefined && d.score > 80).length,
            data.filter((d) => d.score === undefined).length,
          ],
          backgroundColor: 'rgba(153, 102, 255, 0.5)',
        },
      ],
    },
    scatterPlot: {
      datasets: [
        {
          label: 'Score vs Document Length',
          data: data.filter(d => d.score !== undefined && d.resume_text).map((d) => ({ x: d.resume_text.length, y: d.score })),
          backgroundColor: 'rgba(255, 206, 86, 0.5)',
        },
      ],
    },
  };

  return (
    <div className="uk-container uk-container-expand uk-padding">
      <div className="uk-grid uk-grid-medium uk-child-width-1-2@s uk-child-width-1-4@m uk-margin-medium-bottom" data-uk-grid>
        <div>
          <div className="uk-card uk-card-default uk-card-body">
            <h3 className="uk-card-title">Total Documents</h3>
            <p className="uk-text-large">{stats.totalCount}</p>
            <p className="uk-text-large">Document Count: {documentCount}</p> {/* Use documentCount here */}
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-primary uk-card-body">
            <h3 className="uk-card-title">Average Score</h3>
            <p className="uk-text-large">{typeof stats.avgScore === 'number' ? stats.avgScore.toFixed(2) : stats.avgScore}</p>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-secondary uk-card-body">
            <h3 className="uk-card-title">Truthfulness</h3>
            <p className="uk-text-large">{typeof stats.truthfulnessPercentage === 'number' ? stats.truthfulnessPercentage.toFixed(2) : stats.truthfulnessPercentage}%</p>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body">
            <h3 className="uk-card-title">Unique Labelers</h3>
            <p className="uk-text-large">{stats.labelerProductivity?.length || 'N/A'}</p>
          </div>
        </div>
      </div>

      <div className="uk-grid uk-grid-medium uk-child-width-1-2@m" data-uk-grid="masonry: true">
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Time Series Analysis</h3>
            <div style={{ height: '300px' }}>
              <Line data={chartData.timeSeries} options={chartOptions} />
            </div>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Labeler Productivity</h3>
            <div style={{ height: '300px' }}>
              <Bar data={chartData.labelerProductivity} options={{ ...chartOptions, indexAxis: 'y' }} />
            </div>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Truthfulness Distribution</h3>
            <div style={{ height: '300px' }}>
              <Pie data={chartData.truthfulness} options={chartOptions} />
            </div>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Score Distribution</h3>
            <div style={{ height: '300px' }}>
              <Bar data={chartData.scoreDistribution} options={chartOptions} />
            </div>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Score vs Document Length</h3>
            <div style={{ height: '300px' }}>
              <Scatter data={chartData.scatterPlot} options={chartOptions} />
            </div>
          </div>
        </div>
        <div>
          <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
            <h3 className="uk-card-title">Detailed Statistics</h3>
            <table className="uk-table uk-table-striped">
              <tbody>
                <tr>
                  <td>Median Score</td>
                  <td>{stats.median?.toFixed(2) || 'N/A'}</td>
                </tr>
                <tr>
                  <td>Standard Deviation</td>
                  <td>{stats.stdDev?.toFixed(2) || 'N/A'}</td>
                </tr>
                <tr>
                  <td>Min Score</td>
                  <td>{stats.minScore || 'N/A'}</td>
                </tr>
                <tr>
                  <td>Max Score</td>
                  <td>{stats.maxScore || 'N/A'}</td>
                </tr>
                <tr>
                  <td>Date Range</td>
                  <td>
                    {stats.dateRange?.start?.toLocaleDateString() || 'N/A'} -{' '}
                    {stats.dateRange?.end?.toLocaleDateString() || 'N/A'}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneralDashboard;
