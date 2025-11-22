'use client';

import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { UseFormRegister, FieldErrors, UseFormSetValue } from 'react-hook-form';
import type { OnboardingFormData } from '@/types/onboarding';

interface BusinessProfileProps {
  register: UseFormRegister<OnboardingFormData>;
  errors: FieldErrors<OnboardingFormData>;
  setValue: UseFormSetValue<OnboardingFormData>;
}

export function BusinessProfile({ register, errors, setValue }: BusinessProfileProps) {
  const formatPhoneNumber = (value: string): string => {
    const digits = value.replace(/\D/g, '');
    if (digits.length <= 3) {
      return digits;
    } else if (digits.length <= 6) {
      return `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
    } else {
      return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 10)}`;
    }
  };

  const handlePhoneChange = (fieldName: 'phone' | 'phoneSecondary') => (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatPhoneNumber(e.target.value);
    setValue(fieldName, formatted, { shouldValidate: true });
  };

  const handleUrlBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    let value = e.target.value.trim();

    // Skip if empty (it's optional)
    if (!value) return;

    // Add https:// if no protocol is present
    if (value && !value.match(/^https?:\/\//i)) {
      value = `https://${value}`;
      setValue('websiteUrl', value, { shouldValidate: true });
    }
  };

  return (
    <div className="space-y-6">
      <p className="text-text-secondary mb-8">
        We'll use this information to verify your NAP (Name, Address, Phone)
        consistency across all platforms.
      </p>

      <Input
        {...register('email')}
        type="email"
        label="Email Address"
        placeholder="you@yourbusiness.com"
        hint="We'll send your agent reports and updates here"
        error={errors.email?.message}
        required
      />

      <Input
        {...register('businessName')}
        label="Legal Business Name"
        placeholder="Tony's Pizzeria LLC"
        hint="Exactly as it appears on your business license"
        error={errors.businessName?.message}
        required
      />

      <Input
        {...register('dbaName')}
        label="Doing Business As Name"
        placeholder="Tony's Pizza"
        hint="The public-facing name customers know you by (if different)"
        error={errors.dbaName?.message}
      />

      <Input
        {...register('streetAddress')}
        label="Street Address"
        placeholder="123 Main Street"
        error={errors.streetAddress?.message}
        required
      />

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div className="col-span-2 md:col-span-1">
          <Input
            {...register('city')}
            label="City"
            placeholder="Chicago"
            error={errors.city?.message}
            required
          />
        </div>
        <Input
          {...register('state')}
          label="State"
          placeholder="IL"
          error={errors.state?.message}
          required
        />
        <Input
          {...register('zipCode')}
          label="ZIP"
          placeholder="60601"
          error={errors.zipCode?.message}
          required
        />
      </div>

      <Input
        {...register('phone', {
          onChange: handlePhoneChange('phone')
        })}
        type="tel"
        label="Primary Phone Number"
        placeholder="(312) 555-1234"
        hint="Auto-formats as you type - This should match your GBP and website exactly"
        error={errors.phone?.message}
        required
      />

      <Input
        {...register('phoneSecondary', {
          onChange: handlePhoneChange('phoneSecondary')
        })}
        type="tel"
        label="Secondary Phone"
        placeholder="(312) 555-5678"
        hint="Toll-free number, text line, etc. (auto-formats as you type)"
        error={errors.phoneSecondary?.message}
      />

      <Input
        {...register('websiteUrl')}
        type="url"
        label="Website URL"
        placeholder="tonyspizza.com"
        hint="Just enter your domain - we'll add https:// automatically"
        error={errors.websiteUrl?.message}
        onBlur={handleUrlBlur}
      />

      <Select
        {...register('cmsPlatform')}
        label="CMS Platform"
        error={errors.cmsPlatform?.message}
      >
        <option value="">Select your CMS...</option>
        <option value="wordpress">WordPress</option>
        <option value="webflow">Webflow</option>
        <option value="shopify">Shopify</option>
        <option value="squarespace">Squarespace</option>
        <option value="wix">Wix</option>
        <option value="custom">Custom / Other</option>
      </Select>

      <Input
        {...register('primaryCategory')}
        label="Primary Business Category"
        placeholder="e.g., Pizza Restaurant, Dentist, Plumber"
        hint="We'll analyze keywords based on this category automatically"
        error={errors.primaryCategory?.message}
        required
      />

      <Textarea
        {...register('services')}
        label="Services You Offer"
        placeholder="Pizza Delivery&#10;Dine-In&#10;Catering&#10;Gluten-Free Options"
        hint="One service per line - We'll use this for keyword research (3-5 services)"
        error={errors.services?.message}
      />

      <Input
        {...register('coverageRadius', { valueAsNumber: true })}
        type="number"
        label="Service Area Radius (miles)"
        placeholder="10"
        hint="How far do you serve customers from your location?"
        error={errors.coverageRadius?.message}
      />
    </div>
  );
}
