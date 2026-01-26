import React, { useEffect } from 'react';
import { Clock } from 'lucide-react';
import { LogCard } from './LogCard';
import { PaginationControls } from '../../components/pagination/PaginationControls';
import { ItemsPerPageSelector } from '../../components/pagination/ItemsPerPageSelector';
import { usePagination } from '../../hooks/usePagination';
import type { TransitionLog } from '../../services/log.service';
import '../../styles/features/logs/LogTable.css';

interface LogTableProps {
  logs: TransitionLog[];
}

export const LogTable: React.FC<LogTableProps> = ({ logs }) => {
  const {
    currentPage,
    itemsPerPage,
    totalPages,
    startIndex,
    endIndex,
    paginatedItems: paginatedLogs,
    setItemsPerPage,
    goToPage,
    resetPage
  } = usePagination({ items: logs, initialItemsPerPage: 10 });

  useEffect(() => {
    resetPage();
  }, [logs.length, resetPage]);

  return (
    <div className="log-table-card">
      <div className="log-table-card-header">
        <h2 className="log-table-card-title">
          <Clock className="log-table-icon" />
          Transition History ({logs.length})
        </h2>
        {logs.length > 0 && (
          <div className="log-table-controls">
            <ItemsPerPageSelector
              value={itemsPerPage}
              onChange={setItemsPerPage}
              options={[5, 10, 20, 50]}
              id="logs-per-page"
            />
            <div className="pagination-info">
              {startIndex + 1}-{Math.min(endIndex, logs.length)} of {logs.length}
            </div>
          </div>
        )}
      </div>

      <div className="log-table-list">
        {logs.length === 0 ? (
          <div className="log-table-empty">
            No logs found
          </div>
        ) : (
          paginatedLogs.map((log) => (
            <LogCard key={log.id} log={log} />
          ))
        )}
      </div>

      {totalPages > 1 && (
        <PaginationControls
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={goToPage}
        />
      )}
    </div>
  );
};