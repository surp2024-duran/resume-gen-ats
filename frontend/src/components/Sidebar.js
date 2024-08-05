// frontend/src/components/Sidebar.js
import React, { useState } from 'react';
import useFetch from '../hooks/useFetch';
import 'uikit/dist/css/uikit.min.css';
import 'uikit/dist/js/uikit.min.js';

const Sidebar = ({ onSelectCollection }) => {
  const { data: collections, loading } = useFetch();
  const [selectedCollection, setSelectedCollection] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const handleCollectionClick = (collection) => {
    setSelectedCollection(collection);
    onSelectCollection(collection);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div uk-spinner="ratio: 3"></div>
      </div>
    );
  }

  const filteredCollections = collections
    .filter(collection => collection !== 'Resumes')
    .sort((a, b) => a.localeCompare(b))
    .filter((collection) => collection.toLowerCase().includes(searchTerm.toLowerCase()));


  return (
    <aside className="custom-sidebar fixed top-0 left-0 bg-white border-r border-gray-200 p-4 w-64 h-screen">
      <ul className="uk-nav uk-nav-default">
        <li className="text-lg font-bold mb-2">resume-gen-ats</li>
        <li className="text-base font-light mb-2 text-gray-600">SURP 2024</li>
        <li className="text-base font-light mb-2 text-gray-600">With Dr. Kirk Duran</li>
        <li className="uk-nav-divider my-4"></li>
        <li className={`uk-active ${!selectedCollection ? 'active' : ''}`}>
          <a href="/" className="flex items-center space-x-2" onClick={() => handleCollectionClick(null)}>
            <span uk-icon="icon: home"></span> <span>Home</span>
          </a>
        </li>
        <li className="uk-nav-header text-lg font-bold mt-4 mb-2">Collections</li>
        <li>
          <input
            type="text"
            className="uk-input uk-margin-small-bottom"
            placeholder="Search collections"
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </li>
        {filteredCollections.map((collection) => (
          <li key={collection} className={selectedCollection === collection ? 'active' : ''}>
            <a href={`#${collection}`} className="flex items-center space-x-2" onClick={() => handleCollectionClick(collection)}>
              <span uk-icon="icon: folder"></span> <span>{collection}</span>
            </a>
          </li>
        ))}
        <li className="uk-nav-divider my-4"></li>
        <li>
          <a href="/settings" className="flex items-center space-x-2">
            <span uk-icon="icon: cog"></span> <span>Settings</span>
          </a>
        </li>
        <li>
          <a href="/help" className="flex items-center space-x-2">
            <span uk-icon="icon: question"></span> <span>Help</span>
          </a>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
