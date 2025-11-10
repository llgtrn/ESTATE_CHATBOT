import { apiClient } from '@/shared/api/client';
import type {
  GlossaryTerm,
  SearchGlossaryParams,
  SearchGlossaryResponse,
} from '../model/types';

export const glossaryApi = {
  /**
   * Search glossary terms
   */
  async searchTerms(params: SearchGlossaryParams): Promise<SearchGlossaryResponse> {
    const response = await apiClient.get<SearchGlossaryResponse>('/glossary/search', { params });
    return response.data;
  },

  /**
   * Get term by ID
   */
  async getTerm(termId: string): Promise<GlossaryTerm> {
    const response = await apiClient.get<GlossaryTerm>(`/glossary/terms/${termId}`);
    return response.data;
  },
};
