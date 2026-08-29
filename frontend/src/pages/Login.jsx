import { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../services/authService";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("Logging in...");

    try {
      await authService.login({
        username,
        password,
      });

      setMessage("Login successful!");

      navigate("/dashboard");
    } catch (error) {
      console.error("LOGIN FAILED:", error);
      console.error("ERROR MESSAGE:", error.message);
      console.error("ERROR CODE:", error.code);
      console.error("ERROR RESPONSE:", error.response);

      setMessage(
        `ERROR: ${error.code || ""} ${error.message || "Unknown error"}`
      );
    }
  };

  return (
    <div>
      <h1>Capstone Login</h1>

      <form onSubmit={handleLogin}>
        <div>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit">Login</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default Login;