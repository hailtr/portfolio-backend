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

function switchResumeTab(tabEl, contentId) {
  const parent = tabEl.parentElement;
  parent.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  tabEl.classList.add('active');

  const container = parent.parentElement;
  container.querySelectorAll('.resume-tab-content').forEach(c => c.classList.add('hidden'));
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
  let translationFields = '';


  if (type === 'project') {
    const images = d.images || [];
    // Image preview generation
    // Images handled in the template literal below


    // Handle URLs
    const urls = d.urls || [];
    // Backward compatibility for old single URL format if urls is empty
    if (urls.length === 0 && d.url) {
      try {
        const parsed = typeof d.url === 'string' ? JSON.parse(d.url) : d.url;
        if (parsed.github) urls.push({ url_type: 'github', url: parsed.github });
        if (parsed.live) urls.push({ url_type: 'live', url: parsed.live });
      } catch {
        urls.push({ url_type: 'live', url: d.url });
      }
    }

    let urlRows = '';
    urls.forEach((u, idx) => {
      urlRows += `
        <div class="url-row" style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
            <select class="form-control" style="width: 120px;" onchange="updateUrlType(this)">
                <option value="live" ${u.url_type === 'live' ? 'selected' : ''}>Live</option>
                <option value="github" ${u.url_type === 'github' ? 'selected' : ''}>GitHub</option>
                <option value="demo" ${u.url_type === 'demo' ? 'selected' : ''}>Demo</option>
                <option value="article" ${u.url_type === 'article' ? 'selected' : ''}>Article</option>
            </select>
            <input type="text" class="form-control" value="${u.url}" placeholder="https://..." onchange="updateUrlValue(this)">
            <button type="button" class="btn" style="background: var(--danger); padding: 0 0.5rem;" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
        </div>
      `;
    });

    typeFields = `
                <div class="form-group">
                    <label class="form-label">Category <span style="color:var(--danger)">*</span></label>
                    <select class="form-control" name="category" required>
                        <option value="">Select a category...</option>
                        <option value="project" ${(d.category || '').toLowerCase() === 'project' ? 'selected' : ''}>Project</option>
                        <option value="work" ${(d.category || '').toLowerCase() === 'work' ? 'selected' : ''}>Work</option>
                        <option value="study" ${(d.category || '').toLowerCase() === 'study' ? 'selected' : ''}>Study</option>
                    </select>
                </div>
                <div class="form-group" style="display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem;">
                    <input type="checkbox" name="is_featured_cv" ${d.is_featured_cv ? 'checked' : ''}>
                    <label class="form-label" style="margin-bottom: 0; cursor: pointer;">Featured in CV</label>
                </div>
                <div class="form-group">
                    <label class="form-label">Tags (comma separated)</label>
                    <input type="text" class="form-control" name="tags" value="${(d.tags || []).map(t => t.name).join(', ')}">
                </div>
                <div class="form-group">
                    <label class="form-label" style="font-weight: 600; margin-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
                        URLS
                        <button type="button" class="btn btn-sm" style="font-size: 0.8rem; padding: 0.2rem 0.5rem;" onclick="addUrlRow()">+ Add URL</button>
                    </label>
                    <div id="url-container">
                        ${urlRows}
                    </div>
                </div>
                <div class="form-group">
                <div class="form-group">
                    <label class="form-label">Images</label>
                    <div id="image-container" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1rem;">
                        ${images.map((img, idx) => `
                            <div class="image-row" style="display: flex; gap: 1rem; padding: 1rem; background: var(--bg-main); border: 1px solid var(--border); border-radius: 0.5rem; align-items: start;">
                                <div style="width: 100px; height: 100px; flex-shrink: 0; overflow: hidden; border-radius: 0.25rem; background: var(--bg-card);">
                                    <img src="${img.url}" style="width: 100%; height: 100%; object-fit: cover;">
                                </div>
                                <div style="flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                                    <input type="hidden" class="img-url" value="${img.url}">
                                    <input type="hidden" class="img-type" value="${img.type || 'image'}">
                                    <div style="grid-column: 1 / -1;">
                                        <label style="font-size: 0.8rem;">Alt Text</label>
                                        <input type="text" class="form-control img-alt" value="${img.alt_text || ''}" placeholder="Alt text">
                                    </div>
                                    <div>
                                        <label style="font-size: 0.8rem;">Width</label>
                                        <input type="number" class="form-control img-width" value="${img.width || ''}" placeholder="Width">
                                    </div>
                                    <div>
                                        <label style="font-size: 0.8rem;">Height</label>
                                        <input type="number" class="form-control img-height" value="${img.height || ''}" placeholder="Height">
                                    </div>
                                    <div style="grid-column: 1 / -1; display: flex; align-items: center; gap: 0.5rem;">
                                        <input type="checkbox" class="img-featured" id="feat-${idx}" ${img.is_featured ? 'checked' : ''}>
                                        <label for="feat-${idx}" style="font-size: 0.9rem; cursor: pointer;">Featured Image</label>
                                    </div>
                                </div>
                                <button type="button" class="btn" style="background: var(--danger); padding: 0.5rem;" onclick="this.closest('.image-row').remove()"><i class="fas fa-times"></i></button>
                            </div>
                        `).join('')}
                    </div>
                    <label class="btn" style="background: var(--bg-card); border: 1px dashed var(--border); width: 100%; justify-content: center;">
                        <i class="fas fa-cloud-upload-alt"></i> Upload Image
                        <input type="file" accept="image/*" hidden onchange="uploadImage(this)">
                    </label>
                </div>
            `;
  } else if (type === 'experience') {
    typeFields = `
                <!-- Company field removed as it is stored in translation title -->
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
                    <input type="date" class="form-control" name="endDate" id="endDate-input" value="${d.end_date ? d.end_date.substring(0, 10) : ''}" ${d.current ? 'disabled' : ''}>
                </div>
                <div class="form-group" style="display: flex; align-items: center; gap: 0.5rem;">
                    <input type="checkbox" name="current" id="current-checkbox" ${d.current ? 'checked' : ''} onchange="document.getElementById('endDate-input').disabled = this.checked; if(this.checked) document.getElementById('endDate-input').value = '';">
                    <label class="form-label" for="current-checkbox" style="margin-bottom: 0; cursor: pointer;">Current Position (Present)</label>
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
    const categories = window.skill_categories || [];
    const options = categories.map(c => {
      const trans = c.translations.find(t => t.lang === 'es');
      const name = trans ? trans.name : c.slug;
      return `<option value="${c.id}" ${d.category_id === c.id ? 'selected' : ''}>${name}</option>`;
    }).join('');

    typeFields = `
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <select class="form-control" name="category_id">
                        <option value="">Select Category...</option>
                        ${options}
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Proficiency (0-100)</label>
                    <input type="number" class="form-control" name="proficiency" value="${d.proficiency || 50}">
                </div>
                <div class="form-group">
                    <label class="form-label">Icon URL</label>
                    <input type="text" class="form-control" name="icon_url" value="${d.icon_url || ''}">
                </div>
                <div class="form-group" style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                        <input type="checkbox" name="is_visible_cv" ${d.is_visible_cv !== false ? 'checked' : ''}>
                        Visible in CV
                    </label>
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                        <input type="checkbox" name="is_visible_portfolio" ${d.is_visible_portfolio !== false ? 'checked' : ''}>
                        Visible in Portfolio
                    </label>
                </div>
            `;
  } else if (type === 'skill-category') {
    typeFields = `
        <div class="form-group">
            <label class="form-label">Slug (ID)</label>
            <input type="text" class="form-control" name="slug" value="${d.slug || ''}" ${d.id ? 'readonly' : ''}>
        </div>
        <div class="form-group">
            <label class="form-label">Order</label>
            <input type="number" class="form-control" name="order" value="${d.order || 0}">
        </div>
      `;

    translationFields = `
            <div class="tabs">
                <div class="tab active" onclick="switchTab(this, 'trans-es')">Spanish</div>
                <div class="tab" onclick="switchTab(this, 'trans-en')">English</div>
            </div>
            
            <div id="trans-es" class="tab-content">
                <div class="form-group">
                    <label class="form-label">Name (ES) <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="name_es" value="${(es.name || '').replace(/"/g, '&quot;')}" required>
                </div>
            </div>

            <div id="trans-en" class="tab-content hidden">
                <div class="form-group">
                    <label class="form-label">Name (EN) <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="name_en" value="${(en.name || '').replace(/"/g, '&quot;')}" required>
                </div>
            </div>
      `;
    return `<form id="edit-form">${commonFields}${typeFields}${translationFields}</form>`;
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

  translationFields = `
            <div class="tabs">
                <div class="tab active" onclick="switchTab(this, 'trans-es')">Spanish</div>
                <div class="tab" onclick="switchTab(this, 'trans-en')">English</div>
            </div>
            
            <div id="trans-es" class="tab-content">
                <div class="form-group">
                    <label class="form-label">${type === 'experience' ? 'Company Name (ES)' : type === 'education' ? 'Degree (ES)' : 'Title/Name (ES)'} <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="${type === 'skill' ? 'name_es' : 'title_es'}" value="${(es.title || es.name || '').replace(/"/g, '&quot;')}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">${type === 'experience' ? 'Role (ES)' : type === 'education' ? 'Field of Study (ES)' : 'Subtitle (ES)'}</label>
                    <input type="text" class="form-control" name="subtitle_es" value="${(es.subtitle || '').replace(/"/g, '&quot;')}">
                </div>
                <div class="form-group">
                    <label class="form-label">Description (ES)</label>
                    <textarea class="form-control" name="description_es" rows="15">${es.description || ''}</textarea>
                </div>
                ${type === 'project' ? `
                <div class="form-group">
                    <label class="form-label">CV Description (ES) <span style="font-size:0.8em; color:var(--accent)">(Optional - Overrides main description in CV)</span></label>
                    <textarea class="form-control" name="cv_description_es" rows="5">${es.cv_description || ''}</textarea>
                </div>
                ` : ''}
            </div>

            <div id="trans-en" class="tab-content hidden">
                <div class="form-group">
                    <label class="form-label">${type === 'experience' ? 'Company Name (EN)' : type === 'education' ? 'Degree (EN)' : 'Title/Name (EN)'} <span style="color:var(--danger)">*</span></label>
                    <input type="text" class="form-control" name="${type === 'skill' ? 'name_en' : 'title_en'}" value="${(en.title || en.name || '').replace(/"/g, '&quot;')}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">${type === 'experience' ? 'Role (EN)' : type === 'education' ? 'Field of Study (EN)' : 'Subtitle (EN)'}</label>
                    <input type="text" class="form-control" name="subtitle_en" value="${(en.subtitle || '').replace(/"/g, '&quot;')}">
                </div>
                <div class="form-group">
                    <label class="form-label">Description (EN)</label>
                    <textarea class="form-control" name="description_en" rows="15">${en.description || ''}</textarea>
                </div>
                ${type === 'project' ? `
                <div class="form-group">
                    <label class="form-label">CV Description (EN) <span style="font-size:0.8em; color:var(--accent)">(Optional - Overrides main description in CV)</span></label>
                    <textarea class="form-control" name="cv_description_en" rows="5">${en.cv_description || ''}</textarea>
                </div>
                ` : ''}
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
      const container = document.getElementById('image-container');
      const div = document.createElement('div');
      // No need to create a wrapper div, we can just append the HTML string if we handle it right, 
      // but sticking to the existing pattern:
      // Actually, the previous code created a wrapper div AND put the .image-row class on it.
      // Let's match the structure exactly.

      div.className = 'image-row';
      div.style.cssText = 'display: flex; gap: 1rem; padding: 1rem; background: var(--bg-main); border: 1px solid var(--border); border-radius: 0.5rem; align-items: start;';

      div.innerHTML = `
            <div style="width: 100px; height: 100px; flex-shrink: 0; overflow: hidden; border-radius: 0.25rem; background: var(--bg-card);">
                <img src="${data.url}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <input type="hidden" class="img-url" value="${data.url}">
                <input type="hidden" class="img-type" value="${data.format === 'gif' ? 'gif' : 'image'}">
                <div style="grid-column: 1 / -1;">
                    <label style="font-size: 0.8rem;">Alt Text</label>
                    <input type="text" class="form-control img-alt" placeholder="Alt text">
                </div>
                <div>
                    <label style="font-size: 0.8rem;">Width</label>
                    <input type="number" class="form-control img-width" value="${data.width || ''}" placeholder="Width">
                </div>
                <div>
                    <label style="font-size: 0.8rem;">Height</label>
                    <input type="number" class="form-control img-height" value="${data.height || ''}" placeholder="Height">
                </div>
                <div style="grid-column: 1 / -1; display: flex; align-items: center; gap: 0.5rem;">
                    <input type="checkbox" class="img-featured" id="feat-new-${Date.now()}">
                    <label for="feat-new-${Date.now()}" style="font-size: 0.9rem; cursor: pointer;">Featured Image</label>
                </div>
            </div>
            <button type="button" class="btn" style="background: var(--danger); padding: 0.5rem;" onclick="deleteUploadedImage(this, '${data.public_id}')"><i class="fas fa-times"></i></button>
      `;
      container.appendChild(div);
      showToast('Image uploaded', 'success');
    } else {
      showToast('Upload failed: ' + (data.error || 'Unknown error'), 'error');
    }
  } catch (e) {
    showToast('Error uploading: ' + e.message, 'error');
  } finally {
    btn.innerHTML = originalText;
    const newInput = btn.querySelector('input');
    if (newInput) newInput.onchange = function () { uploadImage(this); };
  }
}

