export type Persona = "restorer" | "harvester";

export interface RepairSkill {
  slug: string;
  displayName: string;
  category: string;
}

export interface Profile {
  id: string;
  persona: Persona;
  minProfitMarginUsd: number;
  minRoiPercent: number;
  skills: RepairSkill[];
}

export interface UpdateProfileRequest {
  persona: Persona;
  minProfitMarginUsd: number;
  minRoiPercent: number;
  skillSlugs: string[];
}

export interface RepairSkillListResponse {
  items: RepairSkill[];
}
