import { useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const API = "http://localhost:8000"; // Railway bo‘lsa o‘zgartirasan

function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");

  const [answers, setAnswers] = useState(["", "", "", ""]);
  const [score, setScore] = useState(0);

  const [aiText, setAiText] = useState("");
  const [aiResult, setAiResult] = useState("");

  // ===== AUTH =====
  const register = async () => {
    await axios.post(`${API}/register`, {
      username,
      password,
      role,
    });
    alert("Registered!");
    setPage("login");
  };

  const login = async () => {
    const res = await axios.post(`${API}/login`, {
      username,
      password,
    });
    setToken(res.data.access_token);
    setPage("dashboard");
  };

  // ===== EXAM =====
  const submitExam = async () => {
    const res = await axios.post(
      `${API}/submit`,
      { answers },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setScore(res.data.score);
  };

  // ===== AI =====
  const checkAI = async () => {
    const res = await axios.post(`${API}/ai-check`, {
      text: aiText,
    });
    setAiResult(res.data.response);
  };

  const chartData = [{ name: "Score", value: score }];

  // ===== UI =====
  if (page === "login") {
    return (
      <div style={{ padding: 40 }}>
        <h2>Login</h2>
        <input placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        <br />
        <input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        <br />
        <button onClick={login}>Login</button>
        <button onClick={() => setPage("register")}>Go Register</button>
      </div>
    );
  }

  if (page === "register") {
    return (
      <div style={{ padding: 40 }}>
        <h2>Register</h2>
        <input placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        <br />
        <input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        <br />
        <select onChange={(e) => setRole(e.target.value)}>
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
        </select>
        <br />
        <button onClick={register}>Register</button>
        <button onClick={() => setPage("login")}>Back</button>
      </div>
    );
  }

  if (page === "dashboard") {
    return (
      <div style={{ padding: 40 }}>
        <h1>Dashboard</h1>

        {/* EXAM */}
        <h2>Exam</h2>
        {answers.map((a, i) => (
          <input
            key={i}
            placeholder={`Q${i + 1}`}
            onChange={(e) => {
              const newAns = [...answers];
              newAns[i] = e.target.value;
              setAnswers(newAns);
            }}
          />
        ))}
        <br />
        <button onClick={submitExam}>Submit Exam</button>

        <h3>Score: {score}</h3>

        {/* CHART */}
        <BarChart width={400} height={250} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>

        {/* AI */}
        <h2>AI Check</h2>
        <textarea onChange={(e) => setAiText(e.target.value)} />
        <br />
        <button onClick={checkAI}>Check AI</button>

        <p>{aiResult}</p>

        <button onClick={() => setPage("login")}>Logout</button>
      </div>
    );
  }

  return null;
}

export default App;
