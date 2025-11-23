// State
let currentType = '';
let currentId = null;

// Navigation
function switchView(viewName) {
  document.querySelectorAll('.view-section').forEach(el => el.classList.add('hidden'));
  document.getElementById(`view-${viewName}`).classList.remove('hidden');

  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  // Find the nav item that was clicked (or corresponds to the view)
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(viewName)) {
      item.classList.add('active');
    }
  });
}

function switchTab(tabEl, contentId) {
  const parent = tabEl.parentElement;
  parent.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  tabEl.classList.add('active');

  const container = parent.parentElement;
  container.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
  container.querySelector(`#${contentId}`).classList.remove('hidden');
}

// Modal Logic
function openModal(type, data = null) {
  currentType = type;
  currentId = data ? data.id : null;
  document.getElementById('modal-title').innerText = data ? `Edit ${type}` : `New ${type}`;

  const container = document.getElementById('modal-form-container');
  container.innerHTML = getFormTemplate(type, data);

  document.getElementById('edit-modal').classList.add('active');
}

function closeModal() {
  document.getElementById('edit-modal').classList.remove('active');
}

// Form Templates
function getFormTemplate(type, data) {
  const d = data || {};
  const trans = (lang) => {
    if (!d.translations) return {};
    return d.translations.find(t => t.lang === lang) || {};
  };
  const es = trans('es');
  const en = trans('en');

  let commonFields = ''; // Slug is now always auto-generated

  let typeFields = '';


  if (type === 'project') {
    const images = d.images || [];
    // Image preview generation
    let imagePreviews = '<div class="image-grid" id="image-preview-container">';
    images.forEach((img, idx) => {
      imagePreviews += `
            <div class="image-item">
                <img src="${img.url}" alt="Preview">
                <div class="image-remove" onclick="removeImage(${idx})"><i class="fas fa-times"></i></div>
            </div>
        `;
    });
    imagePreviews += '</div>';

    // Parse URLs if stored as JSON
    let urls = {};
    if (d.url) {
      try {
        urls = typeof d.url === 'string' ? JSON.parse(d.url) : d.url;
      } catch {
        urls = { live: d.url }; // Fallback for old single URL format
      }
    }

    typeFields = `
                <div class="form-group">
                    <label class="form-label">Category <span style="color:var(--danger)">*</span></label>
                    <select class="form-control" name="category" required>
                        <option value="">Select a category...</option>
                        <option value="project" ${d.category === 'project' ? 'selected' : ''}>Project</option>
                        <option value="work" ${d.category === 'work' ? 'selected' : ''}>Work</option>
                        <option value="study" ${d.category === 'study' ? 'selected' : ''}>Study</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Tags (comma separated)</label>
                    <input type="text" class="form-control" name="tags" value="${(d.tags || []).map(t => t.name).join(', ')}">
                </div>
                <div class="form-group">
                    <label class="form-label" style="font-weight: 600; margin-top: 1rem;">URLS</label>
                </div>
                <div class="form-group">
                    <label class="form-label">GitHub Repository</label>
                    <input type="url" class="form-control" name="url_github" value="${urls.github || ''}" placeholder="https://github.com/username/repo">
                </div>
                <div class="form-group">
                    <label class="form-label">Live Demo</label>
                    <input type="url" class="form-control" name="url_live" value="${urls.live || ''}" placeholder="https://example.com">
                </div>
                <div class="form-group">
                    <label class="form-label">Images</label>
                    ${imagePreviews}
                    <div style="margin-top: 1rem;">
                        <label class="btn" style="background: var(--bg-card); border: 1px dashed var(--border); width: 100%; justify-content: center;">
                            <i class="fas fa-cloud-upload-alt"></i> Upload Image
                            <input type="file" hidden onchange="uploadImage(this)">
                        </label>
                    </div>
                    <input type="hidden" name="images" id="images-input" value='${JSON.stringify(images).replace(/'/g, "&#39;")}'>
                </div>
            `;
  } else if (type === 'experience') {
    typeFields = `
                <div class="form-group">
                    <label class="form-label">Company</label>
                    <input type="text" class="form-control" name="company" value="${d.company || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Location</label>
                    <input type="text" class="form-control" name="location" value="${d.location || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Start Date</label>
                    <input type="date" class="form-control" name="startDate" value="${d.start_date ? d.start_date.substring(0, 10) : ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">End Date</label>
                    <input type="date" class="form-control" name="endDate" value="${d.end_date ? d.end_date.substring(0, 10) : ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Tags (Skills)</label>
                    <input type="text" class="form-control" name="tags" value="${(d.tags || []).map(t => t.name).join(', ')}">
                </div>
            `;
  } else if (type === 'education') {
    typeFields = `
        <div class="form-group">
            <label class="form-label">Institution</label>
            <input type="text" class="form-control" name="institution" value="${d.institution || ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Location</label>
            <input type="text" class="form-control" name="location" value="${d.location || ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Start Date</label>
            <input type="date" class="form-control" name="startDate" value="${d.start_date ? d.start_date.substring(0, 10) : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">End Date</label>
            <input type="date" class="form-control" name="endDate" value="${d.end_date ? d.end_date.substring(0, 10) : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Courses (comma separated)</label>
            <input type="text" class="form-control" name="courses" value="${(d.courses || []).join(', ')}">
        </div>
    `;
  } else if (type === 'skill') {
    typeFields = `
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <input type="text" class="form-control" name="category" value="${d.category || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Proficiency (0-100)</label>
                    <input type="number" class="form-control" name="proficiency" value="${d.proficiency || 50}">
                </div>
                <div class="form-group">
                    <label class="form-label">Icon URL</label>
                    <input type="text" class="form-control" name="icon_url" value="${d.icon_url || ''}">
                </div>
            `;
  } else if (type === 'certification') {
    typeFields = `
        <div class="form-group">
            <label class="form-label">Issuer</label>
            <input type="text" class="form-control" name="issuer" value="${d.issuer || ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Issue Date</label>
            <input type="date" class="form-control" name="issueDate" value="${d.issue_date ? d.issue_date.substring(0, 10) : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Expiry Date</label>
            <input type="date" class="form-control" name="expiryDate" value="${d.expiry_date ? d.expiry_date.substring(0, 10) : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">Credential URL</label>
            <input type="text" class="form-control" name="url" value="${d.credential_url || ''}">
        </div>
    `;
  }

  let translationFields = `
            <div class="tabs">
                <div class="tab active" onclick="switchTab(this, 'trans-es')">Spanish</div>
                <div class="tab" onclick="switchTab(this, 'trans-en')">English</div>
            </div>
            
            <div id="trans-es" class="tab-content">
                <div class="form-group">
                    <label class="form-label">Title/Name (ES) <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="title_es" value="${(es.title || es.name || '').replace(/"/g, '&quot;')}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Subtitle (ES)</label>
                    <input type="text" class="form-control" name="subtitle_es" value="${(es.subtitle || '').replace(/"/g, '&quot;')}">
                </div>
                <div class="form-group">
                    <label class="form-label">Description (ES)</label>
                    <textarea class="form-control" name="description_es">${es.description || ''}</textarea>
                </div>
            </div>

            <div id="trans-en" class="tab-content hidden">
                <div class="form-group">
                    <label class="form-label">Title/Name (EN) <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="title_en" value="${(en.title || en.name || '').replace(/"/g, '&quot;')}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Subtitle (EN)</label>
                    <input type="text" class="form-control" name="subtitle_en" value="${(en.subtitle || '').replace(/"/g, '&quot;')}">
                </div>
                <div class="form-group">
                    <label class="form-label">Description (EN)</label>
                    <textarea class="form-control" name="description_en">${en.description || ''}</textarea>
                </div>
            </div>
        `;

  return `<form id="edit-form">${commonFields}${typeFields}${translationFields}</form>`;
}

