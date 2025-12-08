'use client';

import { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-hot-toast';
import {
  getGbpDrafts,
  approveAgentOutput,
  rejectAgentOutput,
  updateAgentOutput,
} from '@/lib/api/agents';
import type { GbpDraft } from '@/types/api';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';

interface DraftApprovalManagerProps {
  locationId: string;
}

export function DraftApprovalManager({ locationId }: DraftApprovalManagerProps) {
  const [drafts, setDrafts] = useState<GbpDraft[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [editingDraftId, setEditingDraftId] = useState<string | null>(null);
  const [editedContent, setEditedContent] = useState('');

  const fetchDrafts = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedDrafts = await getGbpDrafts(locationId);
      setDrafts(fetchedDrafts);
    } catch {
      setError('Failed to load drafts. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [locationId]);

  useEffect(() => {
    if (locationId) {
      fetchDrafts();
    }
  }, [locationId, fetchDrafts]);

  const handleApprove = async (outputId: string) => {
    try {
      await approveAgentOutput(outputId);
      toast.success('Draft approved and will be posted shortly.');
      fetchDrafts(); // Refresh list
    } catch {
      // Error is already handled by the API client toast
    }
  };

  const handleReject = async (outputId: string) => {
    try {
      // For now, using a generic rejection reason
      await rejectAgentOutput(outputId, 'Rejected by user');
      toast.success('Draft rejected.');
      fetchDrafts(); // Refresh list
    } catch {
       // Error is already handled by the API client toast
    }
  };

  const handleEdit = (draft: GbpDraft) => {
    setEditingDraftId(draft.id);
    setEditedContent(draft.content);
  };

  const handleCancelEdit = () => {
    setEditingDraftId(null);
    setEditedContent('');
  };

  const handleSaveEdit = async (draft: GbpDraft) => {
    if (!editingDraftId) return;

    try {
      await updateAgentOutput(editingDraftId, editedContent, draft.call_to_action);
      toast.success('Draft updated successfully.');
      setEditingDraftId(null);
      fetchDrafts(); // Refresh list
    } catch {
      // Error is already handled by the API client toast
    }
  };

  if (isLoading) {
    return <p>Loading drafts...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  if (drafts.length === 0) {
    return (
      <div className="bg-white border-2 border-charcoal rounded-lg p-6 shadow-brutalist-sm">
        <h2 className="font-display text-3xl text-charcoal mb-4">Pending Drafts</h2>
        <p className="text-text-secondary">No pending drafts to approve. The agent will generate new ones soon!</p>
      </div>
    );
  }

  return (
    <div className="bg-white border-2 border-charcoal rounded-lg p-6 shadow-brutalist-sm">
      <h2 className="font-display text-3xl text-charcoal mb-4">Pending Drafts</h2>
      <div className="space-y-4">
        {drafts.map((draft) => (
          <div key={draft.id} className="border border-charcoal/20 rounded-lg p-4">
            {editingDraftId === draft.id ? (
              <div className="space-y-4">
                <Textarea
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  rows={5}
                />
                <div className="flex gap-2">
                  <Button onClick={() => handleSaveEdit(draft)}>Save</Button>
                  <Button variant="secondary" onClick={handleCancelEdit}>Cancel</Button>
                </div>
              </div>
            ) : (
              <div>
                <p className="whitespace-pre-wrap">{draft.content}</p>
                <div className="flex items-center justify-between mt-4">
                    <span className="text-xs font-mono bg-cream-dark px-2 py-1 rounded">
                        CTA: {draft.call_to_action}
                    </span>
                    <div className="flex gap-2">
                        <Button size="sm" onClick={() => handleApprove(draft.id)}>Approve</Button>
                        <Button size="sm" variant="secondary" onClick={() => handleEdit(draft)}>Edit</Button>
                        <Button size="sm" variant="secondary" className="text-red-500" onClick={() => handleReject(draft.id)}>Reject</Button>
                    </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
