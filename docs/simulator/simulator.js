const modes = {
  resurrection: {
    label: "Resurrection Demo",
    total: 8,
    destroyed: [1, 2, 5],
    integrity: 0.625,
    continuity: "PATCHED",
    ask: "User: Explain TCP/IP in 5 structured steps",
    answer:
`Agent:
1. Devices create data at the application layer.
2. TCP breaks data into ordered, reliable segments.
3. IP wraps segments into packets and routes them across networks.
4. Routers forward packets toward the destination host.
5. The receiver reassembles data and delivers it to the application.`,
    raw:
`1. Devices create data at the app layer.
[XLIFELINE_GAP]
3. IP wraps segments into packets...
4. Routers forward packets...
[XLIFELINE_GAP]`,
    recovered:
`Recovered continuity mode: patched

Agent:
3. IP wraps segments into packets and routes them across networks.
4. Routers forward packets toward the destination host.
5. The receiver reassembles data and delivers it to the application.`
  },

  corruption: {
    label: "Corruption Demo",
    total: 8,
    destroyed: [2, 4, 6],
    integrity: 0.625,
    continuity: "PARTIAL",
    ask: "User: Analyze Q1 financial dataset",
    answer:
`Agent:
Loading dataset...
Running anomaly detection...
Detecting unusual spike in region EU-West...
Generating statistical summary...
Preparing final insight report...`,
    raw:
`User: Analyze Q1 financial d[XLIFELINE_GAP]
Agent: Running anomaly detection[XLIFELINE_GAP]
Detecting unusual spike in regio[XLIFELINE_GAP]
tistical summary.
Agent: Preparing final insight report.`,
    recovered:
`Recovered text:
User: Analyze Q1 financial d[XLIFELINE_GAP]
Agent: Running anomaly detection[XLIFELINE_GAP]
Detecting unusual spike in regio[XLIFELINE_GAP]
tistical summary.
Agent: Preparing final insight report.`
  },

  continuity: {
    label: "Continuity Demo",
    total: 6,
    destroyed: [1, 4],
    integrity: 0.667,
    continuity: "PATCHED",
    ask: "User: Continue from step 3",
    answer:
`Agent:
Recovered context available.
Resuming from step 3.
3. IP wraps segments into packets and routes them across networks.
4. Routers forward packets toward the destination host.
5. The receiver reconstructs data for the destination application.`,
    raw:
`Recovered continuity mode: patched
Recovered context:
1. Devices create data...
[XLIFELINE_GAP]
3. IP wraps segments into packets...
4. Routers forward packets...
[XLIFELINE_GAP]`,
    recovered:
`Agent:
Resuming from recovered memory state.
3. IP wraps segments into packets and routes them across networks.
4. Routers forward packets toward the destination host.
5. The receiver reconstructs data for the destination application.`
  }
};

let currentMode = "resurrection";
let timerChain = [];

const fragGrid = document.getElementById("fragGrid");
const terminalText = document.getElementById("terminalText");
const rawBox = document.getElementById("rawBox");
const recoveredBox = document.getElementById("recoveredBox");
const integrityText = document.getElementById("integrityText");
const integrityFill = document.getElementById("integrityFill");
const continuityMode = document.getElementById("continuityMode");
const fragmentStats = document.getElementById("fragmentStats");
const statusBanner = document.getElementById("statusBanner");
const modeLabel = document.getElementById("modeLabel");

function clearTimers(){
  timerChain.forEach(t => clearTimeout(t));
  timerChain = [];
}

function resetSteps(){
  document.querySelectorAll(".step").forEach(s => {
    s.classList.remove("active", "done", "orange");
  });
}

function setStep(i, orange = false){
  document.querySelectorAll(".step").forEach((s, idx) => {
    s.classList.toggle("done", idx < i);
    s.classList.toggle("active", idx === i);
    s.classList.toggle("orange", idx === i && orange);
  });
}

function renderGrid(mode, phase = "initial"){
  fragGrid.innerHTML = "";
  const cfg = modes[mode];

  for(let i = 0; i < cfg.total; i++){
    const div = document.createElement("div");
    div.className = "frag";
    div.textContent = String(i).padStart(2, "0");

    const isDead = cfg.destroyed.includes(i);

    if(phase === "initial"){
      div.classList.add("alive");
    } else if(phase === "destroyed"){
      div.classList.add(isDead ? "dead" : "alive");
    } else if(phase === "recovered"){
      div.classList.add(isDead ? "recovered" : "alive");
    }

    fragGrid.appendChild(div);
  }
}

