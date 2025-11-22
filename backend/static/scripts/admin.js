// Image upload handling
function setupImageUpload(inputId, previewId, urlFieldId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  const urlField = document.getElementById(urlFieldId);

  if (!input) return;

  input.addEventListener("change", async function (e) {
    const file = e.target.files[0];
    if (!file) return;

    // Show loading state
    preview.innerHTML = '<p class="text-gray-500">Uploading...</p>';

    // Create form data
    const formData = new FormData();
    formData.append("file", file);
    formData.append("folder", "portfolio");

    try {
      // Upload to Cloudinary via backend
      const response = await fetch("/admin/upload-image", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        // Show preview
        preview.innerHTML = `<img src="${result.url}" class="max-w-full h-auto rounded" alt="Preview">`;
        // Set hidden field value
        urlField.value = result.url;
      } else {
        preview.innerHTML = `<p class="text-red-500">Error: ${result.error}</p>`;
      }
    } catch (error) {
      preview.innerHTML = `<p class="text-red-500">Upload failed: ${error.message}</p>`;
    }
  });
}

// Initialize image uploads when page loads
document.addEventListener("DOMContentLoaded", function () {
  setupImageUpload(
    "desktop-image-input",
    "desktop-image-preview",
    "desktop-image-url",
  );
  setupImageUpload(
    "mobile-image-input",
    "mobile-image-preview",
    "mobile-image-url",
  );
});

// Delete form handling
const deleteForm = document.getElementById("delete-form");
if (deleteForm) {
  deleteForm.addEventListener("submit", function (e) {
    const select = document.getElementById("project-select");
    const id = select.value;
    if (!id) {
      alert("Selecciona un proyecto para eliminar.");
      e.preventDefault();
      return;
    }

    this.action = `/admin/delete/${id}`;
  });
}
