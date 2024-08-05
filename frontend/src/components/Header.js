// frontend/src/components/Header.js
import React from 'react';

const Header = () => {
  return (
    <header>
      <nav className="uk-navbar-container uk-navbar-transparent uk-light uk-width-1-1" uk-navbar="true" style={{ backgroundColor: 'white' }}>
        <div className="uk-container">
          <div className="uk-navbar-left">
            <ul className="uk-navbar-nav">
              {/* <li className="uk-active"><a href="/" style={{ color: 'black' }}>Dashboard</a></li>
              <li><a href="/analytics" style={{ color: 'black' }}>Analytics</a></li>
              <li><a href="/reports" style={{ color: 'black' }}>Reports</a></li> */}
            </ul>
          </div>
          <div className="uk-navbar-right">
            <ul className="uk-navbar-nav uk-navbar-nav-right-icons">
              {/* <li><a href="#" uk-icon="bell"></a></li> */}
              <li>
                {/* <a href="#"><span uk-icon="user"></span></a> */}
                <div className="uk-navbar-dropdown">
                  <ul className="uk-nav uk-navbar-dropdown-nav">
                    <li><a href="/profile" style={{ color: 'black' }}>Profile</a></li>
                    <li><a href="/settings" style={{ color: 'black' }}>Settings</a></li>
                    <li><a href="/logout" style={{ color: 'black' }}>Logout</a></li>
                  </ul>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;
