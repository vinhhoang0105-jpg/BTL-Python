/**
 * Main layout wrapper — sidebar + header + content area.
 * Used for all authenticated pages.
 */

import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import './MainLayout.css';

export default function MainLayout() {
  return (
    <div className="main-layout">
      <Sidebar />
      <div className="main-content-wrapper">
        <Header />
        <main className="main-content animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
