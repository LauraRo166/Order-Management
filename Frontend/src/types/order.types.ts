export type OrderState = 'Pending' | 'Review' | 'In Preparation' | 'Shipped' | 'Delivered' | 'Cancelled';

export interface Customer {
  name: string;
  email: string;
}

export interface ProductDetail {
  name: string;
  quantity: number;
  unitPrice: number;
}

export interface Order {
  id: string;
  amount: number;
  currentState: OrderState;
  creationDate: string;
  customer: Customer;
  productDetails?: ProductDetail[];
  notes?: string;
}

export interface TransitionLog {
  orderId: string;
  previousState: OrderState | null;
  newState: OrderState;
  timestamp: string;
  reason?: string;
  action: string;
}

export interface CreateOrderDTO {
  amount: number;
  current_state: 'pending';  // Siempre inicia en pending
  customer_id: string;
  products: Array<{
    product_id: string;
    name: string;
    quantity: number;
    unit_price: number;
  }>;
  notes?: string;
}

export interface CreateOrderFormData {
  customer: {
    name: string;
    email: string;
  };
  productDetails: ProductDetail[];
  amount: number;
  notes?: string;
}