function setStats(mode, phase = "initial"){
  const cfg = modes[mode];

  if(phase === "initial"){
    integrityText.textContent = "1.000";
    integrityFill.style.width = "100%";
    integrityFill.style.background = "linear-gradient(90deg,#38bdf8,#22c55e)";
    continuityMode.textContent = "EXACT";
    fragmentStats.textContent = `${cfg.total} total / 0 destroyed / ${cfg.total} recovered`;
    statusBanner.className = "status-banner ok";
    statusBanner.textContent = "✔ CONTINUITY HEALTHY — exact state available";
  } else if(phase === "destroyed"){
    integrityText.textContent = cfg.integrity.toFixed(3);
    integrityFill.style.width = `${cfg.integrity * 100}%`;
    integrityFill.style.background = "linear-gradient(90deg,#f97316,#f59e0b)";
    continuityMode.textContent = cfg.continuity;
    fragmentStats.textContent = `${cfg.total} total / ${cfg.destroyed.length} destroyed / ${cfg.total - cfg.destroyed.length} recovered`;
    statusBanner.className = "status-banner warn";
    statusBanner.textContent = "⚠ PARTIAL CONTINUITY — reconstruction required";
  } else {
    integrityText.textContent = cfg.integrity.toFixed(3);
    integrityFill.style.width = `${cfg.integrity * 100}%`;
    integrityFill.style.background = "linear-gradient(90deg,#38bdf8,#f97316)";
    continuityMode.textContent = cfg.continuity;
    fragmentStats.textContent = `${cfg.total} total / ${cfg.destroyed.length} destroyed / ${cfg.total - cfg.destroyed.length} recovered`;
    statusBanner.className = "status-banner ok";
    statusBanner.textContent = "✔ CONTINUITY RESTORED — task resumed successfully";
  }
}

function typeText(el, text, speed = 14, done){
  el.textContent = "";
  let i = 0;

  function tick(){
    el.textContent = text.slice(0, i++);
    if(i <= text.length){
      const t = setTimeout(tick, speed);
      timerChain.push(t);
    } else if(done){
      done();
    }
  }

  tick();
}

function hardReset(){
  clearTimers();
  resetSteps();
  renderGrid(currentMode, "initial");
  setStats(currentMode, "initial");
  terminalText.textContent = "Ready.";
  rawBox.textContent = "";
  recoveredBox.textContent = "";
  modeLabel.textContent = modes[currentMode].label;

  document.querySelectorAll(".mode-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.mode === currentMode);
  });
}

function playDemo(){
  clearTimers();
  resetSteps();
  rawBox.textContent = "";
  recoveredBox.textContent = "";
  const cfg = modes[currentMode];

  setStep(0);
  renderGrid(currentMode, "initial");
  setStats(currentMode, "initial");

  typeText(terminalText, cfg.ask + "\n\n" + cfg.answer, 9);

  timerChain.push(setTimeout(() => {
    setStep(1);
    terminalText.textContent += "\n\n██ Memory fragmented as DFG";
  }, 1800));

  timerChain.push(setTimeout(() => {
    setStep(2, true);
    renderGrid(currentMode, "destroyed");
    setStats(currentMode, "destroyed");
    terminalText.textContent += `\n██ Corruption simulated: ${cfg.destroyed.length} fragments destroyed`;
    rawBox.textContent = cfg.raw;
  }, 3600));

  timerChain.push(setTimeout(() => {
    setStep(3, true);
    terminalText.textContent += "\n██ Rebuild path resolved";
    renderGrid(currentMode, "recovered");
  }, 5400));

  timerChain.push(setTimeout(() => {
    terminalText.textContent += "\n██ Semantic repair activated";
    recoveredBox.textContent = cfg.recovered;
  }, 6800));

  timerChain.push(setTimeout(() => {
    setStep(4);
    setStats(currentMode, "recovered");
    terminalText.textContent += "\n██ Continuity restored — execution continues";
  }, 8200));
}

document.querySelectorAll(".mode-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    currentMode = btn.dataset.mode;
    hardReset();
  });
});

document.getElementById("playBtn").addEventListener("click", playDemo);
document.getElementById("resetBtn").addEventListener("click", hardReset);

hardReset();