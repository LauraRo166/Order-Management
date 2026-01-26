import { apiClient } from '../api/client';

interface BackendLog {
  id: string;
  order_id: string;
  previous_state: string | null;
  new_state: string;
  action_taken: string;
  transition_date: string;
}

export interface TransitionLog {
  id: string;
  orderId: string;
  previousState: string | null;
  newState: string;
  actionTaken: string;
  transitionDate: string;
}

export class LogService {
  private readonly BASE_PATH = '/orders';

  private mapBackendLogToFrontend(backendLog: BackendLog): TransitionLog {
    return {
      id: backendLog.id,
      orderId: backendLog.order_id,
      previousState: backendLog.previous_state,
      newState: backendLog.new_state,
      actionTaken: backendLog.action_taken,
      transitionDate: backendLog.transition_date
    };
  }

  async getOrderLogs(orderId: string): Promise<TransitionLog[]> {
    const response = await apiClient.get<BackendLog[]>(
      `${this.BASE_PATH}/${orderId}/logs`
    );
    return response.data.map(log => this.mapBackendLogToFrontend(log));
  }

  async getAllLogs(limit: number = 100): Promise<TransitionLog[]> {
    const response = await apiClient.get<BackendLog[]>(
      `${this.BASE_PATH}/logs`,
      { params: { limit } }
    );
    return response.data.map(log => this.mapBackendLogToFrontend(log));
  }

  filterLogsByOrderId(logs: TransitionLog[], orderId: string): TransitionLog[] {
    return logs.filter(log => log.orderId === orderId);
  }

  sortLogsByDate(logs: TransitionLog[], descending = true): TransitionLog[] {
    return [...logs].sort((a, b) => {
      const dateA = new Date(a.transitionDate).getTime();
      const dateB = new Date(b.transitionDate).getTime();
      return descending ? dateB - dateA : dateA - dateB;
    });
  }
}

export const logService = new LogService();