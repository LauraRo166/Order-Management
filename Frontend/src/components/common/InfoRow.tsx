import React from 'react';
import '../../styles/components/InfoRow.css';

interface InfoRowProps {
  label: string;
  value: string | React.ReactNode;
}

export const InfoRow: React.FC<InfoRowProps> = ({ label, value }) => {
  return (
    <div className="info-row">
      <span className="info-row-label">{label}:</span>
      <span className="info-row-value">{value}</span>
    </div>
  );
};
