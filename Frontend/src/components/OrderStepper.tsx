import React from 'react';
import type { OrderState } from '../types/order.types';
import '../styles/components/OrderStepper.css';

interface OrderStepperProps {
  currentState: OrderState;
}

const STANDARD_STEPS: { state: OrderState; label: string }[] = [
  { state: 'pending', label: 'Pending' },
  { state: 'in_preparation', label: 'In Preparation' },
  { state: 'shipped', label: 'Shipped' },
  { state: 'delivered', label: 'Delivered' }
];

export const OrderStepper: React.FC<OrderStepperProps> = ({ currentState }) => {
  if (currentState === 'review') {
    return (
      <div className="stepper-review">
        <div className="step-item">
          <div className="step-circle completed">
            <span className="step-check">✓</span>
          </div>
          <span className="step-label">Pending</span>
        </div>
        <div className="step-line active"></div>
        <div className="step-item">
          <div className="step-circle active">2</div>
          <span className="step-label active">Review</span>
        </div>
      </div>
    );
  }

  if (currentState === 'cancelled') {
    return (
      <div className="stepper-cancelled">
        <div className="step-item">
          <div className="step-circle cancelled">✗</div>
          <span className="step-label cancelled">Cancelled</span>
        </div>
      </div>
    );
  }

  const currentIndex = STANDARD_STEPS.findIndex(step => step.state === currentState);

  return (
    <div className="stepper">
      {STANDARD_STEPS.map((step, idx) => {
        const isActive = idx === currentIndex;
        const isCompleted = idx < currentIndex;
        const isInactive = idx > currentIndex;

        return (
          <React.Fragment key={step.state}>
            <div className="step-item">
              <div className={`step-circle ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''} ${isInactive ? 'inactive' : ''}`}>
                {isCompleted ? '✓' : idx + 1}
              </div>
              <span className={`step-label ${isActive ? 'active' : ''}`}>
                {step.label}
              </span>
            </div>
            {idx < STANDARD_STEPS.length - 1 && (
              <div className={`step-line ${idx < currentIndex ? 'active' : ''}`}></div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};