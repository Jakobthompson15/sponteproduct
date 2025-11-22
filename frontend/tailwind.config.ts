import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'orange-fire': '#FF5810',
        'orange-hover': '#E64D0A',
        'charcoal': '#1A1D2E',
        'charcoal-light': '#2D3142',
        'sage-green': '#10B981',
        'sage-dark': '#059669',
        'cream': '#FFFBF5',
        'cream-dark': '#FFF5E6',
        'text-primary': '#1A1D2E',
        'text-secondary': '#4A5568',
        'text-muted': '#718096',
        'accent-yellow': '#FCD34D',
        'accent-red': '#EF4444',
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        heading: ['var(--font-heading)', 'system-ui', 'sans-serif'],
        body: ['var(--font-body)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      spacing: {
        'xs': '8px',
        'sm': '16px',
        'md': '24px',
        'lg': '32px',
        'xl': '48px',
        '2xl': '64px',
        '3xl': '96px',
        '4xl': '128px',
      },
      boxShadow: {
        'brutalist': '8px 8px 0 #1A1D2E',
        'brutalist-sm': '4px 4px 0 #1A1D2E',
        'brutalist-hover': '6px 6px 0 #1A1D2E',
      },
      borderRadius: {
        'brutalist': '12px',
        'brutalist-lg': '20px',
      },
    },
  },
  plugins: [],
};

export default config;
