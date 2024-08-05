// frontend/src/hooks/useFetch.js
import { useState, useEffect } from 'react';
import { fetchData } from '../services/api';

const useFetch = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDataFromAPI = async () => {
      try {
        const response = await fetchData();
        console.log('Fetched data:', response);  
        const filteredCollections = (response.collections || []).filter(collection => collection !== 'Resumes');
        setData(filteredCollections);
      } catch (error) {
        console.error('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDataFromAPI();
  }, []);

  return { data, loading };
};

export default useFetch;