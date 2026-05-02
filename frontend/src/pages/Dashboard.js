import { useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis } from "recharts";

export default function Dashboard() {
  const [score, setScore] = useState(0);

  const sendExam = async () => {
    const res = await axios.post("http://localhost:8000/submit", {
      answers: ["A","C","B","D"]
    },{
      headers:{Authorization:"Bearer TOKEN"}
    });

    setScore(res.data.score);
  };

  const data = [{name:"Score", value:score}];

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <button className="bg-blue-500 text-white p-2" onClick={sendExam}>
        Submit Exam
      </button>

      <BarChart width={300} height={200} data={data}>
        <XAxis dataKey="name"/>
        <YAxis/>
        <Bar dataKey="value"/>
      </BarChart>
    </div>
  );
}
