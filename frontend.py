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
            .container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 300px 1fr; gap: 20px; }
            .sidebar { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            .main-content { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            h1, h3 { margin-top: 0; color: #111; }
            .btn { background: #ff4b4b; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }
            .btn:hover { background: #e03e3e; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: 500; font-size: 14px; }
            select, input[type="file"] { width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd; box-sizing: border-box; }
            .metric-card { background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 5px solid #2196f3; }
            .matrix-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            .matrix-table th, .matrix-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            .matrix-table th { background-color: #f1f1f1; }
        </style>
    </head>
    <body>
        <h1>📊 Automated Machine Learning Platform Workspace</h1>
        <p>Upload clean data structures, configure variable constraints, and evaluate Scikit-Learn models in real time.</p>
        
        <div class="container">
            <div class="sidebar">
                <h3>Workspace Settings</h3>
                <div class="form-group">
                    <label>Upload Dataset File (.csv, .xlsx)</label>
                    <input type="file" id="datasetFile" accept=".csv, .xlsx" onchange="analyzeDataset()">
                </div>
                <div id="profileMetrics" style="display:none;"></div>
            </div>
            
            <div class="main-content">
                <h3>⚡ Live Computational Results</h3>
                <div id="runtimeKPI"></div>
                <div id="resultsTableContainer"></div>
                <div style="max-width: 600px; margin-top: 20px;">
                    <canvas id="speedChart"></canvas>
                </div>
            </div>
        </div>

        <script>
            let cachedFile = null;

            async function analyzeDataset() {
                const fileInput = document.getElementById('datasetFile');
                if (!fileInput.files.length) return;
                cachedFile = fileInput.files[0];

                const formData = new FormData();
                formData.append('file', cachedFile);

                try {
                    const res = await fetch('/analyze-file', { method: 'POST', body: formData });
                    if (res.status === 200) {
                        const data = await res.json();
                        let metricsHtml = `
                            <div class="metric-card">
                                <strong>🔍 Dataset Profile Metrics</strong><br>
                                <p>Rows × Columns: ${data.shape[0]} × ${data.shape[1]}</p>
                                <p>Numerical features: ${data.numerical_features}</p>
                                <p>Categorical features: ${data.categorical_features}</p>
                                <p>Duplicates: ${data.duplicate_rows}</p>
                            </div>
                            <div class="form-group">
                                <label>Select Machine Learning Track</label>
                                <select id="trackCode">
                                    <option value="R">Regression (R)</option>
                                    <option value="C">Classification (C)</option>
                                    <option value="G">Clustering Unsupervised (G)</option>
                                </select>
                            </div>
                            <button class="btn" onclick="executePipeline()">⚙️ Execute Pipeline</button>
                        `;
                        document.getElementById('profileMetrics').innerHTML = metricsHtml;
                        document.getElementById('profileMetrics').style.display = 'block';
                    }
                } catch (err) { alert('Communication error with pipeline backend node.'); }
            }

            async function executePipeline() {
                if (!cachedFile) return;
                const track = document.getElementById('trackCode').value;
                
                const formData = new FormData();
                formData.append('file', cachedFile);
                formData.append('problem_type', track);
                formData.append('target_column', ''); 
                formData.append('drop_columns', '[]');

                try {
                    const res = await fetch('/evaluate', { method: 'POST', body: formData });
                    if (res.status === 200) {
                        const data = await res.json();
                        document.getElementById('runtimeKPI').innerHTML = `<div class="metric-card">⌛ Overall Execution Runtime: <strong>${data.total_pipeline_time_sec} Sec</strong></div>`;
                        
                        // Render standard runtime tables and performance chart indices
                        let tableHtml = '<table class="matrix-table"><thead><tr><th>Model</th><th>Train Score</th><th>Test Score</th><th>Runtime (Sec)</th></tr></thead><tbody>';
                        const labels = [];
                        const runtimes = [];
                        
                        for (const [model, metrics] of Object.entries(data.results)) {
                            tableHtml += `<tr><td>${model}</td><td>${metrics.Acc_Train || metrics.Silhouette || 'N/A'}</td><td>${metrics.Acc_Test_R2 || metrics.Acc_Test || 'N/A'}</td><td>${metrics.Execution_Time_Sec}</td></tr>`;
                            labels.push(model);
                            runtimes.push(parseFloat(metrics.Execution_Time_Sec));
                        }
                        tableHtml += '</tbody></table>';
                        document.getElementById('resultsTableContainer').innerHTML = tableHtml;

                        // Render Speed Chart
                        new Chart(document.getElementById('speedChart'), {
                            type: 'bar',
                            data: {
                                labels: labels,
                                datasets: [{ label: 'Model Execution Time (Seconds)', data: runtimes, backgroundColor: '#2196f3' }]
                            }
                        });
                    }
                } catch (err) { alert('Error processing workspace computation logs.'); }
            }
        </script>
    </body>
    </html>
    """