'use client';

import { useState } from 'react';
import { toast } from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function CreateTestLocation() {
  const [locationId, setLocationId] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const createTestLocation = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/onboarding/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          // Test data for onboarding
          businessProfile: {
            businessName: 'Test Business for GBP OAuth',
            legalBusinessName: 'Test Business LLC',
            address: '123 Test Street',
            city: 'Test City',
            state: 'CA',
            zipCode: '12345',
            phone: '555-0123',
            website: 'https://testbusiness.com',
            email: 'test@testbusiness.com',
            industry: 'Software',
            description: 'A test business for OAuth testing',
            yearEstablished: 2024,
            googleBusinessProfileUrl: '',
          },
          connectAccounts: {
            googleBusinessProfile: false,
            googleSearchConsole: false,
            googleAnalytics: false,
            wordpress: false,
            meta: false,
            linkedin: false,
          },
          contentBrand: {
            brandTone: 'professional',
            forbiddenWords: [],
            blogCadence: 'weekly',
            gbpCadence: 'weekly',
            socialCadence: 'weekly',
          },
          autonomyControl: {
            globalAutonomy: 'draft',
            blackoutDates: [],
          },
          goalsReporting: {
            primaryGoal: 'calls',
            weeklyReport: true,
            monthlyReport: true,
            reportEmails: 'test@testbusiness.com',
            utmCampaign: 'test-campaign',
          },
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
      }

      const data = await response.json();
      setLocationId(data.location_id);

      // Copy to clipboard
      navigator.clipboard.writeText(data.location_id);
      toast.success('Location created! ID copied to clipboard');

    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to create test location');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cream py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-8 shadow-brutalist">
          <h1 className="font-heading text-3xl font-bold text-charcoal mb-4">
            Create Test Location
          </h1>

          <p className="text-text-secondary mb-6">
            This will create a test business location in your database that you can use for testing GBP OAuth.
          </p>

          <button
            onClick={createTestLocation}
            disabled={loading}
            className="w-full px-6 py-3 bg-orange-fire text-white border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-orange-hover transition-colors disabled:opacity-50 shadow-brutalist-sm mb-6"
          >
            {loading ? 'Creating...' : 'Create Test Location'}
          </button>

          {locationId && (
            <div className="bg-green-50 border-2 border-green-500 rounded-brutalist p-4">
              <h3 className="font-heading font-bold text-charcoal mb-2">
                ✅ Location Created Successfully!
              </h3>
              <p className="text-sm text-text-secondary mb-2">
                Location ID (copied to clipboard):
              </p>
              <code className="block bg-charcoal text-white p-3 rounded font-mono text-sm break-all">
                {locationId}
              </code>
              <p className="text-sm text-text-secondary mt-4">
                Now you can:
              </p>
              <ol className="list-decimal list-inside text-sm text-text-secondary mt-2 space-y-1">
                <li>Go to <a href="/test-gbp-oauth" className="text-orange-fire underline">Test GBP OAuth</a></li>
                <li>Paste this Location ID</li>
                <li>Click "Connect Google Business Profile"</li>
              </ol>
            </div>
          )}

          <div className="mt-6 p-4 bg-yellow-50 border-2 border-yellow-400 rounded-brutalist">
            <h3 className="font-heading font-bold text-charcoal mb-2">
              ℹ️ What is a Location ID?
            </h3>
            <p className="text-sm text-text-secondary">
              A Location ID is a unique identifier (UUID) for each business in the system.
              It links your business data with external services like Google Business Profile.
              When you connect GBP, the system stores which GBP location belongs to this Location ID.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}