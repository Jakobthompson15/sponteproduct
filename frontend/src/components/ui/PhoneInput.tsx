'use client';

import { forwardRef, InputHTMLAttributes, useState, ChangeEvent } from 'react';
import { cn } from '@/lib/utils/cn';

export interface PhoneInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  label?: string;
  error?: string;
  hint?: string;
  onChange?: (value: string) => void;
}

export const PhoneInput = forwardRef<HTMLInputElement, PhoneInputProps>(
  ({ label, error, hint, className, required, onChange, ...props }, ref) => {
    const [displayValue, setDisplayValue] = useState('');

    const formatPhoneNumber = (value: string): string => {
      // Remove all non-digits
      const digits = value.replace(/\D/g, '');

      // Format as (XXX) XXX-XXXX
      if (digits.length <= 3) {
        return digits;
      } else if (digits.length <= 6) {
        return `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
      } else {
        return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 10)}`;
      }
    };

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
      const rawValue = e.target.value;
      const formatted = formatPhoneNumber(rawValue);

      setDisplayValue(formatted);

      // Pass the formatted value back to the form
      if (onChange) {
        onChange(formatted);
      }

      // Update the underlying input value
      if (ref && typeof ref === 'object' && ref.current) {
        ref.current.value = formatted;
      }
    };

    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-heading font-semibold text-charcoal mb-2">
            {label}
            {required && <span className="text-accent-red ml-1">*</span>}
          </label>
        )}

        <input
          ref={ref}
          type="tel"
          value={displayValue}
          onChange={handleChange}
          className={cn(
            'w-full px-4 py-3',
            'bg-white',
            'border-2 border-charcoal',
            'rounded-lg',
            'font-body text-base',
            'text-charcoal placeholder:text-text-muted',
            'transition-all duration-200',
            'focus:outline-none focus:ring-2 focus:ring-orange-fire focus:border-orange-fire',
            'disabled:bg-cream disabled:cursor-not-allowed',
            error && 'border-accent-red focus:ring-accent-red focus:border-accent-red',
            className
          )}
          {...props}
        />

        {hint && !error && (
          <p className="mt-1 text-xs text-text-muted">{hint}</p>
        )}

        {error && (
          <p className="mt-1 text-sm text-accent-red font-medium">{error}</p>
        )}
      </div>
    );
  }
);

PhoneInput.displayName = 'PhoneInput';
