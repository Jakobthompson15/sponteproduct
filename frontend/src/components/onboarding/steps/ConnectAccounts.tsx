'use client';

import { Button } from '@/components/ui/Button';
import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ConnectAccountsProps {
  locationId?: string | null;
}

export function ConnectAccounts({ locationId: propLocationId }: ConnectAccountsProps = {}) {
  const [connected, setConnected] = useState({
    gbp: false,
    gsc: false,
    ga4: false,
    wordpress: false,
  });
  const [locationId, setLocationId] = useState<string | null>(propLocationId || null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Get location_id and check connection status
  useEffect(() => {
    const init = async () => {
      // If location_id is passed as prop, use it
      if (propLocationId) {
        setLocationId(propLocationId);
        await fetchConnectionStatus(propLocationId);
        setIsLoading(false);
        return;
      }

      // Otherwise, try to get from localStorage (onboarding flow)
      const savedOnboarding = localStorage.getItem('sponte_onboarding_draft');
      if (savedOnboarding) {
        try {
          const data = JSON.parse(savedOnboarding);
          if (data.locationId) {
            setLocationId(data.locationId);
            await fetchConnectionStatus(data.locationId);
          }
        } catch (error) {
          console.error('Error parsing saved onboarding:', error);
        }
      }
      setIsLoading(false);
    };

    init();
  }, [propLocationId]);

  const fetchConnectionStatus = async (locId: string) => {
    try {
      // Get Clerk token
      const clerk = (window as any).Clerk;
      if (!clerk || !clerk.session) {
        return;
      }

      const token = await clerk.session.getToken();
      if (!token) {
        return;
      }

      // Fetch connection status from backend
      const response = await fetch(`${API_URL}/api/oauth/connections/status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setConnected({
          gbp: data.google_business_profile?.connected || false,
          gsc: data.google_search_console?.connected || false,
          ga4: data.google_analytics?.connected || false,
          wordpress: data.wordpress?.connected || false,
        });
      }
    } catch (error) {
      console.error('Error fetching connection status:', error);
    }
  };

  const handleConnectGBP = () => {
    if (!locationId) {
      toast.error('Please wait a moment - we\'re still setting up your account. Try clicking "Connect" again in a few seconds.');
      return;
    }

    setIsConnecting(true);

    // Redirect to backend OAuth endpoint with the real location_id
    window.location.href = `${API_URL}/api/oauth/google/connect?location_id=${locationId}`;
  };

  const handleConnect = (provider: keyof typeof connected) => {
    if (provider === 'gbp') {
      handleConnectGBP();
      return;
    }

    // For other providers, show coming soon message
    toast.error(`OAuth flow for ${provider.toUpperCase()} will be implemented soon`);
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <p className="text-text-secondary mb-8">
          Loading connection status...
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <p className="text-text-secondary mb-8">
        Connect your accounts so Sponte can manage your local SEO automatically.
      </p>

      <div className="space-y-4">
        {/* Google Business Profile */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">
                Google Business Profile
              </h3>
              <span className="px-3 py-1 bg-accent-red text-white text-xs font-mono font-bold rounded">
                REQUIRED
              </span>
            </div>
            <p className="text-sm text-text-secondary">
              Manage hours, posts, and insights
            </p>
          </div>
          <Button
            type="button"
            variant={connected.gbp ? 'secondary' : 'primary'}
            onClick={() => handleConnect('gbp')}
            className="ml-4"
            disabled={isConnecting}
          >
            {connected.gbp ? '✓ Connected' : 'Connect'}
          </Button>
        </div>

        {/* Google Search Console */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">
                Google Search Console
              </h3>
              <span className="px-3 py-1 bg-accent-red text-white text-xs font-mono font-bold rounded">
                REQUIRED
              </span>
            </div>
            <p className="text-sm text-text-secondary">
              Track keyword rankings and clicks
            </p>
          </div>
          <Button
            type="button"
            variant={connected.gsc ? 'secondary' : 'primary'}
            onClick={() => handleConnect('gsc')}
            className="ml-4"
            disabled={isConnecting}
          >
            {connected.gsc ? '✓ Connected' : 'Connect'}
          </Button>
        </div>

        {/* Google Analytics 4 */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">
                Google Analytics 4
              </h3>
              <span className="px-3 py-1 bg-sage-green text-white text-xs font-mono font-bold rounded">
                OPTIONAL
              </span>
            </div>
            <p className="text-sm text-text-secondary">
              Measure conversions and UTM performance
            </p>
          </div>
          <Button
            type="button"
            variant={connected.ga4 ? 'secondary' : 'primary'}
            onClick={() => handleConnect('ga4')}
            className="ml-4"
            disabled={isConnecting}
          >
            {connected.ga4 ? '✓ Connected' : 'Connect'}
          </Button>
        </div>

        {/* WordPress / CMS */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">WordPress / CMS</h3>
              <span className="px-3 py-1 bg-accent-red text-white text-xs font-mono font-bold rounded">
                REQUIRED
              </span>
            </div>
            <p className="text-sm text-text-secondary">
              Publish blog posts automatically
            </p>
          </div>
          <Button
            type="button"
            variant={connected.wordpress ? 'secondary' : 'primary'}
            onClick={() => handleConnect('wordpress')}
            className="ml-4"
            disabled={isConnecting}
          >
            {connected.wordpress ? '✓ Connected' : 'Connect'}
          </Button>
        </div>

        {/* Meta (Coming Soon) */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center opacity-60">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">
                Meta (Facebook & Instagram)
              </h3>
              <span className="px-3 py-1 bg-accent-yellow text-charcoal text-xs font-mono font-bold rounded">
                V1.1 SOON
              </span>
            </div>
            <p className="text-sm text-text-secondary">Schedule social posts</p>
          </div>
          <Button type="button" variant="secondary" disabled className="ml-4">
            Coming Soon
          </Button>
        </div>

        {/* LinkedIn (Coming Soon) */}
        <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6 flex justify-between items-center opacity-60">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className="font-heading font-bold text-lg">LinkedIn Pages</h3>
              <span className="px-3 py-1 bg-accent-yellow text-charcoal text-xs font-mono font-bold rounded">
                V1.1 SOON
              </span>
            </div>
            <p className="text-sm text-text-secondary">
              Share updates on LinkedIn
            </p>
          </div>
          <Button type="button" variant="secondary" disabled className="ml-4">
            Coming Soon
          </Button>
        </div>
      </div>

      <div className="mt-6 p-4 bg-cream-dark rounded-lg border-2 border-charcoal/20">
        <p className="text-sm text-text-secondary">
          <strong>Note:</strong> DataForSEO keyword research is included in your
          plan. No additional API key needed!
        </p>
      </div>
    </div>
  );
}