// removeImage and renderImagePreviews are no longer needed
function removeImage(index) {
  // Deprecated
}
function renderImagePreviews(images) {
  // Deprecated
}

function addUrlRow() {
  const container = document.getElementById('url-container');
  const div = document.createElement('div');
  div.className = 'url-row';
  div.style.cssText = 'display: flex; gap: 0.5rem; margin-bottom: 0.5rem;';
  div.innerHTML = `
        <select class="form-control" style="width: 120px;">
            <option value="live">Live</option>
            <option value="github">GitHub</option>
            <option value="demo">Demo</option>
            <option value="article">Article</option>
        </select>
        <input type="text" class="form-control" placeholder="https://..." >
        <button type="button" class="btn" style="background: var(--danger); padding: 0 0.5rem;" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
  container.appendChild(div);
}

// Data variables - populated by inline script in HTML
const projects = window.projects || [];
const experiences = window.experiences || [];
const education = window.education || [];
const skills = window.skills || [];
const skill_categories = window.skill_categories || [];
const certifications = window.certifications || [];

function editProject(id) { openModal('project', projects.find(p => p.id == id)); }


function editExperience(id) { openModal('experience', experiences.find(e => e.id == id)); }
function editEducation(id) { openModal('education', education.find(e => e.id == id)); }
function editSkill(id) { openModal('skill', skills.find(s => s.id == id)); }
function editSkillCategory(id) { openModal('skill-category', skill_categories.find(c => c.id == id)); }
function editCertification(id) { openModal('certification', certifications.find(c => c.id == id)); }

// API Actions
async function saveItem() {
  const form = document.getElementById('edit-form');
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // Fix checkboxes to be boolean
  form.querySelectorAll('input[type="checkbox"][name]').forEach(cb => {
    data[cb.name] = cb.checked;
  });

  // Process specific fields
  if (data.tags) data.tags = data.tags.split(',').map(t => t.trim());
  if (data.images) {
    try { data.images = JSON.parse(data.images); }
    catch { data.images = []; }
  }

  // Collect URLs
  if (currentType === 'project') {
    const urlRows = document.querySelectorAll('#url-container .url-row');
    const urls = [];
    urlRows.forEach((row, idx) => {
      const type = row.querySelector('select').value;
      const url = row.querySelector('input').value;
      if (url) {
        urls.push({ type, url, order: idx });
      }
    });
    data.urls = urls;
  }

  // Collect Images
  if (currentType === 'project') {
    const imgRows = document.querySelectorAll('#image-container .image-row');
    const images = [];
    imgRows.forEach((row, idx) => {
      images.push({
        url: row.querySelector('.img-url').value,
        type: row.querySelector('.img-type').value,
        alt_text: row.querySelector('.img-alt').value,
        width: row.querySelector('.img-width').value ? parseInt(row.querySelector('.img-width').value) : null,
        height: row.querySelector('.img-height').value ? parseInt(row.querySelector('.img-height').value) : null,
        is_featured: row.querySelector('.img-featured').checked,
        order: idx
      });
    });
    data.images = images;
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

async function deleteUploadedImage(btn, publicId) {
  if (publicId && publicId !== 'undefined' && publicId !== 'null') {
    try {
      const res = await fetch('/admin/delete-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ public_id: publicId })
      });

      if (!res.ok) {
        console.error('Failed to delete image from Cloudinary');
      }
    } catch (e) {
      console.error('Error deleting image:', e);
    }
  }
  btn.closest('.image-row').remove();
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
    // Add phone to location object
    if (data.phone) {
      data.location.phone = data.phone;
      delete data.phone; // Remove from top-level data
    }
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
      const err = await res.json();
      showToast(err.error || 'Error saving profile', 'error');
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


// GitHub Import Logic
function openGitHubImport() {
  document.getElementById('github-modal').classList.add('active');
  document.getElementById('github-url-input').value = '';
  document.getElementById('github-error').style.display = 'none';
  document.getElementById('github-loading').style.display = 'none';
}

function closeGitHubModal() {
  document.getElementById('github-modal').classList.remove('active');
}

async function startGitHubImport() {
  console.log("Starting GitHub Import...");
  const urlInput = document.getElementById('github-url-input');
  const modelSelect = document.getElementById('github-model-select');
  const errorDiv = document.getElementById('github-error');
  const loadingDiv = document.getElementById('github-loading');
  const statusLog = document.getElementById('github-status-log');
  const url = urlInput.value.trim();

  // Safe access to model value
  const modelName = modelSelect ? modelSelect.value : 'gemini-2.0-flash';

  if (!url) {
    errorDiv.innerText = 'Please enter a GitHub URL';
    errorDiv.style.display = 'block';
    return;
  }

  // Reset UI
  errorDiv.style.display = 'none';
  loadingDiv.style.display = 'block';
  if (statusLog) statusLog.innerHTML = ''; // Clear previous logs
  urlInput.disabled = true;
  if (modelSelect) modelSelect.disabled = true;

  // Helper to add status logs with typing effect
  const addLog = async (message) => {
    if (!statusLog) return; // Skip if element missing
    const p = document.createElement('div');
    p.style.marginBottom = '4px';
    p.innerHTML = `<span style="color: var(--primary)">></span> ${message}`;
    statusLog.appendChild(p);
    statusLog.scrollTop = statusLog.scrollHeight;
    // Simple delay to simulate processing steps if they were real-time events
    await new Promise(r => setTimeout(r, 500));
  };

  try {
    await addLog("Initializing AI Agent...");
    await addLog(`Selected Model: ${modelName}`);
    await addLog("Connecting to GitHub API...");

    // Simulate progress for better UX (since the backend call is monolithic)
    const progressInterval = setInterval(() => {
      const messages = [
        "Fetching repository structure...",
        "Reading README.md...",
        "Analyzing code patterns...",
        "Identifying tech stack...",
        "Extracting media assets...",
        "Generating project metadata...",
        "Translating content (EN/ES)...",
        "Creating Mermaid diagrams..."
      ];
      const msg = messages[Math.floor(Math.random() * messages.length)];
      addLog(msg);
    }, 2500);

    const response = await fetch('/admin/ai/import-github', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        github_url: url,
        model_name: modelName
      })
    });

    clearInterval(progressInterval);
    await addLog("Processing complete. Finalizing...");

    const result = await response.json();

    if (result.success) {
      closeGitHubModal();

      const data = result.data;

      // Map AI data to form structure
      const projectData = {
        category: data.category,
        tags: (data.tags || []).map(t => ({ name: t })),
        urls: (data.urls || []).map((u, i) => ({ url_type: u.type, url: u.url, order: i })),
        translations: [
          {
            lang: 'en',
            title: data.title,
            subtitle: data.subtitle,
            description: data.translations.en.description
          },
          {
            lang: 'es',
            title: data.title, // Use English title as fallback
            subtitle: data.translations.es.subtitle || data.subtitle,
            description: data.translations.es.description
          }
        ],
        images: []
      };

      // Handle Media
      if (data.media) {
        if (data.media.gif_url) {
          projectData.images.push({
            url: data.media.gif_url,
            type: 'gif',
            alt_text: 'Project Demo',
            is_featured: false,
            width: null, height: null
          });
        }
        if (data.media.image_url) {
          projectData.images.push({
            url: data.media.image_url,
            type: 'image',
            alt_text: 'Project Screenshot',
            is_featured: true,
            width: null, height: null
          });
        }
      }

      // Open the project modal with this data
      openModal('project', projectData);

      showToast('Project analyzed successfully!', 'success');

    } else {
      throw new Error(result.error || 'Unknown error');
    }
  } catch (e) {
    errorDiv.innerText = 'Import failed: ' + e.message;
    errorDiv.style.display = 'block';
  } finally {
    loadingDiv.style.display = 'none';
    urlInput.disabled = false;
    if (modelSelect) modelSelect.disabled = false;
  }
}
