import { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post("/auth/login", { email, password });
    localStorage.setItem("token", res.data.access_token);
    navigate("/dashboard");
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-4">
      <h2 className="text-2xl mb-4">Login</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} className="block mb-2 border p-2 w-full"/>
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} className="block mb-2 border p-2 w-full"/>
      <button type="submit" className="bg-green-600 text-white px-4 py-2">Login</button>
    </form>
  );
}
