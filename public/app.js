const state = {
  articles: [],
  queue: [],
  selectedCity: 'all',
  selectedCategory: 'all',
  searchQuery: '',
  activeArticle: null,
};

async function fetchInitialData() {
  try {
    let artRes = await fetch('/api/articles').catch(() => ({ ok: false }));
    if (!artRes || !artRes.ok) artRes = await fetch('data/articles.json');
    let queueRes = await fetch('/api/queue').catch(() => ({ ok: false }));
    if (!queueRes || !queueRes.ok) queueRes = await fetch('data/keyword_queue.json');
    state.articles = await artRes.json();
    state.queue = await queueRes.json();
    renderAll();
  } catch (err) {
    console.error('Error cargando datos:', err);
  }
}

function renderAll() {
  renderStats();
  renderFeaturedHero();
  renderArticlesGrid();
  renderKeywordQueue();
}

function renderStats() {
  const totalEl = document.getElementById('stat-total-articles');
  if (totalEl) {
    totalEl.textContent = `${state.articles.length} Guías`;
  }
}

function renderFeaturedHero() {
  const heroContainer = document.getElementById('hero-featured-card');
  if (!heroContainer || state.articles.length === 0) return;

  const featured = state.articles[0];
  heroContainer.innerHTML = `
    <img src="${featured.image}" alt="${featured.title}" class="hero-featured-img" />
    <div class="hero-featured-body">
      <div class="hero-featured-meta">
        <span>${featured.city.toUpperCase()}</span>
        <span>·</span>
        <span>${featured.categoryIcon} ${featured.category}</span>
        ${featured.generatedByAgent ? '<span class="card-seo-badge">⚡ Recién creado por Agente</span>' : '<span class="card-seo-badge">Top SEO</span>'}
      </div>
      <h2 class="hero-featured-heading">${featured.title}</h2>
      <p style="font-size: 0.86rem; color: var(--ink-secondary); margin-bottom: 0.65rem;">
        ${featured.excerpt}
      </p>
      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: var(--ink-muted);">
        <span>📍 ${featured.neighborhoods.join(', ')}</span>
        <strong style="color: var(--terracotta);">Leer guía completa →</strong>
      </div>
    </div>
  `;
  heroContainer.onclick = () => openArticleModal(featured.id);
}

function getFilteredArticles() {
  return state.articles.filter((art) => {
    const matchesCity = state.selectedCity === 'all' || art.city === state.selectedCity;
    const matchesCategory = state.selectedCategory === 'all' || art.category === state.selectedCategory;
    const q = state.searchQuery.trim().toLowerCase();
    const matchesQuery =
      !q ||
      art.title.toLowerCase().includes(q) ||
      art.excerpt.toLowerCase().includes(q) ||
      art.city.toLowerCase().includes(q) ||
      art.neighborhoods.some((n) => n.toLowerCase().includes(q)) ||
      art.targetKeyword.toLowerCase().includes(q);
    return matchesCity && matchesCategory && matchesQuery;
  });
}

