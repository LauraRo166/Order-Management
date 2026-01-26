import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { OrderList } from '../features/orders/OrderList';
import { CreateOrderModal } from '../features/orders/CreateOrderModal';
import type { Order, CreateOrderDTO } from '../types/order.types';
import type { CreateProductDTO } from '../types/product.types';
import '../styles/pages/OrdersPage.css';

interface OrdersPageProps {
  orders: Order[];
  onCreateOrder: (order: CreateOrderDTO) => Promise<void>;
  onCreateProduct: (product: CreateProductDTO) => Promise<void>;
  onTransitionOrder: (orderId: string, action: string) => Promise<void>;
}

export const OrdersPage: React.FC<OrdersPageProps> = ({
  orders,
  onCreateOrder,
  onCreateProduct,
  onTransitionOrder
}) => {
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <div className="orders-page-container">
      <div className="orders-page-header">
        <div>
          <h1 className="orders-page-title">Orders</h1>
          <p className="orders-page-subtitle">
            Manage and track your orders · {orders.length} total orders
          </p>
        </div>
        <button onClick={() => setShowCreateModal(true)} className="create-order-btn">
          <Plus className="btn-icon" />
          New Order
        </button>
      </div>

      <OrderList
        orders={orders}
        onTransitionOrder={onTransitionOrder}
      />

      {showCreateModal && (
        <CreateOrderModal
          onClose={() => setShowCreateModal(false)}
          onCreate={onCreateOrder}
          onCreateProduct={onCreateProduct}
        />
      )}
    </div>
  );
};
