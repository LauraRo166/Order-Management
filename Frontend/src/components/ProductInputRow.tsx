import React from 'react';
import { Check, Trash2 } from 'lucide-react';
import '../styles/components/ProductInputRow.css';

interface ProductInputRowProps {
  name: string;
  quantity: string;
  unitPrice: string;
  isConfirmed: boolean;
  isCreating: boolean;
  showRemove: boolean;
  onNameChange: (value: string) => void;
  onQuantityChange: (value: string) => void;
  onPriceChange: (value: string) => void;
  onConfirm: () => void;
  onRemove: () => void;
}

export const ProductInputRow: React.FC<ProductInputRowProps> = ({
  name,
  quantity,
  unitPrice,
  isConfirmed,
  isCreating,
  showRemove,
  onNameChange,
  onQuantityChange,
  onPriceChange,
  onConfirm,
  onRemove
}) => {
  return (
    <div className={`product-input-row ${isConfirmed ? 'confirmed' : ''}`}>
      <div className="product-input-field product-name">
        <label className="product-input-label">Product Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => onNameChange(e.target.value)}
          className="product-input"
          placeholder="Product name"
          disabled={isConfirmed}
        />
      </div>

      <div className="product-input-field product-quantity">
        <label className="product-input-label">Quantity</label>
        <input
          type="text"
          inputMode="numeric"
          value={quantity}
          onChange={(e) => {
            const value = e.target.value;
            if (value === '' || /^\d+$/.test(value)) {
              onQuantityChange(value);
            }
          }}
          className="product-input"
          placeholder="1"
          disabled={isConfirmed}
        />
      </div>

      <div className="product-input-field product-price">
        <label className="product-input-label">Unit Price</label>
        <input
          type="text"
          inputMode="decimal"
          value={unitPrice}
          onChange={(e) => {
            const value = e.target.value;
            if (value === '' || /^\d*\.?\d*$/.test(value)) {
              onPriceChange(value);
            }
          }}
          className="product-input"
          placeholder="0.00"
          disabled={isConfirmed}
        />
      </div>

      <div className="product-input-actions">
        {!isConfirmed ? (
          <button
            onClick={onConfirm}
            className="product-confirm-btn"
            type="button"
            disabled={isCreating}
            title="Confirm and create product"
          >
            <Check className="btn-icon" />
          </button>
        ) : (
          <div className="product-confirmed-badge">✓</div>
        )}

        {showRemove && (
          <button
            onClick={onRemove}
            className="product-remove-btn"
            type="button"
            disabled={isCreating}
          >
            <Trash2 className="btn-icon" />
          </button>
        )}
      </div>
    </div>
  );
};