function renderArticlesGrid() {
  const grid = document.getElementById('articles-grid-container');
  if (!grid) return;

  const filtered = getFilteredArticles();
  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; background: var(--bg-elevated); border: 1px solid var(--border-hairline); border-radius: var(--radius-md);">
        <p style="font-size: 1.05rem; margin-bottom: 0.75rem;">No hay artículos con ese filtro todavía.</p>
        <button type="button" class="open-agent-studio-btn" id="empty-state-agent-btn">
          🤖 Pedirle al Agente que escriba uno ahora
        </button>
      </div>
    `;
    const btn = document.getElementById('empty-state-agent-btn');
    if (btn) btn.onclick = openAgentStudioModal;
    return;
  }

  grid.innerHTML = filtered
    .map(
      (art) => `
      <article class="article-card" data-article-id="${art.id}" id="card-${art.id}">
        <div class="card-image-wrap">
          <img src="${art.image}" alt="${art.title}" class="card-image" loading="lazy" />
          <span class="card-city-tag">${art.city}</span>
          <span class="card-price-tag">${art.priceRange}</span>
        </div>
        <div class="card-body">
          <div class="card-meta-top">
            <span class="card-category">${art.categoryIcon} ${art.category}</span>
            <span class="card-seo-badge" title="Volumen de búsqueda en Google">🔍 ${art.searchVolume}</span>
          </div>
          <h3 class="card-title">${art.title}</h3>
          <p class="card-excerpt">${art.excerpt}</p>
          <div class="card-footer">
            <span class="card-neighborhoods">📍 ${art.neighborhoods.join(' · ')}</span>
            <span class="card-read-link">Ver plan →</span>
          </div>
        </div>
      </article>
    `
    )
    .join('');

  grid.querySelectorAll('.article-card').forEach((card) => {
    card.addEventListener('click', () => {
      openArticleModal(card.getAttribute('data-article-id'));
    });
  });
}

function openArticleModal(articleId) {
  const art = state.articles.find((a) => a.id === articleId);
  if (!art) return;
  state.activeArticle = art;

  const modal = document.getElementById('article-reader-modal');
  const body = document.getElementById('article-reader-body');

  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: art.faqs.map((f) => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.answer,
      },
    })),
  };

  body.innerHTML = `
    <!-- Panel Rayos-X SEO (Oculto por defecto, visible al pulsar el botón superior) -->
    <div class="seo-xray-panel" id="seo-xray-panel">
      <div style="margin-bottom: 0.85rem; border-bottom: 1px solid hsla(37,38%,94%,0.18); padding-bottom: 0.5rem;">
        <strong style="color: #fff; font-size: 0.88rem;">🔬 RADIOLOGÍA SEO DEL ARTÍCULO (Generado automáticamente para Google)</strong>
      </div>
      <div class="seo-xray-grid">
        <div class="seo-xray-item">
          <strong>Palabra Clave Atacada (Long-Tail)</strong>
          <span>"${art.targetKeyword}"</span>
        </div>
        <div class="seo-xray-item">
          <strong>Volumen Mensual / Competencia</strong>
          <span>${art.searchVolume} · Dif: ${art.keywordDifficulty}</span>
        </div>
        <div class="seo-xray-item">
          <strong>URL Amigable (Slug SEO)</strong>
          <span>queplanhoy.es/planes/${art.slug}</span>
        </div>
      </div>
      <div class="seo-xray-item" style="margin-bottom: 0.75rem;">
        <strong>Etiqueta &lt;title&gt; en Google</strong>
        <span>${art.metaTitle}</span>
      </div>
      <div class="seo-xray-item" style="margin-bottom: 0.75rem;">
        <strong>Etiqueta &lt;meta name="description"&gt;</strong>
        <span>${art.metaDescription}</span>
      </div>
      <div class="seo-xray-item">
        <strong>Datos Estructurados Schema.org (JSON-LD FAQPage para salir desplegado en Google)</strong>
        <pre style="background: rgba(0,0,0,0.35); padding: 0.65rem; border-radius: 6px; overflow-x: auto; margin-top: 0.35rem; font-size: 0.72rem;">${JSON.stringify(faqSchema, null, 2)}</pre>
      </div>
    </div>

    <div style="display: flex; gap: 0.6rem; align-items: center; font-size: 0.82rem; font-weight: 700; color: var(--terracotta); margin-bottom: 0.5rem;">
      <span>${art.city.toUpperCase()}</span>
      <span>·</span>
      <span>${art.categoryIcon} ${art.category}</span>
      <span>·</span>
      <span style="color: var(--ink-muted); font-weight: 500;">Lectura: ${art.readTime} · Publicado: ${art.publishedAt}</span>
    </div>

    <h1 id="reader-article-title" style="font-family: var(--font-serif); font-size: clamp(1.65rem, 3vw, 2.3rem); line-height: 1.18; margin-bottom: 0.85rem;">
      ${art.title}
    </h1>

    <p style="font-size: 1.05rem; color: var(--ink-secondary); margin-bottom: 1rem;">
      ${art.excerpt}
    </p>

    <img src="${art.image}" alt="${art.title}" class="reader-hero-img" />

    <!-- Secciones con locales reales, direcciones y precios -->
    ${art.sections
      .map(
        (sec) => `
      <section class="reader-section">
        <h2>${sec.heading}</h2>
        <div class="venue-meta-bar">
          <span>📍 <strong>Dónde:</strong> ${sec.location}</span>
          <span>💶 <strong>Precio real:</strong> ${sec.price}</span>
        </div>
        <p style="font-size: 0.98rem; color: var(--ink-primary);">${sec.content}</p>
      </section>
    `
      )
      .join('')}

    <!-- Bloque de Monetización de Afiliación Nativa -->
    <div class="affiliate-callout">
      <div style="flex: 1; min-width: 240px;">
        <span class="affiliate-badge">💡 ${art.affiliate.badge} · Partner: ${art.affiliate.partner}</span>
        <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 0.35rem;">
          ${art.affiliate.title}
        </h3>
        <p style="font-size: 0.88rem; color: var(--ink-secondary); margin-bottom: 0.45rem;">
          ${art.affiliate.description}
        </p>
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--olive); font-weight: 600;">
          💰 Cómo ganas dinero aquí: ${art.affiliate.commissionNote}
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.4rem;">${art.affiliate.price}</div>
        <button type="button" class="affiliate-cta-btn" id="affiliate-demo-cta" onclick="alert('¡Así funciona la monetización! En tu web real, este botón lleva tu enlace de afiliado de ${art.affiliate.partner}. Si el lector reserva, recibes entre un 8% y un 15% de comisión automáticamente.')">
          ${art.affiliate.ctaText}
        </button>
      </div>
    </div>

    <!-- Preguntas Frecuentes (SEO FAQ Schema) -->
    <section style="margin-top: 2rem;">
      <h2 style="font-family: var(--font-serif); font-size: 1.4rem; margin-bottom: 1rem;">
        Preguntas frecuentes sobre ${art.targetKeyword}
      </h2>
      ${art.faqs
        .map(
          (faq) => `
        <div style="background: var(--bg-paper); border: 1px solid var(--border-hairline); border-radius: var(--radius-sm); padding: 1rem 1.2rem; margin-bottom: 0.75rem;">
          <h3 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem;">❓ ${faq.question}</h3>
          <p style="font-size: 0.9rem; color: var(--ink-secondary);">${faq.answer}</p>
        </div>
      `
        )
        .join('')}
    </section>
  `;

  modal.classList.add('open');
}

function renderKeywordQueue() {
  const container = document.getElementById('keyword-queue-container');
  if (!container) return;

  container.innerHTML = state.queue
    .map(
      (item) => `
      <div class="queue-item ${item.status === 'published' ? 'published' : ''}">
        <div>
          <div style="display: flex; gap: 0.5rem; align-items: center; font-size: 0.76rem; font-weight: 700; color: var(--terracotta); margin-bottom: 0.2rem;">
            <span>${item.city.toUpperCase()}</span>
            <span>·</span>
            <span>${item.categoryIcon} ${item.category}</span>
            <span>·</span>
            <span style="font-family: var(--font-mono); color: var(--olive);">${item.searchVolume} (Dif: ${item.keywordDifficulty})</span>
          </div>
          <div style="font-weight: 700; font-size: 0.95rem;">${item.suggestedTitle}</div>
          <div style="font-size: 0.78rem; color: var(--ink-muted);">
            Keyword objetivo: <code>"${item.keyword}"</code> · Monetización: ${item.affiliateHook}
          </div>
        </div>
        <div>
          ${
            item.status === 'published'
              ? '<span class="card-seo-badge">✅ Ya publicado</span>'
              : `<span class="mono-tag">⏳ ${item.scheduledFor}</span>`
          }
        </div>
      </div>
    `
    )
    .join('');
}

function openAgentStudioModal() {
  const modal = document.getElementById('agent-studio-modal');
  if (modal) modal.classList.add('open');
}

async function triggerNextQueueAgent() {
  const logEl = document.getElementById('agent-log-output');
  const btn = document.getElementById('run-next-queue-btn');
  if (!logEl || !btn) return;

  btn.disabled = true;
  logEl.classList.add('active');
  logEl.textContent =
    '▶ [Paso 1/4] Analizando cola de palabras clave Long-Tail de baja competencia...\n' +
    '▶ [Paso 2/4] Consultando base verificada de direcciones, paradas de Metro y precios reales...\n' +
    '▶ [Paso 3/4] Redactando estructura SEO (H1, H2, Meta-Tags, Enlazado interno y Schema FAQPage)...';

  try {
    const res = await fetch('/api/agent/run-next', { method: 'POST' });
    const data = await res.json();
    logEl.textContent +=
      `\n✅ [Paso 4/4] ¡Artículo publicado con éxito!\n` +
      `   • Título: ${data.article.title}\n` +
      `   • URL: /planes/${data.article.slug}\n` +
      `   • Sitemap XML actualizado para Google Search Console.`;

    await fetchInitialData();
    setTimeout(() => {
      document.getElementById('agent-studio-modal').classList.remove('open');
      openArticleModal(data.article.id);
    }, 1400);
  } catch (e) {
    logEl.textContent += `\n❌ Error ejecutando el agente: ${e.message}`;
  } finally {
    btn.disabled = false;
  }
}

async function triggerCustomAgent(e) {
  e.preventDefault();
  const city = document.getElementById('custom-city-select').value;
  const category = document.getElementById('custom-category-select').value;
  const keyword = document.getElementById('custom-keyword-input').value.trim();
  if (!keyword) return;

  const logEl = document.getElementById('agent-log-output');
  logEl.classList.add('active');
  logEl.textContent =
    `▶ [Paso 1/4] Investigando palabra clave "${keyword}" en ${city}...\n` +
    `▶ [Paso 2/4] Seleccionando locales reales, precios y enlaces del clúster de ${city}...\n` +
    `▶ [Paso 3/4] Generando artículo optimizado y bloque de afiliado...`;

  try {
    const res = await fetch('/api/agent/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ city, category, keyword }),
    });
    const data = await res.json();
    logEl.textContent +=
      `\n✅ [Paso 4/4] ¡Nuevo artículo publicado!\n` +
      `   • Título: ${data.article.title}\n` +
      `   • URL: /planes/${data.article.slug}`;

    document.getElementById('custom-keyword-input').value = '';
    await fetchInitialData();
    setTimeout(() => {
      document.getElementById('agent-studio-modal').classList.remove('open');
      openArticleModal(data.article.id);
    }, 1300);
  } catch (err) {
    logEl.textContent += `\n❌ Error: ${err.message}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  fetchInitialData();

  // Filtros de ciudad
  document.querySelectorAll('.city-filter-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.city-filter-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      state.selectedCity = btn.getAttribute('data-city');
      renderArticlesGrid();
    });
  });

  // Filtros de categoría ("El Triángulo de Oro")
  document.querySelectorAll('.style-pill-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.style-pill-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      state.selectedCategory = btn.getAttribute('data-category');
      renderArticlesGrid();
    });
  });

  // Buscador en vivo
  const searchInput = document.getElementById('article-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      renderArticlesGrid();
    });
  }

  // Botones para abrir el Estudio del Agente
  ['open-agent-modal-btn', 'top-trigger-agent-btn', 'bottom-open-agent-btn'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', openAgentStudioModal);
  });

  // Cerrar modales
  document.getElementById('close-reader-modal-btn').addEventListener('click', () => {
    document.getElementById('article-reader-modal').classList.remove('open');
  });
  document.getElementById('close-agent-modal-btn').addEventListener('click', () => {
    document.getElementById('agent-studio-modal').classList.remove('open');
  });

  // Toggle Rayos-X SEO
  document.getElementById('toggle-seo-xray-btn').addEventListener('click', () => {
    const panel = document.getElementById('seo-xray-panel');
    if (panel) panel.classList.toggle('visible');
  });

  // Ejecutar agente desde la cola o formulario personalizado
  document.getElementById('run-next-queue-btn').addEventListener('click', triggerNextQueueAgent);
  document.getElementById('custom-agent-form').addEventListener('submit', triggerCustomAgent);
});
