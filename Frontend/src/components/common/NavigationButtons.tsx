import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/components/NavigationButtons.css';

interface NavigationButtonsProps {
  onPrevious: () => void;
  onNext: () => void;
  hasPrevious: boolean;
  hasNext: boolean;
  previousLabel?: string;
  nextLabel?: string;
}

export const NavigationButtons: React.FC<NavigationButtonsProps> = ({
  onPrevious,
  onNext,
  hasPrevious,
  hasNext,
  previousLabel = 'Previous',
  nextLabel = 'Next'
}) => {
  return (
    <div className="navigation-buttons">
      <button
        onClick={onPrevious}
        disabled={!hasPrevious}
        className="nav-btn"
        aria-label={previousLabel}
        title={previousLabel}
      >
        <ChevronLeft className="nav-btn-icon" />
      </button>
      <button
        onClick={onNext}
        disabled={!hasNext}
        className="nav-btn"
        aria-label={nextLabel}
        title={nextLabel}
      >
        <ChevronRight className="nav-btn-icon" />
      </button>
    </div>
  );
};
