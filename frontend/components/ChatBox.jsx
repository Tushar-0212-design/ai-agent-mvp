import React, { useState } from "react";
import axios from "axios";

const ChatBox = ({ sessionId }) => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    try {
      const res = await axios.post("http://localhost:8000/chat/", {
        session_id: sessionId,
        message: input,
      });
      setResponse(res.data.reply);
    } catch (error) {
      setResponse("Error getting response.");
    }
  };

  return (
    <div>
      <h2>Chat</h2>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={handleSend}>Send</button>
      <p><strong>AI:</strong> {response}</p>
    </div>
  );
};

export default ChatBox;
