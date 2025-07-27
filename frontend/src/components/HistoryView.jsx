import React, { useEffect, useState } from "react";
import axios from "axios";

const HistoryView = ({ sessionId }) => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8003/history/${sessionId}`
        );
        setMessages(res.data);
      } catch (err) {
        console.error("Error fetching history", err);
      }
    };

    fetchHistory();
  }, [sessionId]);

  return (
    <div>
      <h2>Chat History</h2>
      <ul>
        {messages.map((msg, idx) => (
          <li key={idx}>
            <strong>{msg.role}:</strong> {msg.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryView;
