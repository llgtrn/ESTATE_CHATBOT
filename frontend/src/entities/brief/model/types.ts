import type { PropertyType, BriefStatus } from '@/shared/types/common';

export interface Brief {
  brief_id: string;
  session_id: string;
  property_type: PropertyType;
  status: BriefStatus;
  location?: string;
  budget_min?: number;
  budget_max?: number;
  rooms?: string;
  area_min?: number;
  area_max?: number;
  data?: Record<string, unknown>;
  extracted_entities?: Record<string, unknown>;
  completeness_score?: number;
  lead_score?: number;
  created_at: string;
  updated_at: string;
  submitted_at?: string;
}

export interface UpdateBriefRequest {
  status?: BriefStatus;
  data?: Record<string, unknown>;
}

export interface SubmitBriefResponse {
  brief_id: string;
  status: BriefStatus;
  submitted_at: string;
}
