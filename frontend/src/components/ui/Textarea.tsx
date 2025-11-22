import { cn } from '@/lib/utils/cn';
import { forwardRef, TextareaHTMLAttributes } from 'react';

export interface TextareaProps
  extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string;
  label?: string;
  hint?: string;
}

const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, error, label, hint, required, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block font-heading font-semibold text-sm text-text-primary mb-2">
            {label}
            {required && <span className="text-accent-red ml-1">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          className={cn(
            'w-full px-4 py-3 border-2 border-charcoal rounded-lg font-body text-base text-text-primary transition-all',
            'focus:outline-none focus:border-orange-fire focus:shadow-[0_0_0_3px_rgba(255,88,16,0.1)]',
            'min-h-[100px] resize-vertical',
            error && 'border-accent-red focus:border-accent-red',
            className
          )}
          {...props}
        />
        {hint && !error && (
          <p className="text-sm text-text-muted mt-2">{hint}</p>
        )}
        {error && <p className="text-sm text-accent-red mt-2">{error}</p>}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';

export { Textarea };