// Image Upload Logic
async function uploadImage(input) {
  if (!input.files || !input.files[0]) return;

  const formData = new FormData();
  formData.append('file', input.files[0]);
  formData.append('folder', 'portfolio/projects');

  const btn = input.parentElement;
  const originalText = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';

  try {
    const res = await fetch('/admin/upload-image', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    if (data.success) {
      const imagesInput = document.getElementById('images-input');
      const images = JSON.parse(imagesInput.value || '[]');
      images.push({ url: data.url, type: 'image', caption: '' });
      imagesInput.value = JSON.stringify(images);
      renderImagePreviews(images);
      showToast('Image uploaded', 'success');
    } else {
      showToast('Upload failed: ' + (data.error || 'Unknown error'), 'error');
    }
  } catch (e) {
    showToast('Error uploading: ' + e.message, 'error');
  } finally {
    btn.innerHTML = originalText;
    // Re-attach event listener if needed, though inline onchange should persist
    const newInput = btn.querySelector('input');
    if (newInput) newInput.onchange = function () { uploadImage(this); };
  }
}

function removeImage(index) {
  const imagesInput = document.getElementById('images-input');
  const images = JSON.parse(imagesInput.value || '[]');
  images.splice(index, 1);
  imagesInput.value = JSON.stringify(images);
  renderImagePreviews(images);
}

function renderImagePreviews(images) {
  const container = document.getElementById('image-preview-container');
  let html = '';
  images.forEach((img, idx) => {
    html += `
            <div class="image-item">
                <img src="${img.url}" alt="Preview">
                <div class="image-remove" onclick="removeImage(${idx})"><i class="fas fa-times"></i></div>
            </div>
        `;
  });
  container.innerHTML = html;
}

// Data variables - populated by inline script in HTML
const projects = window.projects || [];
const experiences = window.experiences || [];
const education = window.education || [];
const skills = window.skills || [];
const certifications = window.certifications || [];

function editProject(id) { openModal('project', projects.find(p => p.id === id)); }


function editExperience(id) { openModal('experience', experiences.find(e => e.id === id)); }
function editEducation(id) { openModal('education', education.find(e => e.id === id)); }
function editSkill(id) { openModal('skill', skills.find(s => s.id === id)); }
function editCertification(id) { openModal('certification', certifications.find(c => c.id === id)); }

// API Actions
async function saveItem() {
  const form = document.getElementById('edit-form');
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // Process specific fields
  if (data.tags) data.tags = data.tags.split(',').map(t => t.trim());
  if (data.images) {
    try { data.images = JSON.parse(data.images); }
    catch { data.images = []; }
  }

  // Combine URL fields into JSON object
  if (data.url_github || data.url_live) {
    data.url = JSON.stringify({
      github: data.url_github || null,
      live: data.url_live || null
    });
    delete data.url_github;
    delete data.url_live;
  }

  if (currentId) data.id = currentId;

  try {
    const res = await fetch(`/admin/save/${currentType}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      showToast('Saved successfully', 'success');
      setTimeout(() => location.reload(), 1000);
    } else {
      const err = await res.json();
      showToast(err.error || 'Error saving', 'error');
    }
  } catch (e) {
    showToast(e.message, 'error');
  }
}


async function deleteItem(type, id) {
  if (!confirm('Are you sure?')) return;

  try {
    const res = await fetch(`/admin/delete/${type}/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Deleted successfully', 'success');
      setTimeout(() => location.reload(), 1000);
    } else {
      showToast('Error deleting', 'error');
    }
  } catch (e) {
    showToast(e.message, 'error');
  }
}

async function saveProfile() {
  const form = document.getElementById('profile-form');
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  try {
    data.location = JSON.parse(data.location);
    data.social = JSON.parse(data.social);
  } catch (e) {
    showToast('Invalid JSON in location or social links', 'error');
    return;
  }

  try {
    const res = await fetch('/admin/save/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      showToast('Profile saved', 'success');
    } else {
      showToast('Error saving profile', 'error');
    }
  } catch (e) {
    showToast(e.message, 'error');
  }
}

function showToast(msg, type) {
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.className = `toast show ${type}`;
  setTimeout(() => toast.classList.remove('show'), 3000);
}
