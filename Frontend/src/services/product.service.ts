import { apiClient } from '../api/client';

export interface Product {
  id: string;
  name: string;
  unit_price: number;
}

export interface ProductCreate {
  name: string;
  unit_price: number;
}

export class ProductService {
  private readonly BASE_PATH = '/products';

  async getAllProducts(): Promise<Product[]> {
    const response = await apiClient.get<Product[]>(this.BASE_PATH);
    return response.data;
  }

  async getProduct(productId: string): Promise<Product> {
    const response = await apiClient.get<Product>(`${this.BASE_PATH}/${productId}`);
    return response.data;
  }

  async createProduct(product: ProductCreate): Promise<Product> {
    const response = await apiClient.post<Product>(this.BASE_PATH, product);
    return response.data;
  }
}

export const productService = new ProductService();