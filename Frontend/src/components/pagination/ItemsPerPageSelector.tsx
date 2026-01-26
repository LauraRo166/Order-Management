import React from 'react';
import '../../styles/components/Pagination.css';

interface ItemsPerPageSelectorProps {
  value: number;
  onChange: (value: number) => void;
  options: number[];
  id?: string;
  label?: string;
}

export const ItemsPerPageSelector: React.FC<ItemsPerPageSelectorProps> = ({
  value,
  onChange,
  options,
  id = 'items-per-page',
  label = 'Show:'
}) => {
  return (
    <div className="items-per-page">
      <label htmlFor={id}>{label}</label>
      <select
        id={id}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="items-per-page-select"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option} per page
          </option>
        ))}
      </select>
    </div>
  );
};
