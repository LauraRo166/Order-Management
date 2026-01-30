import { apiClient } from '../api/client';
import type { Order, CreateOrderDTO } from '../types/order.types';

interface BackendOrder {
  id: string;
  amount: number;
  current_state: string;
  creation_date: string;
  customer: {
    name: string;
    email: string;
  };
  products: Array<{
    product_id: string;
    name: string;
    quantity: number;
    unit_price: number;
  }>;
  notes?: string;
}

class OrderService {
  private readonly BASE_PATH = '/orders';

  private mapBackendOrderToFrontend(backendOrder: BackendOrder): Order {
    return {
      id: backendOrder.id,
      amount: backendOrder.amount,
      currentState: backendOrder.current_state as Order['currentState'],
      creationDate: backendOrder.creation_date,
      customer: backendOrder.customer,
      productDetails: backendOrder.products.map(p => ({
        name: p.name,
        quantity: p.quantity,
        unitPrice: p.unit_price
      })),
      notes: backendOrder.notes
    };
  }

  async getOrders(): Promise<Order[]> {
    const response = await apiClient.get<BackendOrder[]>(this.BASE_PATH);
    return response.data.map(order => this.mapBackendOrderToFrontend(order));
  }

  async createOrder(order: CreateOrderDTO): Promise<Order> {
    const response = await apiClient.post<BackendOrder>(this.BASE_PATH, order);
    return this.mapBackendOrderToFrontend(response.data);
  }

  async deleteOrder(orderId: string): Promise<void> {
    await apiClient.delete(`${this.BASE_PATH}/${orderId}`);
  }

  async transitionOrder(orderId: string, action: string, cancellationReason?: string): Promise<Order> {
    const payload: { action: string; cancellation_reason?: string } = { action };

    if (action === 'cancel') {
      if (!cancellationReason || cancellationReason.trim() === '') {
        throw new Error('Cancellation reason is required');
      }
      payload.cancellation_reason = cancellationReason;
    }

    const response = await apiClient.post<BackendOrder>(
      `${this.BASE_PATH}/${orderId}/transition`,
      payload
    );
    return this.mapBackendOrderToFrontend(response.data);
  }

  async getOrderLogs(orderId: string): Promise<any[]> {
    const response = await apiClient.get(`${this.BASE_PATH}/${orderId}/logs`);
    return response.data;
  }

  async getAllLogs(limit: number = 100): Promise<any[]> {
    const response = await apiClient.get(`${this.BASE_PATH}/logs`, {
      params: { limit }
    });
    return response.data;
  }

  async getAllowedActions(orderId: string): Promise<string[]> {
    const response = await apiClient.get<string[]>(
      `${this.BASE_PATH}/${orderId}/allowed-actions`
    );
    return response.data;
  }
}

export const orderService = new OrderService();