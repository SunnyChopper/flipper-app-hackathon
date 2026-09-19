import { Zap } from "lucide-react";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/cn";

const links = [
  { to: "/radar", label: "Radar" },
  { to: "/saved", label: "Saved" },
];

export function AppHeader() {
  return (
    <header className="sticky top-0 z-40 h-16 bg-nav text-white">
      <div className="mx-auto grid h-full max-w-[1320px] grid-cols-2 items-center px-4 md:grid-cols-3 md:px-6">
        <NavLink to="/radar" className="flex items-center gap-2.5 justify-self-start">
          <span className="grid h-6 w-6 place-items-center rounded-md bg-primary">
            <span className="h-2.5 w-2.5 rotate-45 rounded-[2px] bg-white" />
          </span>
          <span className="text-[17px] font-bold tracking-tight">DealSniper</span>
        </NavLink>

        <nav className="flex items-center justify-end gap-6 md:justify-center">
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
        </nav>

        <p className="hidden items-center justify-self-end gap-1.5 text-xs text-[#94a3b8] md:flex">
          <Zap className="h-3.5 w-3.5 text-primary" />
          Find deals. Flip smarter.
        </p>
      </div>
    </header>
  );
}
