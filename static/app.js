// Response AI Dashboard Client Logic

const PRESETS = {
  1: `Production server APP-PROD-01 is down since 2:30 AM. 
Users are getting error 503. Database connection is failing. 
Reported by John Smith.`,
  2: `DB-CLUSTER-03 experienced high memory pressure at 04:15 AM. 
Query timeouts occurred with error code 504. Connection pool exhausted. 
Reported by Sarah Jenkins.`,
  3: `AUTH-GW-02 service is un-responsive. 
API authentication requests are returning 500 Internal Server Error. 
Reported by Alex Rivera.`
};

function loadPreset(id) {
  const input = document.getElementById('ticketInput');
  if (PRESETS[id]) {
    input.value = PRESETS[id];
  }
}

// Auto load preset 1 on start
window.addEventListener('DOMContentLoaded', () => {
  loadPreset(1);
});

async function runAnalysis() {
  const ticketInput = document.getElementById('ticketInput').value.trim();
  const analyzeBtn = document.getElementById('analyzeBtn');
  const btnSpinner = document.getElementById('btnSpinner');
  const btnText = document.getElementById('btnText');

  if (!ticketInput) {
    alert('Please enter an incident ticket description or select a preset!');
    return;
  }

  // UI State: Loading
  analyzeBtn.disabled = true;
  btnSpinner.classList.remove('hidden');
  btnText.innerText = 'Analyzing Ticket...';

  resetPipelineUI();

  try {
    // Step 1: Active
    setStepState(1, 'active');

    const response = await fetch('/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ticket: ticketInput })
    });

    const data = await response.json();

    if (response.ok && data.status === 'success') {
      // Step 1 & 2 completed
      setStepState(1, 'completed');
      setStepState(2, 'completed');
      setStepState(3, 'completed');
      setStepState(4, 'completed');

      // Populate Entities
      if (data.entities) {
        document.getElementById('valServer').innerText = data.entities.server_name || 'N/A';
        document.getElementById('valComponent').innerText = data.entities.component || 'N/A';
        document.getElementById('valErrorCode').innerText = data.entities.error_code || 'N/A';
        document.getElementById('valReporter').innerText = data.entities.reporter || 'N/A';
        document.getElementById('entityContainer').classList.remove('hidden');
      }

      // Populate Analysis & Report
      document.getElementById('analysisOutput').innerText = data.analysis;
      document.getElementById('reportOutput').innerText = data.report;
      document.getElementById('resultsContainer').classList.remove('hidden');

    } else {
      alert('Error: ' + (data.error || 'Failed to process incident ticket'));
      resetPipelineUI();
    }

  } catch (err) {
    console.error('API Error:', err);
    alert('Failed to connect to Response AI API server!');
    resetPipelineUI();
  } finally {
    analyzeBtn.disabled = false;
    btnSpinner.classList.add('hidden');
    btnText.innerText = '🚀 Run Agentic Analysis';
  }
}

function setStepState(stepNum, state) {
  const step = document.getElementById(`step${stepNum}`);
  if (!step) return;

  step.classList.remove('active', 'completed');
  if (state === 'active') step.classList.add('active');
  if (state === 'completed') step.classList.add('completed');
}

function resetPipelineUI() {
  for (let i = 1; i <= 4; i++) {
    setStepState(i, '');
  }
  document.getElementById('entityContainer').classList.add('hidden');
  document.getElementById('resultsContainer').classList.add('hidden');
}

function copyReport() {
  const reportText = document.getElementById('reportOutput').innerText;
  navigator.clipboard.writeText(reportText).then(() => {
    alert('Incident report copied to clipboard!');
  });
}
