import { useState } from "react";
import axios from "axios";

function App() {
  const [answers, setAnswers] = useState(["", "", "", ""]);
  const [result, setResult] = useState(null);

  const handleChange = (i, val) => {
    const newAns = [...answers];
    newAns[i] = val;
    setAnswers(newAns);
  };

  const submit = async () => {
    const res = await axios.post("http://127.0.0.1:8000/submit", {
      answers
    });
    setResult(res.data);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Exam System</h1>

      {answers.map((a, i) => (
        <div key={i}>
          <input
            placeholder={`Savol ${i+1}`}
            onChange={(e) => handleChange(i, e.target.value)}
          />
        </div>
      ))}

      <button onClick={submit}>Yuborish</button>

      {result && (
        <div>
          <h2>Score: {result.score}/{result.total}</h2>
          <h3>{result.percentage}%</h3>
        </div>
      )}
    </div>
  );
}

export default App;
