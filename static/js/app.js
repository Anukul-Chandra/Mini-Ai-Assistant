const chatBox = document.getElementById("chat-box");
const input = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");
const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const uploadStatus = document.getElementById("upload-status");

let uploadedFilename = null;

uploadArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  uploadStatus.textContent = "Uploading...";
  uploadStatus.className = "";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/upload/document", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      uploadStatus.textContent = `Error: ${data.detail || "Upload failed"}`;
      uploadStatus.className = "error";
      return;
    }

    uploadedFilename = data.filename;
    uploadStatus.textContent = `Indexed "${data.filename}" (${data.chunks} chunks)`;
    uploadStatus.className = "success";
    uploadArea.classList.add("has-file");
  } catch {
    uploadStatus.textContent = "Network error during upload";
    uploadStatus.className = "error";
  }
});

sendBtn.addEventListener("click", askQuestion);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
});

async function askQuestion() {
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";
  sendBtn.disabled = true;

  const loadingId = addMessage("Thinking...", "loading");

  try {
    const res = await fetch("/chat/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    removeMessage(loadingId);

    if (!res.ok) {
      addMessage(data.detail || "Something went wrong", "error");
      return;
    }

    if (data.source === "tool") {
      addMessage(formatToolResult(data.answer), "bot");
    } else {
      addMessage(data.answer, "bot");
    }
  } catch {
    removeMessage(loadingId);
    addMessage("Network error. Please try again.", "error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
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

function formatToolResult(data) {
  if (typeof data === "object" && data !== null) {
    return JSON.stringify(data, null, 2);
  }
  return String(data);
}
