import React from 'react';
import '../../styles/components/ModalSection.css';

interface ModalSectionProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export const ModalSection: React.FC<ModalSectionProps> = ({
  title,
  children,
  className = ''
}) => {
  return (
    <div className={`modal-section ${className}`}>
      <h3 className="modal-section-title">{title}</h3>
      {children}
    </div>
  );
};
