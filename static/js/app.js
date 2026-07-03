const chatBox = document.getElementById("chat-box");
const questionInput = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");
const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const uploadStatus = document.getElementById("upload-status");
const sourcesList = document.getElementById("sources-list");

let uploadedFilename = null;

uploadArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  uploadArea.classList.add("loading");
  uploadStatus.textContent = "Uploading document...";
  uploadStatus.className = "loading";
  fileInput.disabled = true;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/upload/document", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      uploadStatus.textContent = data.detail || "Upload failed";
      uploadStatus.className = "error";
      return;
    }

    uploadedFilename = data.filename;
    uploadStatus.textContent = `Indexed "${data.filename}" \u2014 ${data.chunks} chunks`;
    uploadStatus.className = "success";
    uploadArea.classList.remove("loading");
    uploadArea.classList.add("has-file");
  } catch {
    uploadStatus.textContent = "Network error during upload";
    uploadStatus.className = "error";
  } finally {
    uploadArea.classList.remove("loading");
    fileInput.disabled = false;
  }
});

sendBtn.addEventListener("click", askQuestion);
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
});

async function askQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addMessage(question, "user");
  questionInput.value = "";
  sendBtn.disabled = true;

  const loadingEl = addSpinner();

  try {
    const res = await fetch("/chat/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    removeMessage(loadingEl);

    if (!res.ok) {
      addMessage(data.detail || "Something went wrong", "error");
      return;
    }

    addMessage(data.answer || JSON.stringify(data), "bot");
    if (data.type === "knowledge" && data.retrieved_chunks) {
      updateSources(question, data.retrieved_chunks);
    }
  } catch {
    removeMessage(loadingEl);
    addMessage("Network error. Please try again.", "error");
  } finally {
    sendBtn.disabled = false;
    questionInput.focus();
  }
}

function updateSources(question, chunks) {
  sourcesList.innerHTML = "";

  const count = chunks.length;
  const header = document.createElement("p");
  header.textContent = `Retrieved ${count} chunk${count !== 1 ? "s" : ""} for: "${question}"`;
  sourcesList.appendChild(header);

  chunks.forEach((chunk, i) => {
    const item = document.createElement("p");
    item.className = "chunk";
    item.textContent = chunk;
    sourcesList.appendChild(item);
  });

  const details = sourcesList.closest("details");
  if (details) details.open = true;
}

function addSpinner() {
  const placeholder = chatBox.querySelector(".placeholder");
  if (placeholder) placeholder.remove();

  const container = document.createElement("div");
  container.className = "message loading";
  container.innerHTML = '<span class="spinner"></span> Thinking...';
  chatBox.appendChild(container);
  chatBox.scrollTop = chatBox.scrollHeight;
  return container;
}

function addMessage(text, className) {
  const placeholder = chatBox.querySelector(".placeholder");
  if (placeholder) placeholder.remove();

  const div = document.createElement("div");
  div.className = `message ${className}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

function removeMessage(el) {
  if (el && el.parentNode) el.remove();
}


