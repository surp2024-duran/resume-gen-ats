const http = require('http');
const { MongoClient } = require('mongodb');
const url = require('url');
const dotenv = require('dotenv');
const path = require('path');
const cors = require('cors');

dotenv.config({ path: path.resolve(__dirname, '../.env') });

// Construct the MongoDB URI
const mongoUri = `mongodb+srv://${process.env.MONGO_USERNAME}:${process.env.MONGO_PASSWORD}@${process.env.MONGO_URI}/${process.env.MONGO_DB_NAME}?retryWrites=true&w=majority`;
let db;

MongoClient.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(client => {
    db = client.db();
    console.log('MongoDB connected');
  })
  .catch(err => console.error('Failed to connect to MongoDB', err));

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
  'Access-Control-Allow-Headers': 'X-Requested-With,content-type',
  'Access-Control-Allow-Credentials': true
};

const server = http.createServer((req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, corsHeaders);
    res.end();
    return;
  }

  if (req.method === 'GET') {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;

    if (path === '/api/collections') {
      db.listCollections().toArray()
        .then(collections => {
          // Extract and return only the collection names
          const collectionNames = collections.map(collection => ({ name: collection.name }));
          res.writeHead(200, { 'Content-Type': 'application/json', ...corsHeaders });
          res.end(JSON.stringify(collectionNames));
        })
        .catch(err => {
          res.writeHead(500, { 'Content-Type': 'application/json', ...corsHeaders });
          res.end(JSON.stringify({ error: err.message }));
        });
    } else if (path.startsWith('/api/collections/')) {
      const collectionName = path.split('/').pop();
      db.collection(collectionName).find({}).toArray()
        .then(data => {
          // Filter out items that do not have a score property
          const scoredItems = data.filter(item => item.hasOwnProperty('score'));

          const totalScores = scoredItems.reduce((total, item) => total + item.score, 0);
          const averageScore = scoredItems.length ? (totalScores / scoredItems.length) : 0;

          const response = {
            data: data,
            statistics: {
              averageScore: averageScore
            }
          };
          res.writeHead(200, { 'Content-Type': 'application/json', ...corsHeaders });
          res.end(JSON.stringify(response));
        })
        .catch(err => {
          res.writeHead(500, { 'Content-Type': 'application/json', ...corsHeaders });
          res.end(JSON.stringify({ error: err.message }));
        });
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json', ...corsHeaders });
      res.end(JSON.stringify({ error: 'Not Found' }));
    }
  } else {
    res.writeHead(405, { 'Content-Type': 'application/json', ...corsHeaders });
    res.end(JSON.stringify({ error: 'Method Not Allowed' }));
  }
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
