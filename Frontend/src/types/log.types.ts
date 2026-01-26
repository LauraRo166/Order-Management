export interface Log {
  id: string;
  orderId: string;
  fromState: string | null;
  toState: string;
  timestamp: string;
  customerName: string;
}
