// frontend/src/services/api.js
import axios from 'axios';

console.log('API URL:', process.env.REACT_APP_API_URL)

export const fetchData = async () => {
  try {
    const response = await axios.get(`${process.env.REACT_APP_API_URL}/data`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data', error);
    throw error;
  }
};
