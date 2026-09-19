import { CircleCheck, TriangleAlert } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { RepairSkillSummary } from "@/types/catalog";

export function RequiredSkillsPanel({ skills }: { skills: RepairSkillSummary[] }) {
  return (
    <Card className="p-5">
      <h3 className="text-lg font-semibold tracking-tight">Required Skills</h3>
      {skills.length ? (
        <ul className="mt-3 space-y-2.5">
          {skills.map((skill) => (
            <li key={skill.slug} className="flex items-start gap-2 text-[13px] text-foreground">
              {skill.userHasSkill ? (
                <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              ) : (
                <TriangleAlert className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
              )}
              <div>
                <div className="font-medium">{skill.displayName}</div>
                <div className="text-muted">
                  {skill.userHasSkill ? "You have this skill" : "Skill not enabled"}
                </div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm text-muted">No repair skills required.</p>
      )}
    </Card>
  );
}
