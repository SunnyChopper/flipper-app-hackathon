import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import type { ReactNode } from "react";
import { AuthProvider } from "@/auth/AuthProvider";
import { useHydrateSavedDeals } from "@/hooks/useSavedDeals";
import { useToastStore } from "@/store/toastStore";

function AppEffects({ children }: { children: ReactNode }) {
  const message = useToastStore((state) => state.message);
  useHydrateSavedDeals();

  return (
    <TooltipPrimitive.Provider delayDuration={150}>
      {children}
      {message ? (
        <div className="fixed bottom-5 right-5 z-50 rounded-lg border border-border bg-white px-3 py-2 text-sm shadow-card-hover">
          {message}
        </div>
      ) : null}
    </TooltipPrimitive.Provider>
  );
}

export function Providers({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <AppEffects>{children}</AppEffects>
    </AuthProvider>
  );
}
