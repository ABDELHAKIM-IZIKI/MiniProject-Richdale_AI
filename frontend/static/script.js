const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const predictionBox = document.getElementById("prediction");
let selectedFile = null;

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    selectedFile = files[0];
    dropZone.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
  }
});

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  dropZone.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
});

async function uploadImage() {
  if (!selectedFile) {
    return alert("Please select an image first");
  }

  const validExtensions = [".jpg", ".jpeg", ".JPG", ".JPEG"];
  const fileExt = selectedFile.name
    .substring(selectedFile.name.lastIndexOf("."))
    .toLowerCase();
  if (!validExtensions.includes(fileExt)) {
    return alert("File must have .jpg or .jpeg extension");
  }

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("http://localhost:7000/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    document.getElementById("typeResult").textContent = data.result;
    document.getElementById("percentageResult").textContent =
      data.confidence || "--";
    document.getElementById("resultImage").src = data.image;
    predictionBox.style.display = "block";
  } catch (err) {
    alert("Prediction failed: " + err.message);
  }
}
