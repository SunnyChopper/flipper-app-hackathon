import { LogOut } from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/AuthProvider";
import { cn } from "@/lib/cn";
import { useApiHealth } from "@/hooks/useApiHealth";
import { useSavedStore } from "@/store/savedStore";

const links = [
  { to: "/radar", label: "Radar" },
  { to: "/saved", label: "Saved" },
];

export function AppHeader() {
  const { health, error, loading } = useApiHealth();
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const apiLabel = loading ? "Checking API…" : health?.status === "ok" ? "API connected" : "API offline";

  async function onSignOut() {
    try {
      await signOut();
    } finally {
      useSavedStore.getState().replace([]);
      navigate("/login");
    }
  }

  return (
    <header className="sticky top-0 z-40 h-16 bg-nav text-white">
      <div className="mx-auto grid h-full max-w-[1320px] grid-cols-2 items-center px-4 md:grid-cols-3 md:px-6">
        <div className="flex items-center gap-3 justify-self-start">
          <NavLink to="/radar" className="flex items-center gap-2.5">
            <span className="grid h-6 w-6 place-items-center rounded-md bg-primary">
              <span className="h-2.5 w-2.5 rotate-45 rounded-[2px] bg-white" />
            </span>
            <span className="text-[17px] font-bold tracking-tight">DealSniper</span>
          </NavLink>
          <span
            title={error ?? health?.service ?? "FastAPI /health"}
            className={cn(
              "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px]",
              loading && "bg-white/5 text-[#94a3b8]",
              !loading && health?.status === "ok" && "bg-primary/15 text-[#6ee7b7]",
              !loading && !health && "bg-danger/15 text-[#fca5a5]",
            )}
          >
            <span
              className={cn(
                "h-1.5 w-1.5 rounded-full",
                loading && "bg-[#94a3b8]",
                !loading && health?.status === "ok" && "bg-primary",
                !loading && !health && "bg-danger",
              )}
            />
            {apiLabel}
          </span>
        </div>

        <nav className="flex items-center justify-end gap-4 md:justify-center md:gap-6">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                cn(
                  "relative py-5 text-sm transition",
                  isActive ? "font-medium text-white" : "text-[#cbd5e1] hover:text-white",
                )
              }
            >
              {({ isActive }) => (
                <>
                  {link.label}
                  {isActive ? <span className="absolute inset-x-0 bottom-0 h-0.5 bg-primary" /> : null}
                </>
              )}
            </NavLink>
          ))}
          {user ? (
            <button
              type="button"
              onClick={() => void onSignOut()}
              className="text-sm text-[#cbd5e1] md:hidden"
            >
              Sign out
            </button>
          ) : (
            <NavLink to="/login" className="text-sm text-[#cbd5e1] md:hidden">
              Sign in
            </NavLink>
          )}
        </nav>

        <div className="hidden items-center justify-self-end gap-3 md:flex">
          {user ? (
            <>
              <span className="max-w-[180px] truncate text-xs text-[#94a3b8]" title={user.email ?? undefined}>
                {user.email}
              </span>
              <button
                type="button"
                onClick={() => void onSignOut()}
                className="inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-[#cbd5e1] transition hover:bg-white/5 hover:text-white"
              >
                <LogOut className="h-3.5 w-3.5" />
                Sign out
              </button>
            </>
          ) : (
            <NavLink
              to="/login"
              className="rounded-md px-2.5 py-1 text-xs font-medium text-white transition hover:bg-white/5"
            >
              Sign in
            </NavLink>
          )}
        </div>
      </div>
    </header>
  );
}
