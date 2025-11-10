// Common types used across the application

export type Language = 'ja' | 'en' | 'vi';

export type PropertyType = 'buy' | 'rent' | 'sell';

export type SessionStatus = 'active' | 'completed' | 'expired';

export type BriefStatus = 'draft' | 'in_progress' | 'submitted';

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}

export interface PaginationParams {
  limit?: number;
  offset?: number;
}

export interface PaginationResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}
