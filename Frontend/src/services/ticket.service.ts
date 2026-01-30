import { apiClient } from '../api/client';
import type { Ticket } from '../types/order.types';

interface BackendTicket {
  id: string;
  order_id: string;
  cancellation_reason: string;
  creation_date: string;
}

class TicketService {
  private readonly BASE_PATH = '/tickets';

  private mapBackendTicketToFrontend(backendTicket: BackendTicket): Ticket {
    return {
      id: backendTicket.id,
      orderId: backendTicket.order_id,
      cancellationReason: backendTicket.cancellation_reason,
      creationDate: backendTicket.creation_date
    };
  }

  async getAllTickets(): Promise<Ticket[]> {
    const response = await apiClient.get<BackendTicket[]>(this.BASE_PATH);
    return response.data.map(ticket => this.mapBackendTicketToFrontend(ticket));
  }

  async getTicketById(ticketId: string): Promise<Ticket> {
    const response = await apiClient.get<BackendTicket>(`${this.BASE_PATH}/${ticketId}`);
    return this.mapBackendTicketToFrontend(response.data);
  }

  async getTicketByOrderId(orderId: string): Promise<Ticket | null> {
    try {
      const response = await apiClient.get<BackendTicket>(`${this.BASE_PATH}/order/${orderId}`);
      return this.mapBackendTicketToFrontend(response.data);
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  }
}

export const ticketService = new TicketService();
