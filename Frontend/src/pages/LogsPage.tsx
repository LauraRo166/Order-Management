import React, { useState } from 'react';
import { SearchInput } from '../components/common/SearchInput';
import { LogTable } from '../features/logs/LogTable';
import type { TransitionLog } from '../services/log.service';
import '../styles/pages/LogsPage.css';

interface LogsPageProps {
  logs: TransitionLog[];
}

export const LogsPage: React.FC<LogsPageProps> = ({ logs }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredLogs = logs
    .filter(log => log.orderId.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => new Date(b.transitionDate).getTime() - new Date(a.transitionDate).getTime());

  return (
    <div className="logs-page-container">
      <div className="logs-page-header">
        <h1 className="logs-page-title">Transition Logs</h1>
        <p className="logs-page-subtitle">
          Order state change history · {logs.length} total logs
        </p>
      </div>

      <div className="logs-page-search">
        <SearchInput
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search by Order ID..."
        />
      </div>

      <LogTable logs={filteredLogs} />
    </div>
  );
};
