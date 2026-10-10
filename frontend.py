from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ML Workspace UI Engine")

@app.get("/", response_class=HTMLResponse)
async def render_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📊 Automated Machine Learning Platform Workspace</title>
        <script src="https://jsdelivr.net"></script>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 350px 1fr; gap: 25px; }
            .sidebar { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            .main-content { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            h1, h3, h4 { margin-top: 0; color: #111; }
            .btn { background: #ff4b4b; color: white; border: none; padding: 12px 15px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; font-size: 15px; margin-top: 10px; }
            .btn:hover { background: #e03e3e; }
            .form-group { margin-bottom: 18px; }
            label { display: block; margin-bottom: 6px; font-weight: 500; font-size: 14px; color: #444; }
            select, input[type="file"] { width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc; box-sizing: border-box; background: #fff; }
            select[multiple] { height: 100px; }
            .metric-card { background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 5px solid #2196f3; font-size: 14px; line-height: 1.5; }
            .matrix-table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; }
            .matrix-table th, .matrix-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            .matrix-table th { background-color: #f7f7f7; font-weight: 600; }
            .charts-grid { display: grid; grid-template-columns: 1fr; gap: 30px; margin-top: 20px; }
            .chart-container { background: #fafafa; padding: 15px; border-radius: 6px; border: 1px solid #eee; }
        </style>
    </head>
    <body>
        <h1>📊 Automated Machine Learning Platform Workspace</h1>
        <p style="color: #666; margin-bottom: 25px;">Upload clean data structures, configure variable constraints, and evaluate Scikit-Learn models in real time.</p>
        
        <div class="container">
            <div class="sidebar">
                <h3>Workspace Settings</h3>
                <div class="form-group">
                    <label>Upload Target Workspace File (.csv, .xlsx)</label>
                    <input type="file" id="datasetFile" accept=".csv, .xlsx" onchange="analyzeDataset()">
                </div>
                
                <div id="dynamicControls" style="display:none;"></div>
            </div>
            
            <div class="main-content">
                <h3>⚡ Live Computational Results</h3>
                <div id="runtimeKPI"></div>
                <div id="resultsTableContainer"></div>
                
                <div class="charts-grid" id="visualizationsContainer" style="display:none;">
                    <div class="chart-container">
                        <h4>📈 Performance Distribution Visualization</h4>
                        <canvas id="performanceChart" height="120"></canvas>
                    </div>
                    <div class="chart-container">
                        <h4>⏱️ Model Speed Analysis</h4>
                        <canvas id="speedChart" height="120"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentColumns = [];

            async function analyzeDataset() {
                const fileInput = document.getElementById('datasetFile');
                if (!fileInput.files.length) return;

                const formData = new FormData();
                // ⭐ FIXED: Grabbed the single file index [0] so it parses correctly
                formData.append('file', fileInput.files[0]);

                try {
                    const res = await fetch('/analyze-file', { method: 'POST', body: formData });
                    if (res.status === 200) {
                        const data = await res.json();
                        currentColumns = data.columns;
                        
                        let targetOptions = currentColumns.map(col => `<option value="${col}">${col}</option>`).join('');
                        
                        let controlsHtml = `
                            <div class="metric-card">
                                <strong>🔍 Dataset Profile Metrics</strong><br>
                                • Matrix Shape: ${data.shape[0]} rows × ${data.shape[1]} columns<br>
                                • Total Elements: ${data.size}<br>
                                • Numerical Parameters: ${data.numerical_features}<br>
                                • Categorical Parameters: ${data.categorical_features}<br>
                                • Missing Value Columns: ${data.null_features}<br>
                                • Duplicate Rows: ${data.duplicate_rows}
                            </div>
                            
                            <div class="form-group">
                                <label>Select Machine Learning Track</label>
                                <select id="trackCode" onchange="toggleTrackInputs()">
                                    <option value="R">Regression (R)</option>
                                    <option value="C">Classification (C)</option>
                                    <option value="G">Clustering Unsupervised (G)</option>
                                </select>
                            </div>
                            
                            <div class="form-group" id="targetContainer">
                                <label>Choose Target Predictor Component (y)</label>
                                <select id="targetVariable">${targetOptions}</select>
                            </div>
                            
                            <div class="form-group">
                                <label>Choose Optional Attributes to Omit (Hold Ctrl to select multiple)</label>
                                <select id="dropSelections" multiple>${targetOptions}</select>
                            </div>
                            
                            <button class="btn" onclick="executePipeline()">⚙️ Execute Model Pipeline Computations</button>
                        `;
                        
                        document.getElementById('dynamicControls').innerHTML = controlsHtml;
                        document.getElementById('dynamicControls').style.display = 'block';
                    } else {
                        const errText = await res.text();
                        alert('Backend Analysis Error: ' + errText);
                    }
                } catch (err) { alert('Failed to parse connection protocols from the backend engine.'); }
            }

            function toggleTrackInputs() {
                const track = document.getElementById('trackCode').value;
                const targetContainer = document.getElementById('targetContainer');
                targetContainer.style.display = (track === 'G') ? 'none' : 'block';
            }

            async function executePipeline() {
                const fileInput = document.getElementById('datasetFile');
                if (!fileInput.files.length) return;

                const track = document.getElementById('trackCode').value;
                const target = track !== 'G' ? document.getElementById('targetVariable').value : '';
                
                const dropOptions = document.getElementById('dropSelections').options;
                const omittedCols = [];
                for (let i = 0; i < dropOptions.length; i++) {
                    if (dropOptions[i].selected) omittedCols.push(dropOptions[i].value);
                }

                const formData = new FormData();
                // ⭐ FIXED: Grabbed the single file index [0] here as well
                formData.append('file', fileInput.files[0]);
                formData.append('problem_type', track);
                formData.append('target_column', target);
                formData.append('drop_columns', JSON.stringify(omittedCols));

                try {
                    const res = await fetch('/evaluate', { method: 'POST', body: formData });
                    if (res.status === 200) {
                        const data = await res.json();
                        
                        document.getElementById('runtimeKPI').innerHTML = `
                            <div class="metric-card" style="background:#e8f5e9; border-left-color:#4caf50;">
                                ⌛ <strong>Overall Execution Runtime:</strong> ${data.total_pipeline_time_sec} Sec
                            </div>
                        `;
                        
                        let isClustering = track === 'G';
                        let scoreHeader = isClustering ? '<th>Silhouette</th><th>Davies Bouldin</th><th>Calinski Harabasz</th>' : '<th>Acc Train</th><th>Acc Test</th>';
                        
                        let tableHtml = `<table class="matrix-table"><thead><tr><th>Model Framework</th>${scoreHeader}<th>Execution Time (Sec)</th></tr></thead><tbody>`;
                        
                        const modelNames = [];
                        const scoreMetrics1 = [];
                        const scoreMetrics2 = [];
const speedRuntimes = [];
for (const [model, metrics] of Object.entries(data.results)) {
modelNames.push(model);
speedRuntimes.push(parseFloat(metrics.Execution_Time_Sec));
if (isClustering) {
tableHtml += <tr><td><strong>${model}</strong></td><td>${metrics.Silhouette}</td><td>${metrics.Davies_Bouldin}</td><td>${metrics.Calinski_Harabasz}</td><td>${metrics.Execution_Time_Sec}</td></tr>;
scoreMetrics1.push(parseFloat(metrics.Silhouette));
} else {
let testScore = metrics.Acc_Test_R2 || metrics.Acc_Test;
tableHtml += <tr><td><strong>${model}</strong></td><td>${metrics.Acc_Train}</td><td>${testScore}</td><td>${metrics.Execution_Time_Sec}</td></tr>;
scoreMetrics1.push(parseFloat(metrics.Acc_Train));
scoreMetrics2.push(parseFloat(testScore));
}
}
tableHtml += '';
document.getElementById('resultsTableContainer').innerHTML = tableHtml;
document.getElementById('visualizationsContainer').style.display = 'grid';
// Render Performance Graph
let datasetArray = isClustering ?
[{ label: 'Silhouette Index Metric', data: scoreMetrics1, backgroundColor: '#4caf50' }] :
[{ label: 'Train Score Split', data: scoreMetrics1, backgroundColor: '#2196f3' }, { label: 'Test Score Split', data: scoreMetrics2, backgroundColor: '#bbdefb' }];
new Chart(document.getElementById('performanceChart'), {
type: 'bar',
data: { labels: modelNames, datasets: datasetArray },
options: { responsive: true, scales: { y: { min: 0, max: isClustering ? undefined : 1.05 } } }
});
// Render Speed Graph
new Chart(document.getElementById('speedChart'), {
type: 'bar',
data: {
labels: modelNames,
datasets: [{ label: 'Model Runtime Duration Speed (Seconds)', data: speedRuntimes, backgroundColor: '#ff9800' }]
},
options: { responsive: true }
});
}
} catch (err) { alert('Processing computational pipeline failure.'); }
}



"""