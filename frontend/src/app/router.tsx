import { Navigate, Outlet, Route, Routes, useLocation } from "react-router-dom";
import { useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { RequireAuth } from "@/auth/RequireAuth";
import { AppHeader } from "@/components/layout/AppHeader";
import { LoginPage } from "@/pages/LoginPage";
import { RadarPage } from "@/pages/RadarPage";
import { OpportunityPage } from "@/pages/OpportunityPage";
import { SavedPage } from "@/pages/SavedPage";
import { NotFoundPage } from "@/pages/NotFoundPage";

function AppShell() {
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);
  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
        >
          <Outlet />
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<RequireAuth />}>
        <Route element={<AppShell />}>
          <Route path="/" element={<Navigate to="/radar" replace />} />
          <Route path="/radar" element={<RadarPage />} />
          <Route path="/opportunities/:id" element={<OpportunityPage />} />
          <Route path="/saved" element={<SavedPage />} />
        </Route>
      </Route>
      <Route element={<AppShell />}>
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
