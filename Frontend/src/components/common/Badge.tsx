import React from 'react';
import type { OrderState } from '../types/order.types';
import '../../styles/components/Badge.css';

interface BadgeProps {
  state: OrderState | string;
}

const STATE_LABELS: Record<string, string> = {
  'pending': 'Pending',
  'review': 'Review',
  'in_preparation': 'In Preparation',
  'shipped': 'Shipped',
  'delivered': 'Delivered',
  'cancelled': 'Cancelled'
};

export const Badge: React.FC<BadgeProps> = ({ state }) => {
  const stateKey = state.toLowerCase().replace(' ', '_');
  const className = `badge badge-${state.toLowerCase().replace(/[_ ]/g, '-')}`;
  const label = STATE_LABELS[stateKey] || state;

  return (
    <span className={className}>
      {label}
    </span>
  );
};