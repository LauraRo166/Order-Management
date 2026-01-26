import React from 'react';
import '../../styles/components/FormInput.css';

interface FormInputProps {
  label: string;
  type?: 'text' | 'email' | 'number' | 'textarea';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  rows?: number;
  inputMode?: 'text' | 'numeric' | 'decimal' | 'email';
}

export const FormInput: React.FC<FormInputProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  disabled = false,
  required = false,
  rows = 3,
  inputMode
}) => {
  const commonProps = {
    value,
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      onChange(e.target.value),
    className: 'form-input',
    placeholder,
    disabled,
    required
  };

  return (
    <div className="form-input-group">
      <label className="form-input-label">
        {label}
        {required && <span className="form-input-required">*</span>}
      </label>
      {type === 'textarea' ? (
        <textarea {...commonProps} rows={rows} />
      ) : (
        <input
          {...commonProps}
          type={type}
          inputMode={inputMode}
        />
      )}
    </div>
  );
};
