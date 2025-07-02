import { useState } from "react";
import axios from "../api/axios";

export default function Upload() {
  const [file, setFile] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/transactions/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          // ✅ If your axios instance sets Content-Type, this overrides it.
        },
      });
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Upload failed.");
    }
  };

  return (
    <form onSubmit={handleUpload} className="max-w-md mx-auto p-4">
      <h2 className="text-2xl mb-4">Upload Bank CSV</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="block mb-2"
      />
      <button
        type="submit"
        className="bg-purple-600 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
    </form>
  );
}
