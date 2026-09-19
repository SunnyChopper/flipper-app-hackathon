import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/auth/AuthProvider";

export function RequireAuth() {
  const { configured, loading, session } = useAuth();
  const location = useLocation();

  if (!configured) return <Outlet />;
  if (loading) {
    return (
      <div className="grid min-h-screen place-items-center bg-background text-sm text-muted">
        Checking session…
      </div>
    );
  }
  if (!session) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return <Outlet />;
}
