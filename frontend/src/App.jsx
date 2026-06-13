import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import HomePage from "./pages/HomePage";
import NewsDetailPage from "./pages/NewsDetailPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={{ padding: "12px 24px", borderBottom: "1px solid #ddd", display: "flex", gap: 16, alignItems: "center" }}>
      <Link to="/" style={{ fontWeight: "bold", textDecoration: "none" }}>Haber Öneri</Link>
      <span style={{ flex: 1 }} />
      {isAuthenticated ? (
        <button onClick={handleLogout} style={{ cursor: "pointer" }}>Çıkış</button>
      ) : (
        <>
          <Link to="/login">Giriş</Link>
          <Link to="/register">Kayıt Ol</Link>
        </>
      )}
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/news/:id" element={<NewsDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
