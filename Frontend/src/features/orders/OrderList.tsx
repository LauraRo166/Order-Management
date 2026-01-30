import React, { useState } from 'react';
import { OrderCard } from './OrderCard';
import { OrderModal } from './OrderModal';
import { PaginationControls } from '../../components/pagination/PaginationControls';
import { ItemsPerPageSelector } from '../../components/pagination/ItemsPerPageSelector';
import { usePagination } from '../../hooks/usePagination';
import type { Order } from '../../types/order.types';
import '../../styles/features/orders/OrderList.css';

interface OrderListProps {
  orders: Order[];
  onTransitionOrder: (orderId: string, action: string, cancellationReason?: string) => Promise<void>;
}

export const OrderList: React.FC<OrderListProps> = ({
  orders,
  onTransitionOrder
}) => {
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);

  const {
    currentPage,
    itemsPerPage,
    totalPages,
    startIndex,
    endIndex,
    paginatedItems: paginatedOrders,
    setItemsPerPage,
    goToPage
  } = usePagination({ items: orders, initialItemsPerPage: 9 });

  const handleTransition = async (action: string, cancellationReason?: string) => {
    if (selectedOrderId) {
      await onTransitionOrder(selectedOrderId, action, cancellationReason);
    }
  };

  const handleNavigate = (direction: 'prev' | 'next') => {
    if (!selectedOrderId) return;

    const currentIndex = orders.findIndex(order => order.id === selectedOrderId);
    if (currentIndex === -1) return;

    if (direction === 'prev' && currentIndex > 0) {
      setSelectedOrderId(orders[currentIndex - 1].id);
    } else if (direction === 'next' && currentIndex < orders.length - 1) {
      setSelectedOrderId(orders[currentIndex + 1].id);
    }
  };

  const selectedOrder = selectedOrderId
    ? orders.find(order => order.id === selectedOrderId)
    : null;

  const selectedOrderIndex = selectedOrderId
    ? orders.findIndex(order => order.id === selectedOrderId)
    : null;

  return (
    <>
      {orders.length > 0 && (
        <div className="pagination-controls-top">
          <ItemsPerPageSelector
            value={itemsPerPage}
            onChange={setItemsPerPage}
            options={[6, 9, 12, 24]}
            id="items-per-page"
          />
          <div className="pagination-info">
            Showing {startIndex + 1}-{Math.min(endIndex, orders.length)} of {orders.length}
          </div>
        </div>
      )}

      <div className="orders-grid">
        {orders.length === 0 ? (
          <div className="empty-state">
            <p className="empty-state-text">No orders yet. Create your first order!</p>
          </div>
        ) : (
          paginatedOrders.map((order, paginatedIndex) => {
            return (
              <OrderCard
                key={order.id}
                order={order}
                onView={() => setSelectedOrderId(order.id)}
              />
            );
          })
        )}
      </div>

      {totalPages > 1 && (
        <PaginationControls
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={goToPage}
        />
      )}

      {selectedOrder && selectedOrderIndex !== null && (
        <OrderModal
          order={selectedOrder}
          onClose={() => setSelectedOrderId(null)}
          onTransition={handleTransition}
          onNavigate={handleNavigate}
          hasPrevious={selectedOrderIndex > 0}
          hasNext={selectedOrderIndex < orders.length - 1}
          currentIndex={selectedOrderIndex}
          totalOrders={orders.length}
        />
      )}
    </>
  );
};