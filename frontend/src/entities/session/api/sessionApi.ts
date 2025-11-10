import { apiClient } from '@/shared/api/client';
import type { Session, CreateSessionRequest, CreateSessionResponse } from '../model/types';

export const sessionApi = {
  /**
   * Create a new session
   */
  async createSession(data?: CreateSessionRequest): Promise<CreateSessionResponse> {
    const response = await apiClient.post<CreateSessionResponse>('/sessions', data);
    return response.data;
  },

  /**
   * Get session by ID
   */
  async getSession(sessionId: string): Promise<Session> {
    const response = await apiClient.get<Session>(`/sessions/${sessionId}`);
    return response.data;
  },

  /**
   * Delete session
   */
  async deleteSession(sessionId: string): Promise<void> {
    await apiClient.delete(`/sessions/${sessionId}`);
  },
};
