const fileInput = document.getElementById("cv_file");
const fileLabel = document.getElementById("file-label");
const form = document.getElementById("cv-upload-form");
const submitBtn = document.getElementById("cv-submit-btn");

if (fileInput && fileLabel) {
  fileInput.addEventListener("change", () => {
    const name = fileInput.files[0]?.name;
    fileLabel.textContent = name || "Choose file or drag here";
  });
}

if (form && submitBtn) {
  form.addEventListener("submit", () => {
    submitBtn.disabled = true;
    submitBtn.textContent = "AI is analyzing your CV…";
  });
}