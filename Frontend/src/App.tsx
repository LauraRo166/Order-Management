import React, { useState } from 'react';
import { Header } from './components/common/Header';
import { OrdersPage } from './pages/OrdersPage';
import { LogsPage } from './pages/LogsPage';
import { useOrders } from './hooks/useOrders';
import type { CreateOrderDTO } from './types/order.types';

const App: React.FC = () => {
  const [view, setView] = useState<'orders' | 'logs'>('orders');
  const { orders, logs, loading, createOrder, createProduct, transitionOrder } = useOrders();

  const handleCreateOrder = async (orderData: CreateOrderDTO) => {
    try {
      await createOrder(orderData);
    } catch (error) {
      console.error('Failed to create order:', error);
    }
  };

  const handleTransitionOrder = async (orderId: string, action: string) => {
    try {
      await transitionOrder(orderId, action);
    } catch (error) {
      console.error('Failed to transition order:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading orders...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentView={view} onViewChange={setView} />

      {view === 'orders' ? (
        <OrdersPage
          orders={orders}
          onCreateOrder={handleCreateOrder}
          onCreateProduct={createProduct}
          onTransitionOrder={handleTransitionOrder}
        />
      ) : (
        <LogsPage logs={logs} />
      )}
    </div>
  );
};

export default App;