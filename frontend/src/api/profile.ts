import { apiFetch } from "./apiClient";
import type { Profile, RepairSkillListResponse, UpdateProfileRequest } from "@/types/profile";

export async function getProfile(): Promise<Profile> {
  return apiFetch<Profile>("/api/v1/profile");
}

export async function updateProfile(payload: UpdateProfileRequest): Promise<Profile> {
  return apiFetch<Profile>("/api/v1/profile", {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function getRepairSkills(): Promise<RepairSkillListResponse> {
  return apiFetch<RepairSkillListResponse>("/api/v1/repair-skills");
}
