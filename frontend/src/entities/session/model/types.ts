import type { Language, SessionStatus } from '@/shared/types/common';

export interface Session {
  session_id: string;
  user_id?: string;
  status: SessionStatus;
  language: Language;
  turn_count: number;
  token_count: number;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  expires_at?: string;
}

export interface CreateSessionRequest {
  language?: Language;
  user_id?: string;
  metadata?: Record<string, unknown>;
}

export interface CreateSessionResponse {
  session_id: string;
  status: SessionStatus;
  language: Language;
  created_at: string;
  expires_at?: string;
}
