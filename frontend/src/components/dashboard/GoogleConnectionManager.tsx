'use client';

import { Button } from '@/components/ui/Button';
import { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-hot-toast';
import { useAuth } from '@clerk/nextjs';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface GoogleConnectionManagerProps {
  locationId: string;
}

interface ConnectionStatus {
  connected: boolean;
  email?: string;
}

export function GoogleConnectionManager({ locationId }: GoogleConnectionManagerProps) {
  const [status, setStatus] = useState<ConnectionStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isConnecting, setIsConnecting] = useState(false);
  const { getToken } = useAuth();

  const fetchStatus = useCallback(async () => {
    setIsLoading(true);
    try {
      const token = await getToken();
      if (!token) {
        throw new Error('Authentication token not found.');
      }

      const response = await fetch(`${API_URL}/api/oauth/google/status/${locationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch status: ${response.statusText}`);
      }

      const data: ConnectionStatus = await response.json();
      setStatus(data);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred.';
      toast.error(`Error fetching connection status: ${errorMessage}`);
      setStatus({ connected: false });
    } finally {
      setIsLoading(false);
    }
  }, [locationId, getToken]);

  useEffect(() => {
    if (locationId) {
      fetchStatus();
    }
  }, [locationId, fetchStatus]);

  const handleConnect = () => {
    setIsConnecting(true);
    window.location.href = `${API_URL}/api/oauth/google/connect?location_id=${locationId}`;
  };

  const handleDisconnect = async () => {
    setIsLoading(true);
    try {
      const token = await getToken();
      if (!token) {
        throw new Error('Authentication token not found.');
      }

      const response = await fetch(`${API_URL}/api/oauth/google/disconnect/${locationId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to disconnect: ${response.statusText}`);
      }

      toast.success('Successfully disconnected Google account.');
      await fetchStatus(); // Refresh status
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred.';
      toast.error(`Error disconnecting account: ${errorMessage}`);
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    if (isLoading) {
      return <p className="text-sm text-text-secondary">Loading connection status...</p>;
    }

    if (status?.connected) {
      return (
        <>
          <div className="flex-1">
            <h3 className="font-heading font-bold text-lg">Google Business Profile</h3>
            <p className="text-sm text-text-secondary">
              Connected as: <span className="font-bold text-charcoal">{status.email || 'N/A'}</span>
            </p>
          </div>
          <Button
            type="button"
            variant="secondary"
            onClick={handleDisconnect}
            className="ml-4"
            isLoading={isLoading}
          >
            Disconnect
          </Button>
        </>
      );
    }

    return (
      <>
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
          variant="primary"
          onClick={handleConnect}
          className="ml-4"
          isLoading={isConnecting}
        >
          Connect
        </Button>
      </>
    );
  };

  return (
    <div className="bg-white border-2 border-charcoal rounded-lg p-6 flex justify-between items-center shadow-brutalist-sm">
      {renderContent()}
    </div>
  );
}
