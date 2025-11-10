import type { Language } from '@/shared/types/common';

export interface GlossaryTerm {
  term_id: string;
  term: string;
  language: Language;
  translation: string;
  explanation: string;
  category?: string;
  synonyms?: string[];
  examples?: string[];
  usage_count?: number;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface SearchGlossaryParams {
  query: string;
  language?: Language;
  limit?: number;
}

export interface SearchGlossaryResponse {
  query: string;
  language: Language;
  results: GlossaryTerm[];
  total: number;
}
