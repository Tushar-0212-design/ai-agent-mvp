import React, { useState } from "react";
import ChatBox from "./components/ChatBox";
import HistoryView from "./components/HistoryView";

function App() {
  const [sessionId, setSessionId] = useState("demo-session");

  const handleSessionChange = (e) => {
    setSessionId(e.target.value);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>🤖 AI Agent Chat</h1>
      <label>
        Session ID:
        <input
          type="text"
          value={sessionId}
          onChange={handleSessionChange}
          style={{ marginLeft: 10 }}
        />
      </label>

      <ChatBox sessionId={sessionId} />
      <HistoryView sessionId={sessionId} />
    </div>
  );
}

export default App;
