// frontend/src/hooks/useFetchCollectionData.js
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL

const useFetchCollectionData = (collectionName) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (collectionName) {
      const fetchDataFromAPI = async () => {
        try {
          const response = await axios.get(`${API_URL}/data/${collectionName}`);
          setData(response.data);
        } catch (error) {
          console.error('Error fetching collection data', error);
          setError(error);
        } finally {
          setLoading(false);
        }
      };

      fetchDataFromAPI();
    }
  }, [collectionName]);

  return { data, loading, error };
};

export default useFetchCollectionData;
