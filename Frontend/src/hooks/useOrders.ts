import { useState, useEffect, useCallback } from 'react';
import { orderService } from '../services/order.service';
import { productService } from '../services/product.service';
import { logService, TransitionLog } from '../services/log.service';
import type { Order, CreateOrderDTO } from '../types/order.types';
import type { CreateProductDTO } from '../types/product.types';

export const useOrders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [logs, setLogs] = useState<TransitionLog[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = useCallback(async () => {
    try {
      const data = await orderService.getOrders();
      setOrders(data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    }
  }, []);

  const fetchLogs = useCallback(async () => {
    try {
      const data = await logService.getAllLogs(100);
      setLogs(data);
    } catch (error) {
      console.error('Failed to fetch logs:', error);
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchOrders(), fetchLogs()]);
      setLoading(false);
    };
    loadData();
  }, [fetchOrders, fetchLogs]);

  const createOrder = async (orderData: CreateOrderDTO) => {
    await orderService.createOrder(orderData);
    await fetchOrders();await fetchLogs();
  };

  const createProduct = async (productData: CreateProductDTO) => {
    return await productService.createProduct(productData);
  };

  const transitionOrder = async (orderId: string, action: string, cancellationReason?: string) => {
    await orderService.transitionOrder(orderId, action, cancellationReason);
    await fetchOrders();
    await fetchLogs();
  };

  return {
    orders,
    logs,
    loading,
    createOrder,
    createProduct,
    transitionOrder
  };
};