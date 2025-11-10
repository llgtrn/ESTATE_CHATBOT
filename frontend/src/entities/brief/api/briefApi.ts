import { apiClient } from '@/shared/api/client';
import type { Brief, UpdateBriefRequest, SubmitBriefResponse } from '../model/types';

export const briefApi = {
  /**
   * Get brief by ID
   */
  async getBrief(briefId: string): Promise<Brief> {
    const response = await apiClient.get<Brief>(`/briefs/${briefId}`);
    return response.data;
  },

  /**
   * Update brief
   */
  async updateBrief(briefId: string, data: UpdateBriefRequest): Promise<Brief> {
    const response = await apiClient.patch<Brief>(`/briefs/${briefId}`, data);
    return response.data;
  },

  /**
   * Submit brief
   */
  async submitBrief(briefId: string): Promise<SubmitBriefResponse> {
    const response = await apiClient.post<SubmitBriefResponse>(`/briefs/${briefId}/submit`);
    return response.data;
  },
};
