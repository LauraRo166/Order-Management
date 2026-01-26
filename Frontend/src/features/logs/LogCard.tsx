import React from 'react';
import { Badge } from '../../components/common/Badge';
import type { TransitionLog } from '../../services/log.service';
import '../../styles/features/logs/LogCard.css';

interface LogCardProps {
  log: TransitionLog;
}

export const LogCard: React.FC<LogCardProps> = ({ log }) => {
  return (
    <div className="log-card">
      <div className="log-card-header">
        <div>
          <p className="log-card-order-id">{log.orderId}</p>
          <p className="log-card-timestamp">
            {new Date(log.transitionDate).toLocaleString()}
          </p>
        </div>
        <Badge state={log.newState} />
      </div>

      <div className="log-card-transition">
        {log.previousState && (
          <>
            <Badge state={log.previousState} />
            <span className="log-card-arrow">→</span>
          </>
        )}
        <Badge state={log.newState} />
      </div>

      <p className="log-card-action">Action: {log.actionTaken}</p>
    </div>
  );
};
