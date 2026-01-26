import { apiClient } from '../api/client';

export interface Customer {
  id: string;
  name: string;
  email: string;
}

export interface CustomerCreate {
  name: string;
  email: string;
}

export class CustomerService {
  private readonly BASE_PATH = '/customers';

  async getCustomer(customerId: string): Promise<Customer> {
    const response = await apiClient.get<Customer>(`${this.BASE_PATH}/${customerId}`);
    return response.data;
  }

  async createCustomer(customer: CustomerCreate): Promise<Customer> {
    const response = await apiClient.post<Customer>(this.BASE_PATH, customer);
    return response.data;
  }
}

export const customerService = new CustomerService();