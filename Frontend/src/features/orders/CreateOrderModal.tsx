import React, { useState } from 'react';
import { X, Plus } from 'lucide-react';
import { ModalSection } from '../../components/common/ModalSection';
import { FormInput } from '../../components/common/FormInput';
import { ProductInputRow } from '../../components/ProductInputRow';
import type { CreateOrderDTO } from '../../types/order.types';
import type { CreateProductDTO } from '../../types/product.types';
import { customerService } from '../../services/customer.service';
import '../../styles/features/orders/CreateOrderModal.css';

interface CreateOrderModalProps {
  onClose: () => void;
  onCreate: (order: CreateOrderDTO) => Promise<void>;
  onCreateProduct: (product: CreateProductDTO) => Promise<void>;
}

interface ProductInput {
  name: string;
  quantity: string;
  unit_price: string;
  isConfirmed: boolean;
  productId?: string;
}

export const CreateOrderModal: React.FC<CreateOrderModalProps> = ({
  onClose,
  onCreate,
  onCreateProduct
}) => {
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');
  const [notes, setNotes] = useState('');
  const [products, setProducts] = useState<ProductInput[]>([
    { name: '', quantity: '1', unit_price: '', isConfirmed: false }
  ]);
  const [creatingProductIndex, setCreatingProductIndex] = useState<number | null>(null);

  const addProduct = () => {
    setProducts([...products, { name: '', quantity: '1', unit_price: '', isConfirmed: false }]);
  };

  const removeProduct = (idx: number) => {
    setProducts(products.filter((_, i) => i !== idx));
  };

  const updateProduct = (idx: number, field: keyof ProductInput, value: string) => {
    const updated = [...products];
    updated[idx] = { ...updated[idx], [field]: value };
    setProducts(updated);
  };

  const confirmProduct = async (idx: number) => {
    const product = products[idx];
    const price = parseFloat(product.unit_price);

    if (!product.name || !product.unit_price || price <= 0) {
      alert('Please fill in product name and valid price');
      return;
    }

    setCreatingProductIndex(idx);
    try {
      const productData: CreateProductDTO = {
        name: product.name,
        unit_price: price
      };

      const createdProduct = await onCreateProduct(productData);

      const updated = [...products];
      updated[idx] = {
        ...updated[idx],
        isConfirmed: true,
        productId: createdProduct.id
      };
      setProducts(updated);
    } catch (error) {
      console.log('Failed to create product:', error);
      alert('Failed to create product. Please try again.');
    } finally {
      setCreatingProductIndex(null);
    }
  };
  const total = products
    .filter(p => p.isConfirmed)
    .reduce((sum, p) => {
      const qty = parseFloat(p.quantity) || 0;
      const price = parseFloat(p.unit_price) || 0;
      return sum + (qty * price);
    }, 0);

  const handleCreate = async () => {
    const confirmedProducts = products.filter(p => p.isConfirmed);

    if (!customerName || !customerEmail || confirmedProducts.length === 0) {
      alert('Please fill customer information and confirm at least one product');
      return;
    }

    if (confirmedProducts.some(p => !p.productId)) {
      alert('All products must be confirmed before creating the order');
      return;
    }

    try {
      const customer = await customerService.createCustomer({
        name: customerName,
        email: customerEmail
      });

      const parsedProducts = confirmedProducts.map(p => ({
        product_id: p.productId || '',
        name: p.name,
        quantity: parseInt(p.quantity) || 1,
        unit_price: parseFloat(p.unit_price) || 0
      }));

      const orderData: CreateOrderDTO = {
        amount: total,
        current_state: 'pending',
        customer_id: customer.id,
        products: parsedProducts,
        notes: notes || undefined
      };

      await onCreate(orderData);
      onClose();
    } catch (error) {
      console.log('Failed to create order:', error);
      alert('Failed to create order. Please try again.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <div>
            <h2 className="modal-title">Create New Order</h2>
            <p className="modal-subtitle">Complete the form to create a new order</p>
          </div>
          <button onClick={onClose} className="modal-close-btn" aria-label="Close modal">
            <X className="modal-icon" />
          </button>
        </div>

        <div className="modal-body">
          <ModalSection title="Customer Information">
            <div className="section-content">
              <FormInput
                label="Customer Name"
                value={customerName}
                onChange={setCustomerName}
                placeholder="John Doe"
                required
              />
              <FormInput
                label="Email"
                type="email"
                value={customerEmail}
                onChange={setCustomerEmail}
                placeholder="john@example.com"
                inputMode="email"
                required
              />
            </div>
          </ModalSection>

          <ModalSection title="Products">
            <div className="section-header">
              <button onClick={addProduct} className="add-product-btn" type="button">
                <Plus className="btn-icon" />
                Add Product
              </button>
            </div>

            <div className="products-list">
              {products.map((product, idx) => (
                <ProductInputRow
                  key={idx}
                  name={product.name}
                  quantity={product.quantity}
                  unitPrice={product.unit_price}
                  isConfirmed={product.isConfirmed}
                  isCreating={creatingProductIndex === idx}
                  showRemove={products.length > 1}
                  onNameChange={(value) => updateProduct(idx, 'name', value)}
                  onQuantityChange={(value) => updateProduct(idx, 'quantity', value)}
                  onPriceChange={(value) => updateProduct(idx, 'unit_price', value)}
                  onConfirm={() => confirmProduct(idx)}
                  onRemove={() => removeProduct(idx)}
                />
              ))}
            </div>

            <div className="products-total">
              <span className="total-label">Total:</span>
              <span className="total-amount">${total.toFixed(2)}</span>
            </div>
          </ModalSection>

          <ModalSection title="Notes (Optional)">
            <FormInput
              label=""
              type="textarea"
              value={notes}
              onChange={setNotes}
              placeholder="Additional notes..."
              rows={3}
            />
          </ModalSection>

          <div className="modal-actions">
            <button onClick={onClose} className="btn-cancel" type="button">
              Cancel
            </button>
            <button onClick={handleCreate} className="btn-create" type="button">
              Create Order
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

