import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

// Public Pages
import Home from "@/pages/public/home";
import NotFound from "@/pages/NotFound";
import Login from "@/pages/public/login";
import About from "@/pages/public/about";
import AccountActivation from "@/pages/public/accountActivation";
import TEST from "./pages/test";

export default function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* ===============Public Routes=============== */}
      <Route path="/" element={<Home />} />
      <Route path="*" element={<NotFound />} />
      <Route
        path="/login"
        element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
        }
      />
      <Route path="/about-us" element={<About />} />
      <Route path="/activate" element={<AccountActivation />} />





      {/* ===============Private Routes=============== */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <TEST />
          </ProtectedRoute>
        }
      />

      {/* <Route path="/profile/:id" element={<Profile />} /> */}
    </Routes>
  );
}
