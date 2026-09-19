export function scoreTone(score: number): "high" | "mid" | "low" {
  if (score >= 90) return "high";
  if (score >= 75) return "mid";
  return "low";
}

export function scoreLabel(score: number): string {
  if (score >= 90) return "High opportunity";
  if (score >= 75) return "Solid opportunity";
  return "Review carefully";
}
