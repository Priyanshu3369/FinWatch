import { useEffect, useState } from "react";
import axios from "../api/axios";

export default function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [suggestion, setSuggestion] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const txRes = await axios.get("/transactions");
      setTransactions(txRes.data.transactions);
      const sugRes = await axios.get("/transactions/suggestions");
      if (sugRes.data.suggestions.length) {
        setSuggestion(sugRes.data.suggestions[0].suggestion);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl mb-4">Your Dashboard</h2>
      {suggestion && <p className="mb-4 p-2 bg-green-100">{suggestion}</p>}
      <table className="w-full border">
        <thead>
          <tr>
            <th>Description</th><th>Amount</th><th>Date</th><th>Fraud?</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(tx => (
            <tr key={tx._id}>
              <td>{tx.description}</td>
              <td>${tx.amount.toFixed(2)}</td>
              <td>{tx.date.split("T")[0]}</td>
              <td>{tx.is_fraud ? "🚩" : "✅"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
