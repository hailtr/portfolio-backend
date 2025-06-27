function addCustomLanguage() {
  const container = document.getElementById('extra-translations');

  const lang = prompt("Introduce el código del nuevo idioma (ej: en, es, fr):");
  if (!lang || !/^[a-z]{2}$/.test(lang)) {
    alert("Código inválido. Usa dos letras minúsculas.");
    return;
  }

  // Verifica que no exista ya
  if (document.querySelector(`[name='lang_${lang}']`)) {
    alert("Este idioma ya está agregado.");
    return;
  }

  const block = document.createElement('div');
  block.className = "translation-block border rounded-lg p-4 bg-white shadow space-y-4 mt-4";

  block.innerHTML = `
    <h3 class="text-lg font-semibold mb-2">Traducción: ${lang.toUpperCase()}</h3>
    <input type="hidden" name="lang_${lang}" value="${lang}">

    <label class="block">Título
      <input type="text" name="title_${lang}" class="w-full border px-3 py-2 rounded mt-1">
    </label>

    <label class="block">Subtítulo
      <input type="text" name="subtitle_${lang}" class="w-full border px-3 py-2 rounded mt-1">
    </label>

    <label class="block">Descripción
      <textarea name="description_${lang}" class="w-full border px-3 py-2 rounded mt-1"></textarea>
    </label>

    <label class="block">Resumen
      <textarea name="summary_${lang}" class="w-full border px-3 py-2 rounded mt-1"></textarea>
    </label>

    <label class="block">Contenido extra (JSON)
      <textarea name="content_${lang}" class="w-full border px-3 py-2 rounded mt-1">{}</textarea>
    </label>
  `;

  container.appendChild(block);
}

document.getElementById('delete-form').addEventListener('submit', function (e) {
  const select = document.getElementById('project-select');
  const id = select.value;
  if (!id) {
    alert('Selecciona un proyecto para eliminar.');
    e.preventDefault();
    return;
  }

  this.action = `/admin/delete/${id}`;
});
