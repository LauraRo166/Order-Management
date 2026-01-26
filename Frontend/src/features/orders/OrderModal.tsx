import React from 'react';
import { X, Package } from 'lucide-react';
import { Badge } from '../../components/common/Badge';
import { OrderStepper } from '../../components/OrderStepper';
import { ModalSection } from '../../components/common/ModalSection';
import { InfoRow } from '../../components/common/InfoRow';
import { ProductList } from '../../components/ProductList';
import { NavigationButtons } from '../../components/common/NavigationButtons';
import type { Order, OrderState } from '../../types/order.types';
import '../../styles/features/orders/OrderModal.css';

interface OrderModalProps {
  order: Order;
  onClose: () => void;
  onTransition: (action: string) => void;
  onNavigate?: (direction: 'prev' | 'next') => void;
  hasPrevious?: boolean;
  hasNext?: boolean;
  currentIndex?: number;
  totalOrders?: number;
}

interface ActionButton {
  label: string;
  action: string;
  variant: 'blue' | 'orange' | 'purple' | 'green' | 'red';
}

const getAvailableActions = (order: Order): ActionButton[] => {
  const { currentState, amount } = order;

  const actionMap: Record<OrderState, ActionButton[]> = {
    'pending': amount > 1000
      ? [
          { label: 'Submit for Review', action: 'submit_for_review', variant: 'orange' },
          { label: 'Cancel Order', action: 'cancel', variant: 'red' }
        ]
      : [
          { label: 'Start Preparation', action: 'start_preparation', variant: 'blue' },
          { label: 'Cancel Order', action: 'cancel', variant: 'red' }
        ],
    'review': [
      { label: 'Approve & Start Preparation', action: 'approve', variant: 'blue' },
      { label: 'Cancel Order', action: 'cancel', variant: 'red' }
    ],
    'in_preparation': [
      { label: 'Ship Order', action: 'ship', variant: 'purple' },
      { label: 'Cancel Order', action: 'cancel', variant: 'red' }
    ],
    'shipped': [
      { label: 'Confirm Delivery', action: 'deliver', variant: 'green' }
    ],
    'delivered': [],
    'cancelled': []
  };

  return actionMap[currentState] || [];
};

export const OrderModal: React.FC<OrderModalProps> = ({
  order,
  onClose,
  onTransition,
  onNavigate,
  hasPrevious = false,
  hasNext = false,
  currentIndex,
  totalOrders
}) => {
  const actions = getAvailableActions(order);

  return (
    <div className="order-modal-overlay">
      <div className="order-modal-content">
        <div className="order-modal-header">
          <div className="order-modal-header-left">
            <div>
              <h2 className="order-modal-title">Order {order.id}</h2>
              <p className="order-modal-subtitle">Customer: {order.customer.name}</p>
            </div>
            {currentIndex !== undefined && totalOrders !== undefined && (
              <div className="order-modal-pagination-info">
                Order {currentIndex + 1} of {totalOrders}
              </div>
            )}
          </div>
          <div className="order-modal-header-right">
            {onNavigate && (
              <NavigationButtons
                onPrevious={() => onNavigate('prev')}
                onNext={() => onNavigate('next')}
                hasPrevious={hasPrevious}
                hasNext={hasNext}
                previousLabel="Previous order"
                nextLabel="Next order"
              />
            )}
            <button onClick={onClose} className="order-modal-close" aria-label="Close modal">
              <X className="order-modal-icon" />
            </button>
          </div>
        </div>

        <div className="order-modal-body">
          <ModalSection title="Order Status">
            <OrderStepper currentState={order.currentState} />
            <div className="order-status-badge">
              <Badge state={order.currentState} />
            </div>
          </ModalSection>

          <ModalSection title="Customer Information">
            <div className="order-info-grid">
              <InfoRow label="Name" value={order.customer.name} />
              <InfoRow label="Email" value={order.customer.email} />
              <InfoRow
                label="Creation Date"
                value={new Date(order.creationDate).toLocaleString()}
              />
            </div>
          </ModalSection>

          <ModalSection title="Products">
            <ProductList
              products={order.productDetails || []}
              totalAmount={order.amount}
            />
          </ModalSection>

          {actions.length > 0 && (
            <ModalSection title="Actions">
              <div className="order-actions-grid">
                {actions.map((action) => (
                  <button
                    key={action.action}
                    onClick={() => onTransition(action.action)}
                    className={`order-action-btn action-btn-${action.variant}`}
                  >
                    <Package className="action-btn-icon" />
                    {action.label}
                  </button>
                ))}
              </div>
            </ModalSection>
          )}
        </div>
      </div>
    </div>
  );
};