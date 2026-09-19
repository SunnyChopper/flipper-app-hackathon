import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function Layout() {
  const { session, enabled } = useAuth();

  return (
    <div className="shell">
      <header className="topbar">
        <NavLink to="/" className="brand">
          <strong className="serif">Deal Sniper</strong>
          <small>flip radar</small>
        </NavLink>
        <nav>
          <NavLink to="/" end>
            Feed
          </NavLink>
          <NavLink to="/saved">Saved</NavLink>
          <NavLink to="/login">{enabled && session ? "Account" : "Sign in"}</NavLink>
        </nav>
      </header>
      <Outlet />
    </div>
  );
}
