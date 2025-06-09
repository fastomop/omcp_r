import express from "express";
import { loadPyodide } from "pyodide";

let pyodideReadyPromise = loadPyodide();

const app = express();
app.use(express.json());

app.post("/run", async (req, res) => {
  const code = req.body.code;
  try {
    const pyodide = await pyodideReadyPromise;
    let result, error = null;
    try {
      result = pyodide.runPython(code);
    } catch (err) {
      error = err.toString();
    }
    res.json({ result, error });
  } catch (e) {
    res.status(500).json({ error: e.toString() });
  }
});

app.listen(8000, () => console.log("Pyodide server running on port 8000")); 