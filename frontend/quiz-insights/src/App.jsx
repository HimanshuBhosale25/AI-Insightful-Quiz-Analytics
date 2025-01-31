import React, { useState } from "react";
import axios from "axios";
import { marked } from "marked";  // Importing marked library
import './App.css';  // Importing the external CSS file

const App = () => {
  const [file, setFile] = useState(null);
  const [insights, setInsights] = useState(null);
  const [charts, setCharts] = useState({
    scoreProgression: "",
    scoreDistribution: "",
    scoreTrend: "",
    scoreRange: "",
  });
  const [loading, setLoading] = useState(false);  // Track loading state

  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
    setLoading(true);  // Set loading to true

    const formData = new FormData();
    formData.append("file", uploadedFile);

    try {
      const response = await axios.post("http://localhost:8000/process_data/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const data = response.data;
      setInsights(data.natural_response);  // Assuming it's raw Markdown
      setCharts({
        scoreProgression: data.score_progression_chart,
        scoreDistribution: data.score_distribution_chart,
        scoreTrend: data.score_trend_chart,
        scoreRange: data.score_range_pie_chart,
        mistakeCorrectionHeatmap: data.mistake_correction_heatmap,
        scoreImprovement: data.score_improvement_plot
      });
    } catch (error) {
      console.error("Error uploading file", error);
    } finally {
      setLoading(false);  // Stop loading when done
    }
  };

  return (
    <div className="app-container">
      <h1>Student Quiz Performance Insights</h1>

      <div className="file-upload">
        <label className="custom-file-upload">
          <span className="upload-icon">📁</span> Choose File
          <input type="file" onChange={handleFileUpload} accept=".json" />
        </label>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          Loading...
        </div>
      )}

      {insights && !loading && (
        <div className="insights-container">
          <h2>Quiz Data Analysis:</h2>
          <div
            className="insights-content"
            dangerouslySetInnerHTML={{
              __html: marked(insights),  // Convert Markdown to HTML
            }}
          />
        </div>
      )}

      {charts.scoreProgression && (
        <div className="chart-container">
          <h2>Score Progression by Topic</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.scoreProgression}`}
            alt="Score Progression"
          />
        </div>
      )}

      {charts.scoreDistribution && (
        <div className="chart-container">
          <h2>Score Distribution per Topic</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.scoreDistribution}`}
            alt="Score Distribution"
          />
        </div>
      )}

      {charts.scoreTrend && (
        <div className="chart-container">
          <h2>Score Trend Over Time</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.scoreTrend}`}
            alt="Score Trend"
          />
        </div>
      )}

      {charts.scoreRange && (
        <div className="chart-container">
          <h2>Score Range Distribution</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.scoreRange}`}
            alt="Score Range"
          />
        </div>
      )}
      {charts.scoreImprovement && (
        <div className="chart-container">
          <h2>Score improvement over-time</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.scoreImprovement}`}
            alt="scoreImprovement"
          />
        </div>
      )}
      {charts.mistakeCorrectionHeatmap && (
        <div className="chart-container">
          <h2>Mistake Correction Trends</h2>
          <img
            className="chart-image"
            src={`data:image/png;base64,${charts.mistakeCorrectionHeatmap}`}
            alt="Mistake Correction Heatmap"
          />
        </div>
      )}
      
    </div>
  );
};

export default App;
