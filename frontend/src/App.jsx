import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-blue-700 text-white px-4 py-3 flex justify-between">
          <h1 className="font-bold text-xl">FinWatch</h1>
          <div className="space-x-4">
            <a href="/register" className="hover:underline">Register</a>
            <a href="/login" className="hover:underline">Login</a>
            <a href="/upload" className="hover:underline">Upload</a>
            <a href="/dashboard" className="hover:underline">Dashboard</a>
          </div>
        </nav>

        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/upload" 
            element={
              <ProtectedRoute>
                <Upload />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}
