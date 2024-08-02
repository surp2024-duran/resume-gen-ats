import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [collections, setCollections] = useState([]);
    const [selectedCollection, setSelectedCollection] = useState(null);
    const [data, setData] = useState([]);
    const [statistics, setStatistics] = useState(null);

    useEffect(() => {
        console.log("Fetching collections...");
        axios.get(`${process.env.REACT_APP_API_URL}/collections`)
            .then(response => {
                console.log("Collections fetched:", response.data);
                setCollections(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the collections!', error);
            });
    }, []);

    const fetchCollectionData = (name) => {
        console.log(`Fetching data for collection: ${name}`);
        setData([]); // Clear previous data before fetching new data
        setStatistics(null); // Clear previous statistics
        axios.get(`${process.env.REACT_APP_API_URL}/collections/${name}`)
            .then(response => {
                console.log(`Data for collection ${name}:`, response.data);
                setSelectedCollection(name);
                setData(response.data.data);
                setStatistics(response.data.statistics);
            })
            .catch(error => {
                console.error(`There was an error fetching the data for collection ${name}!`, error);
            });
    };

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="collections">
                <h2>Collections</h2>
                <ul>
                    {collections.map(collection => (
                        <li key={collection.name}>
                            <button onClick={() => fetchCollectionData(collection.name)}>
                                {collection.name}
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
            
            <div className="statistics">
                <h2>Statistics</h2>
                {statistics ? (
                    <div>
                        <p>Average Score: {statistics.averageScore}</p>
                        <pre>{JSON.stringify(statistics, null, 2)}</pre>
                    </div>
                ) : (
                    <p>No statistics available or loading...</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
