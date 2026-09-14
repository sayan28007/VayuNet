export type EvidenceType = "sensor" | "citizen" | "image";
export interface ImageEvidence {
  evidence_id: string;
  evidence_type: EvidenceType;
  latitude: number;
  longitude: number;
  confidence: number;
  filename?: string;
  visible_smoke: number;
  dust: number;
  fire: number;
  haze: number;
  detected_categories: string[];
  is_synthetic: boolean;
}
