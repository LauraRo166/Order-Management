import React from 'react';
import '../styles/components/ProductList.css';

interface ProductDetail {
  name: string;
  quantity: number;
  unitPrice: number;
}

interface ProductListProps {
  products: ProductDetail[];
  totalAmount: number;
}

export const ProductList: React.FC<ProductListProps> = ({ products, totalAmount }) => {
  return (
    <div className="product-list">
      {products.map((product, idx) => (
        <div key={idx} className="product-list-item">
          <div>
            <p className="product-list-name">{product.name}</p>
            <p className="product-list-details">
              Quantity: {product.quantity} × ${product.unitPrice.toFixed(2)}
            </p>
          </div>
          <p className="product-list-subtotal">
            ${(product.quantity * product.unitPrice).toFixed(2)}
          </p>
        </div>
      ))}
      <div className="product-list-total">
        <span className="product-list-total-label">Total:</span>
        <span className="product-list-total-value">${totalAmount.toFixed(2)}</span>
      </div>
    </div>
  );
};
