const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("file-input");
const dzEmpty = document.getElementById("dropzone-empty");
const previewWrap = document.getElementById("preview-wrap");
const previewImg = document.getElementById("preview-img");
const scanline = document.getElementById("scanline");
const analyzeBtn = document.getElementById("analyze-btn");
const resetBtn = document.getElementById("reset-btn");
const statusLine = document.getElementById("status-line");
const resultCard = document.getElementById("result-card");
const resultBadge = document.getElementById("result-badge");
const resultConfidence = document.getElementById("result-confidence");
const resultBars = document.getElementById("result-bars");

let selectedFile = null;

// ---- Dropzone interactions ----
dropzone.addEventListener("click", () => fileInput.click());

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length) handleFile(e.target.files[0]);
});

function handleFile(file) {
  if (!file.type.startsWith("image/")) {
    setStatus("Please choose an image file (PNG/JPG).", true);
    return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    dzEmpty.classList.add("hidden");
    previewWrap.classList.remove("hidden");
    analyzeBtn.disabled = false;
    resetBtn.classList.remove("hidden");
    resultCard.classList.add("hidden");
    setStatus("");
  };
  reader.readAsDataURL(file);
}

resetBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewWrap.classList.add("hidden");
  dzEmpty.classList.remove("hidden");
  analyzeBtn.disabled = true;
  resetBtn.classList.add("hidden");
  resultCard.classList.add("hidden");
  scanline.classList.add("hidden");
  setStatus("");
});

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  resultCard.classList.add("hidden");
  scanline.classList.remove("hidden");
  setStatus("Scanning image…");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const res = await fetch("/predict", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      setStatus(data.error || "Something went wrong.", true);
      analyzeBtn.disabled = false;
      scanline.classList.add("hidden");
      return;
    }

    renderResult(data);
    setStatus("Analysis complete.");
  } catch (err) {
    setStatus("Could not reach the server. Is the Flask app running?", true);
  } finally {
    analyzeBtn.disabled = false;
    scanline.classList.add("hidden");
  }
});

function setStatus(msg, isError = false) {
  statusLine.textContent = msg;
  statusLine.classList.toggle("error", isError);
}

function renderResult(data) {
  resultBadge.textContent = data.display_result;
  resultBadge.className = "result-badge " + (data.has_tumor ? "alert" : "clear");
  resultConfidence.textContent = `${(data.confidence * 100).toFixed(1)}% confidence`;

  resultBars.innerHTML = "";
  data.all_probabilities.forEach((item, idx) => {
    const row = document.createElement("div");
    row.className = "result-row" + (idx === 0 ? " top" : "") + (item.label === "notumor" ? " notumor" : "");

    const label = document.createElement("span");
    label.textContent = item.label;

    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${(item.confidence * 100).toFixed(1)}%`;
    track.appendChild(fill);

    const pct = document.createElement("span");
    pct.textContent = `${(item.confidence * 100).toFixed(1)}%`;

    row.append(label, track, pct);
    resultBars.appendChild(row);
  });

  resultCard.classList.remove("hidden");
}
