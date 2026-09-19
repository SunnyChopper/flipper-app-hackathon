import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { AuthPage } from "./pages/AuthPage";
import { DealDetailPage } from "./pages/DealDetailPage";
import { SavedSearchesPage } from "./pages/SavedSearchesPage";
import { SearchPage } from "./pages/SearchPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<SearchPage />} />
        <Route path="/deals/:dealId" element={<DealDetailPage />} />
        <Route path="/saved" element={<SavedSearchesPage />} />
        <Route path="/login" element={<AuthPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
