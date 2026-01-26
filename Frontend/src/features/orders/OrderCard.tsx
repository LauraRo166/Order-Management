import React from 'react';
import { Package, Eye } from 'lucide-react';
import { Badge } from '../../components/common/Badge';
import type { Order } from '../../types/order.types';
import '../../styles/features/orders/OrderCard.css';

interface OrderCardProps {
  order: Order;
  onView: () => void;
}

export const OrderCard: React.FC<OrderCardProps> = ({ order, onView }) => {
  return (
    <div className="order-card">
      <div className="order-card-header">
        <div className="order-card-info">
          <Package className="order-card-icon" />
          <div>
            <h3 className="order-card-id">{order.id}</h3>
            <p className="order-card-customer">{order.customer.name}</p>
          </div>
        </div>
        <button onClick={onView} className="order-card-view-btn" aria-label="View order details">
          <Eye className="order-card-icon" />
        </button>
      </div>

      <div className="order-card-amount">
        <p className="order-card-amount-label">Total Amount</p>
        <p className="order-card-amount-value">${order.amount.toFixed(2)}</p>
      </div>

      <div className="order-card-footer">
        <Badge state={order.currentState} />
      </div>
    </div>
  );
};