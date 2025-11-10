import { apiClient } from '@/shared/api/client';
import type {
  SendMessageRequest,
  SendMessageResponse,
  GetMessagesResponse,
} from '../model/types';

export const messageApi = {
  /**
   * Send a message in a session
   */
  async sendMessage(
    sessionId: string,
    data: SendMessageRequest
  ): Promise<SendMessageResponse> {
    const response = await apiClient.post<SendMessageResponse>(
      `/sessions/${sessionId}/messages`,
      data
    );
    return response.data;
  },

  /**
   * Get messages for a session
   */
  async getMessages(
    sessionId: string,
    params?: { limit?: number; offset?: number }
  ): Promise<GetMessagesResponse> {
    const response = await apiClient.get<GetMessagesResponse>(
      `/sessions/${sessionId}/messages`,
      { params }
    );
    return response.data;
  },
};
