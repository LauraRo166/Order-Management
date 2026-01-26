import React from 'react';
import { Package, FileText, LucideIcon } from 'lucide-react';
import '../../styles/components/Header.css';

interface HeaderProps {
  currentView: 'orders' | 'logs';
  onViewChange: (view: 'orders' | 'logs') => void;
}

interface NavItem {
  view: 'orders' | 'logs';
  icon: LucideIcon;
  label: string;
}

const NAV_ITEMS: NavItem[] = [
  { view: 'orders', icon: Package, label: 'Orders' },
  { view: 'logs', icon: FileText, label: 'Logs' }
];

export const Header: React.FC<HeaderProps> = ({ currentView, onViewChange }) => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-brand">
          <Package className="header-icon" />
          <h1 className="header-title">Order Management</h1>
        </div>
        <nav className="header-nav">
          {NAV_ITEMS.map(({ view, icon: Icon, label }) => (
            <button
              key={view}
              onClick={() => onViewChange(view)}
              className={`nav-button ${currentView === view ? 'active' : ''}`}
            >
              <Icon className="nav-icon" />
              {label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};