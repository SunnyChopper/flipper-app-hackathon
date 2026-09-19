import { NavLink } from "react-router-dom";
import { cn } from "@/lib/cn";

export function MobileNav() {
  return (
    <div className="flex items-center gap-5 text-sm md:hidden">
      <NavLink to="/radar" className={({ isActive }) => cn(isActive ? "text-white" : "text-[#cbd5e1]")}>
        Radar
      </NavLink>
      <NavLink to="/saved" className={({ isActive }) => cn(isActive ? "text-white" : "text-[#cbd5e1]")}>
        Saved
      </NavLink>
    </div>
  );
}
