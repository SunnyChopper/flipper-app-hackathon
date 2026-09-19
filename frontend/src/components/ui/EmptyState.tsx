import type { ReactNode } from "react";
import { Button } from "./Button";

type EmptyStateProps = {
  icon: ReactNode;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function EmptyState({ icon, title, description, actionLabel, onAction }: EmptyStateProps) {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center px-6 py-16 text-center">
      <div className="mb-4 text-subtle">{icon}</div>
      <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
      <p className="mt-2 text-sm text-muted">{description}</p>
      {actionLabel && onAction ? (
        <Button className="mt-5" onClick={onAction}>
          {actionLabel}
        </Button>
      ) : null}
    </div>
  );
}
