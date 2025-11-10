import type { Language } from '@/shared/types/common';

export interface Message {
  message_id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  language: Language;
  intent?: string;
  confidence?: number;
  entities?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  created_at: string;
}

export interface SendMessageRequest {
  message: string;
  language?: Language;
}

export interface SendMessageResponse {
  message_id: string;
  session_id: string;
  response: string;
  intent?: string;
  confidence?: number;
  entities?: Record<string, unknown>;
  language: Language;
}

export interface GetMessagesResponse {
  session_id: string;
  messages: Message[];
  total: number;
  limit?: number;
  offset?: number;
}
