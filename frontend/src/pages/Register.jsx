import { useState } from "react";
import axios from "../api/axios";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post("/auth/register", { email, password });
    alert("Registered ✅ Now login!");
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-4">
      <h2 className="text-2xl mb-4">Register</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} className="block mb-2 border p-2 w-full"/>
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} className="block mb-2 border p-2 w-full"/>
      <button type="submit" className="bg-blue-600 text-white px-4 py-2">Register</button>
    </form>
  );
}
