import "./App.css";
import React, { useEffect } from "react";
import { useState } from "react";
import { io } from "socket.io-client";

function App() {
  const [temp, setTemp] = useState(0.0);

  useEffect(() => {
    const socket = io("localhost:5000/", {
      transports: ["websocket"],
      cors: {
        origin: "http://localhost:3000/",
      },
    });

    socket.on("data", (data) => {
      setTemp(data.data);
    });

    return function cleanup() {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h3>Current temp 🌡️</h3>
        <br />
        <h1>{temp}°C</h1>
      </header>
    </div>
  );
}

export default App;
