// frontend/src/App.js
import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Chart from './components/Chart';
import GeneralDashboard from './components/GeneralDashboard';
import 'uikit/dist/css/uikit.min.css';
import 'uikit/dist/js/uikit.min.js';

function App() {
  const [selectedCollection, setSelectedCollection] = useState(null);

  return (
    <div className="uk-offcanvas-content">
      <Header />
      <div className="flex">
        <Sidebar onSelectCollection={setSelectedCollection} />
        <main className="flex-1 p-4 ml-64">
          {selectedCollection ? (
            <Chart collectionName={selectedCollection} />
          ) : (
            <GeneralDashboard />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
