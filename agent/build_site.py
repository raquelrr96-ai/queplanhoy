#!/usr/bin/env python3
"""Generador de Sitio Estático (SSG) para ¿Qué Plan Hoy? (queplanhoy.es).

Diseñado con los estándares E-E-A-T de Google (Experience, Expertise, Authoritativeness,
Trustworthiness) y Helpful Content:
  - /index.html (Portada general)
  - /madrid/, /barcelona/, /valencia/, /sevilla/, /toledo/ (Páginas de ciudad)
  - /<ciudad>/<slug>/ (Páginas de cada guía con Tabla Resumen para Featured Snippets,
    Schema.org Article + FAQPage + BreadcrumbList y Ficha de Verificación Editorial)
  - /sobre-nosotros/ (Página de transparencia editorial y autoría para E-E-A-T y afiliados)
"""

from datetime import date
import html
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "data", "articles.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
SITE_URL = "https://queplanhoy.es"

CITIES = {
    "Madrid": {
        "slug": "madrid",
        "h1": "Planes en Madrid: qué hacer hoy fuera de lo típico",
        "metaTitle": (
            "Planes en Madrid Hoy: Originales, Gratis y en Pareja (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "Descubre los mejores planes en Madrid para hoy y este fin de"
            " semana: ideas por menos de 10 €, citas originales en pareja,"
            " jardines ocultos y cultura."
        ),
        "intro": (
            "Nuestra selección de rincones secretos, talleres creativos,"
            " jardines gratuitos y planes en pareja en Madrid con precios"
            " exactos y paradas de Metro."
        ),
    },
    "Barcelona": {
        "slug": "barcelona",
        "h1": "Planes en Barcelona: miradores, citas y rincones sin colas",
        "metaTitle": (
            "Planes en Barcelona Hoy: Originales, Gratis y en Pareja (2026) |"
            " Qué Plan Hoy"
        ),
        "metaDesc": (
            "Guía local de planes diferentes, baratos y en pareja en Barcelona:"
            " miradores alternativos a los Bunkers, jardines históricos y rutas"
            " por barrios."
        ),
        "intro": (
            "Explora una Barcelona lejos de las aglomeraciones: desde jardines"
            " neoclásicos gratuitos hasta terrazas con vistas al Mediterráneo y"
            " planes en pareja."
        ),
    },
    "Valencia": {
        "slug": "valencia",
        "h1": "Planes en Valencia: atardeceres, huerta y cultura local",
        "metaTitle": (
            "Planes en Valencia Hoy: Originales, Gratis y en Pareja (2026) |"
            " Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué hacer hoy en Valencia? Planes diferentes, baratos y en"
            " pareja: puestas de sol en barca en L'Albufera, rutas por la"
            " huerta, El Cabanyal y Ruzafa."
        ),
        "intro": (
            "Los mejores planes para disfrutar de Valencia todo el año:"
            " escapadas en autobús urbano a L'Albufera, jardines escondidos y"
            " tapeo en barrios marineros."
        ),
    },
    "Sevilla": {
        "slug": "sevilla",
        "h1": "Planes en Sevilla: casas-palacio, patios y rutas al atardecer",
        "metaTitle": (
            "Planes en Sevilla Hoy: Originales, Gratis y en Pareja (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "Descubre planes originales, gratis y en pareja en Sevilla:"
            " casas-palacio mudéjares sin colas, atardeceres en Triana y"
            " callejuelas de Santa Cruz."
        ),
        "intro": (
            "Vive Sevilla con ojos locales: palacios gratuitos, rutas al"
            " anochecer por la antigua judería y planes auténticos en Triana y"
            " la Calle Feria."
        ),
    },
    "Toledo": {
        "slug": "toledo",
        "h1": "Planes en Toledo: escapadas, rutas nocturnas y rincones ocultos",
        "metaTitle": (
            "Planes en Toledo: Qué Hacer de Día, de Noche y en Pareja | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "Guía de planes diferentes en Toledo a 33 minutos de Madrid: ruta"
            " de cobertizos iluminados, baños árabes en pareja, senda del Tajo"
            " y subterráneos."
        ),
        "intro": (
            "A solo 33 minutos en tren desde Madrid: descubre qué hacer en"
            " Toledo cuando se marchan los autobuses turísticos, desde"
            " pasadizos medievales hasta baños árabes."
        ),
    },
}


def render_head(
    title: str,
    description: str,
    canonical_url: str,
    root_prefix: str,
    json_ld_list: list,
    og_image: str = "",
) -> str:
  ld_scripts = "\n".join(
      '<script type="application/ld+json">\n'
      + json.dumps(ld, ensure_ascii=False, indent=2)
      + "\n</script>"
      for ld in json_ld_list
  )
  og_img_tag = (
      f'<meta property="og:image" content="{html.escape(og_image)}" />'
      if og_image
      else ""
  )
  return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{canonical_url}" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:site_name" content="Qué Plan Hoy" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(description)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_url}" />
  {og_img_tag}
  <link rel="sitemap" type="application/xml" title="Sitemap" href="{root_prefix}sitemap.xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root_prefix}index.css" />
  {ld_scripts}
</head>"""


def render_header(root_prefix: str, active_city: str = "all") -> str:
  nav_items = [
      (
          "all",
          "Todas las ciudades",
          f"{root_prefix}index.html" if root_prefix else "./",
      ),
      ("Madrid", "Madrid", f"{root_prefix}madrid/"),
      ("Barcelona", "Barcelona", f"{root_prefix}barcelona/"),
      ("Valencia", "Valencia", f"{root_prefix}valencia/"),
      ("Sevilla", "Sevilla", f"{root_prefix}sevilla/"),
      ("Toledo", "Toledo", f"{root_prefix}toledo/"),
  ]
  links_html = []
  for key, label, href in nav_items:
    active_cls = " active" if key == active_city else ""
    links_html.append(
        f'<a href="{href}" class="city-filter-btn{active_cls}"'
        f' id="nav-{key.lower()}" style="text-decoration:none;">{label}</a>'
    )

  return f"""
  <div class="top-utility-bar">
    <div class="top-utility-inner">
      <div class="agent-status-indicator" style="font-family: var(--font-sans); color: var(--bg-paper);">
        <span>✨ Guía local de planes originales en España</span>
      </div>
      <div class="utility-actions">
        <a href="{root_prefix}madrid/" class="utility-link-btn">Madrid</a>
        <a href="{root_prefix}barcelona/" class="utility-link-btn">Barcelona</a>
        <a href="{root_prefix}valencia/" class="utility-link-btn">Valencia</a>
        <a href="{root_prefix}sevilla/" class="utility-link-btn">Sevilla</a>
        <a href="{root_prefix}toledo/" class="utility-link-btn">Toledo</a>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="header-inner">
      <a href="{root_prefix if root_prefix else './'}" class="brand-logo" id="brand-home-link">
        <span class="brand-name">¿Qué<span>Plan</span>Hoy?</span>
        <span class="brand-tagline">Madrid · Barcelona · Valencia · Sevilla · Toledo</span>
      </a>
      <nav class="city-nav" aria-label="Navegación por ciudades">
        {''.join(links_html)}
      </nav>
    </div>
  </header>"""


def render_footer(root_prefix: str) -> str:
  return f"""
  <footer class="site-footer">
    <div style="max-width: var(--container-max); margin: 0 auto; display: flex; flex-direction: column; gap: 0.75rem; align-items: center;">
      <div style="font-family: var(--font-serif); font-size: 1.25rem; color: var(--ink-primary); font-weight: 700;">
        ¿Qué<span style="color: var(--terracotta); font-style: italic;">Plan</span>Hoy?
      </div>
      <p>Guía independiente de planes diferentes, gratuitos y citas en pareja con direcciones y precios reales.</p>
      <nav aria-label="Enlaces de ciudades y criterio editorial" style="display: flex; gap: 1.25rem; flex-wrap: wrap; justify-content: center; margin-top: 0.25rem;">
        <a href="{root_prefix}madrid/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Planes en Madrid</a>
        <a href="{root_prefix}barcelona/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Planes en Barcelona</a>
        <a href="{root_prefix}valencia/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Planes en Valencia</a>
        <a href="{root_prefix}sevilla/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Planes en Sevilla</a>
        <a href="{root_prefix}toledo/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Planes en Toledo</a>
        <span>·</span>
        <a href="{root_prefix}sobre-nosotros/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Sobre Nosotros y Criterio Editorial</a>
      </nav>
      <p style="font-size: 0.78rem; margin-top: 0.5rem;">© {date.today().year} Qué Plan Hoy · Selección verificada en España.</p>
    </div>
  </footer>"""


def render_article_card(art: dict, root_prefix: str) -> str:
  city_slug = CITIES.get(art["city"], {"slug": art["city"].lower()})["slug"]
  article_href = f"{root_prefix}{city_slug}/{art['slug']}/"
  img_src = f"{root_prefix}{art['image'].lstrip('/')}"
  img_alt = art.get("imageAlt", art["title"])
  return f"""
  <article class="article-card" data-category="{html.escape(art['category'])}" data-search="{html.escape((art['title'] + ' ' + art['excerpt'] + ' ' + ' '.join(art['neighborhoods'])).lower())}">
    <a href="{article_href}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
      <div class="card-image-wrap">
        <img src="{img_src}" alt="{html.escape(img_alt)}" class="card-image" loading="lazy" width="640" height="360" />
        <span class="card-city-tag">{html.escape(art['city'])}</span>
        <span class="card-price-tag">{html.escape(art['priceRange'])}</span>
      </div>
      <div class="card-body">
        <div class="card-meta-top">
          <span class="card-category">{art['categoryIcon']} {html.escape(art['category'])}</span>
          <span style="color: var(--ink-muted); font-size: 0.76rem;">⏱ {html.escape(art['readTime'])} de lectura</span>
        </div>
        <h2 class="card-title" style="font-size: 1.25rem;">{html.escape(art['title'])}</h2>
        <p class="card-excerpt">{html.escape(art['excerpt'])}</p>
        <div class="card-footer">
          <span class="card-neighborhoods">📍 {html.escape(' · '.join(art['neighborhoods']))}</span>
          <span class="card-read-link">Leer guía →</span>
        </div>
      </div>
    </a>
  </article>"""


def render_filter_script() -> str:
  return """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const pills = document.querySelectorAll('.style-pill-btn');
      const searchInput = document.getElementById('article-search-input');
      const cards = document.querySelectorAll('.article-card');
      let currentCat = 'all';
      let currentQuery = '';

      function applyFilters() {
        cards.forEach(card => {
          const cat = card.getAttribute('data-category');
          const text = card.getAttribute('data-search') || '';
          const matchCat = currentCat === 'all' || cat === currentCat;
          const matchQuery = !currentQuery || text.includes(currentQuery);
          card.style.display = (matchCat && matchQuery) ? 'flex' : 'none';
        });
      }

      pills.forEach(btn => {
        btn.addEventListener('click', () => {
          pills.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentCat = btn.getAttribute('data-category');
          applyFilters();
        });
      });

      if (searchInput) {
        searchInput.addEventListener('input', e => {
          currentQuery = e.target.value.trim().toLowerCase();
          applyFilters();
        });
      }
    });
  </script>"""


def build_listing_page(
    articles: list,
    output_path: str,
    title: str,
    description: str,
    canonical_url: str,
    h1: str,
    subtitle: str,
    kicker: str,
    root_prefix: str,
    active_city: str,
):
  featured = articles[0] if articles else None
  featured_html = ""
  if featured:
    f_city_slug = CITIES.get(
        featured["city"], {"slug": featured["city"].lower()}
    )["slug"]
    f_href = f"{root_prefix}{f_city_slug}/{featured['slug']}/"
    f_img = f"{root_prefix}{featured['image'].lstrip('/')}"
    f_alt = featured.get("imageAlt", featured["title"])
    featured_html = f"""
      <a href="{f_href}" class="hero-featured-card" style="text-decoration: none; color: inherit;">
        <img src="{f_img}" alt="{html.escape(f_alt)}" class="hero-featured-img" width="640" height="360" />
        <div class="hero-featured-body">
          <div class="hero-featured-meta">
            <span>{html.escape(featured['city'].upper())}</span>
            <span>·</span>
            <span>{featured['categoryIcon']} {html.escape(featured['category'])}</span>
            <span>·</span>
            <span style="color: var(--ink-muted);">{html.escape(featured['priceRange'])}</span>
          </div>
          <h2 class="hero-featured-heading">{html.escape(featured['title'])}</h2>
          <p style="font-size: 0.88rem; color: var(--ink-secondary); margin-bottom: 0.65rem;">
            {html.escape(featured['excerpt'])}
          </p>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--ink-muted);">
            <span>📍 {html.escape(', '.join(featured['neighborhoods']))}</span>
            <strong style="color: var(--terracotta);">Leer guía completa →</strong>
          </div>
        </div>
      </a>"""

  cards_html = "\n".join(
      render_article_card(a, root_prefix) for a in articles
  )

  schema_ld = [{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": title,
      "description": description,
      "url": canonical_url,
  }]

  page_html = f"""{render_head(title, description, canonical_url, root_prefix, schema_ld)}
<body>
  {render_header(root_prefix, active_city)}

  <main class="main-container">
    <section class="editorial-hero" aria-labelledby="main-hero-heading">
      <div class="hero-copy">
        <span class="hero-kicker">{html.escape(kicker)}</span>
        <h1 class="hero-title" id="main-hero-heading">{html.escape(h1)}</h1>
        <p class="hero-subtitle">{html.escape(subtitle)}</p>
        <div class="hero-QuickStats">
          <div class="stat-item">
            <span class="stat-value">💸 Gratis y Baratos</span>
            <span class="stat-label">Ideas por menos de 10 €</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">✨ Planes Diferentes</span>
            <span class="stat-label">Para salir de la rutina</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">❤️ En Pareja</span>
            <span class="stat-label">Citas y escapadas con encanto</span>
          </div>
        </div>
      </div>
      {featured_html}
    </section>

    <section class="filter-toolbar" aria-label="Filtrar por estilo de plan">
      <div class="style-pills">
        <button type="button" class="style-pill-btn active" data-category="all" id="filter-cat-all">Todos los planes</button>
        <button type="button" class="style-pill-btn" data-category="Gratis y Baratos" id="filter-cat-cheap">💸 Gratis y Baratos</button>
        <button type="button" class="style-pill-btn" data-category="Planes Diferentes" id="filter-cat-unique">✨ Planes Diferentes</button>
        <button type="button" class="style-pill-btn" data-category="En Pareja" id="filter-cat-couple">❤️ En Pareja</button>
      </div>
      <div class="search-box-wrapper">
        <input
          type="search"
          id="article-search-input"
          class="search-input"
          placeholder="Buscar barrio o plan (ej. Albufera, Triana, gratis...)"
          aria-label="Buscar planes"
        />
      </div>
    </section>

    <section aria-label="Guías de planes">
      <div class="articles-grid" id="articles-grid-container">
        {cards_html}
      </div>
    </section>
  </main>

  {render_footer(root_prefix)}
  {render_filter_script()}
</body>
</html>
"""
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(page_html)


def build_article_page(art: dict, all_articles: list):
  city_name = art["city"]
  city_info = CITIES.get(
      city_name, {"slug": city_name.lower(), "h1": f"Planes en {city_name}"}
  )
  city_slug = city_info["slug"]
  root_prefix = "../../"
  output_path = os.path.join(
      PUBLIC_DIR, city_slug, art["slug"], "index.html"
  )
  canonical_url = f"{SITE_URL}/{city_slug}/{art['slug']}/"
  img_src = f"{root_prefix}{art['image'].lstrip('/')}"
  img_alt = art.get("imageAlt", art["title"])
  full_img_url = f"{SITE_URL}/{art['image'].lstrip('/')}"

  article_schema = {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": art["title"],
      "description": art["metaDescription"],
      "image": [full_img_url],
      "datePublished": art["publishedAt"],
      "dateModified": art["publishedAt"],
      "author": {
          "@type": "Organization",
          "name": "Redacción Qué Plan Hoy",
          "url": f"{SITE_URL}/sobre-nosotros/",
      },
      "publisher": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": SITE_URL,
      },
  }
  faq_schema = {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
          {
              "@type": "Question",
              "name": f["question"],
              "acceptedAnswer": {"@type": "Answer", "text": f["answer"]},
          }
          for f in art.get("faqs", [])
      ],
  }
  breadcrumb_schema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
          {
              "@type": "ListItem",
              "position": 1,
              "name": "Inicio",
              "item": f"{SITE_URL}/",
          },
          {
              "@type": "ListItem",
              "position": 2,
              "name": f"Planes en {city_name}",
              "item": f"{SITE_URL}/{city_slug}/",
          },
          {
              "@type": "ListItem",
              "position": 3,
              "name": art["title"],
              "item": canonical_url,
          },
      ],
  }

  # Tabla Resumen Rápida (Ideal para Featured Snippets de Google y utilidad real del lector)
  table_rows = []
  for sec in art.get("sections", []):
    venue_label = sec.get("venue", sec["heading"])
    table_rows.append(f"""
          <tr>
            <td style="padding: 0.65rem 0.85rem; border-bottom: 1px solid var(--border-hairline); font-weight: 600;">{html.escape(venue_label)}</td>
            <td style="padding: 0.65rem 0.85rem; border-bottom: 1px solid var(--border-hairline); color: var(--ink-secondary);">{html.escape(sec['location'])}</td>
            <td style="padding: 0.65rem 0.85rem; border-bottom: 1px solid var(--border-hairline); font-weight: 600; color: var(--olive);">{html.escape(sec['price'])}</td>
          </tr>""")

  summary_table_html = f"""
    <div style="background: var(--bg-elevated); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 2rem; overflow-x: auto;">
      <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--terracotta); margin-bottom: 0.65rem;">
        📋 Resumen rápido de la ruta en {html.escape(city_name)}
      </div>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-strong);">
            <th style="padding: 0.5rem 0.85rem;">Lugar / Plan</th>
            <th style="padding: 0.5rem 0.85rem;">Ubicación y Transporte</th>
            <th style="padding: 0.5rem 0.85rem;">Precio</th>
          </tr>
        </thead>
        <tbody>
          {''.join(table_rows)}
        </tbody>
      </table>
    </div>"""

  sections_html = []
  for sec in art.get("sections", []):
    sections_html.append(f"""
      <section class="reader-section">
        <h2>{html.escape(sec['heading'])}</h2>
        <div class="venue-meta-bar">
          <span>📍 <strong>Dirección y cómo llegar:</strong> {html.escape(sec['location'])}</span>
          <span>💶 <strong>Precio:</strong> {html.escape(sec['price'])}</span>
        </div>
        <p style="font-size: 1.04rem; color: var(--ink-primary); line-height: 1.75;">{html.escape(sec['content'])}</p>
      </section>""")

  aff = art.get("affiliate", {})
  aff_url = aff.get("url", "https://www.civitatis.com/es/")
  affiliate_html = ""
  if aff:
    affiliate_html = f"""
      <aside class="affiliate-callout" aria-label="Actividad recomendada">
        <div style="flex: 1; min-width: 240px;">
          <span class="affiliate-badge">✨ {html.escape(aff.get('badge', 'Plan Recomendado'))}</span>
          <h3 style="font-family: var(--font-serif); font-size: 1.3rem; margin-bottom: 0.35rem;">
            {html.escape(aff.get('title', ''))}
          </h3>
          <p style="font-size: 0.92rem; color: var(--ink-secondary);">
            {html.escape(aff.get('description', ''))}
          </p>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.45rem;">{html.escape(aff.get('price', ''))}</div>
          <a href="{html.escape(aff_url)}" target="_blank" rel="noopener sponsored" class="affiliate-cta-btn">
            {html.escape(aff.get('ctaText', 'Ver disponibilidad →'))}
          </a>
        </div>
      </aside>"""

  faqs_html = []
  for faq in art.get("faqs", []):
    faqs_html.append(f"""
      <div style="background: var(--bg-elevated); border: 1px solid var(--border-hairline); border-radius: var(--radius-sm); padding: 1.15rem 1.35rem; margin-bottom: 0.85rem;">
        <h3 style="font-size: 1.02rem; font-weight: 700; margin-bottom: 0.4rem;">{html.escape(faq['question'])}</h3>
        <p style="font-size: 0.95rem; color: var(--ink-secondary);">{html.escape(faq['answer'])}</p>
      </div>""")

  # Bloque de Autoría y Verificación E-E-A-T para Google Quality Raters
  eeat_box_html = f"""
    <div style="background: var(--bg-subtle); border-left: 4px solid var(--terracotta); border-radius: var(--radius-sm); padding: 1.15rem 1.35rem; margin-top: 2.25rem; font-size: 0.88rem; color: var(--ink-secondary);">
      <strong style="color: var(--ink-primary); display: block; margin-bottom: 0.25rem;">
        ✔️ Guía verificada por el equipo editorial de ¿Qué Plan Hoy?
      </strong>
      Revisamos periódicamente las direcciones, tarifas vigentes y paradas de transporte público de cada propuesta en {html.escape(city_name)}. Si detectas algún cambio de horario en alguno de los locales, puedes escribirnos a través de nuestra página <a href="{root_prefix}sobre-nosotros/" style="color: var(--terracotta); font-weight: 600;">Sobre Nosotros</a>.
    </div>"""

  related = [
      a
      for a in all_articles
      if a["id"] != art["id"] and a["city"] == city_name
  ]
  if len(related) < 3:
    related += [
        a
        for a in all_articles
        if a["id"] != art["id"] and a["city"] != city_name
    ][: 3 - len(related)]

  related_cards = "\n".join(
      render_article_card(r, root_prefix) for r in related[:3]
  )

  page_html = f"""{render_head(art['metaTitle'], art['metaDescription'], canonical_url, root_prefix, [article_schema, faq_schema, breadcrumb_schema], full_img_url)}
<body>
  {render_header(root_prefix, city_name)}

  <main class="main-container" style="max-width: 860px;">
    <nav aria-label="Migas de pan" style="font-size: 0.85rem; color: var(--ink-muted); margin-bottom: 1.25rem;">
      <a href="{root_prefix}" style="color: var(--ink-secondary); text-decoration: none;">Inicio</a>
      <span> › </span>
      <a href="{root_prefix}{city_slug}/" style="color: var(--ink-secondary); text-decoration: none;">Planes en {html.escape(city_name)}</a>
      <span> › </span>
      <span style="color: var(--ink-primary);">{html.escape(art['category'])}</span>
    </nav>

    <article>
      <div style="display: flex; gap: 0.6rem; align-items: center; font-size: 0.85rem; font-weight: 700; color: var(--terracotta); margin-bottom: 0.6rem; flex-wrap: wrap;">
        <span>{html.escape(city_name.upper())}</span>
        <span>·</span>
        <span>{art['categoryIcon']} {html.escape(art['category'])}</span>
        <span>·</span>
        <span style="color: var(--ink-muted); font-weight: 500;">Lectura: {html.escape(art['readTime'])} · Presupuesto: {html.escape(art['priceRange'])}</span>
      </div>

      <h1 style="font-family: var(--font-serif); font-size: clamp(1.85rem, 3.5vw, 2.65rem); line-height: 1.16; margin-bottom: 1rem;">
        {html.escape(art['title'])}
      </h1>

      <p style="font-size: 1.12rem; color: var(--ink-secondary); margin-bottom: 1.25rem;">
        {html.escape(art['excerpt'])}
      </p>

      <img src="{img_src}" alt="{html.escape(img_alt)}" class="reader-hero-img" width="860" height="480" />

      {summary_table_html}

      {''.join(sections_html)}

      {affiliate_html}

      <section style="margin-top: 2.5rem;" aria-labelledby="faq-heading">
        <h2 id="faq-heading" style="font-family: var(--font-serif); font-size: 1.55rem; margin-bottom: 1.1rem;">
          Preguntas frecuentes
        </h2>
        {''.join(faqs_html)}
      </section>

      {eeat_box_html}
    </article>

    <section style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--border-hairline);">
      <h2 style="font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1.25rem;">
        Más planes que te pueden gustar
      </h2>
      <div class="articles-grid" style="grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.25rem;">
        {related_cards}
      </div>
    </section>
  </main>

  {render_footer(root_prefix)}
</body>
</html>
"""
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(page_html)


def build_about_page():
  root_prefix = "../"
  output_path = os.path.join(PUBLIC_DIR, "sobre-nosotros", "index.html")
  canonical_url = f"{SITE_URL}/sobre-nosotros/"
  org_schema = {
      "@context": "https://schema.org",
      "@type": "AboutPage",
      "name": "Sobre Qué Plan Hoy y Criterio Editorial",
      "url": canonical_url,
      "mainEntity": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": SITE_URL,
          "description": (
              "Guía independiente de planes originales, baratos y en pareja en"
              " Madrid, Barcelona, Valencia, Sevilla y Toledo."
          ),
      },
  }
  page_html = f"""{render_head("Sobre Nosotros y Criterio Editorial | Qué Plan Hoy", "Conoce cómo seleccionamos y verificamos los planes locales, gratuitos y en pareja de Qué Plan Hoy en Madrid, Barcelona, Valencia, Sevilla y Toledo.", canonical_url, root_prefix, [org_schema])}
<body>
  {render_header(root_prefix, "none")}
  <main class="main-container" style="max-width: 780px;">
    <span class="hero-kicker">TRANSPARENCIA Y CRITERIO LOCAL</span>
    <h1 class="hero-title" style="margin-bottom: 1.25rem;">Sobre ¿Qué Plan Hoy?</h1>
    <p style="font-size: 1.08rem; color: var(--ink-secondary); margin-bottom: 1.5rem;">
      <strong>¿Qué Plan Hoy?</strong> nació con una misión sencilla: responder a la eterna pregunta de cada viernes por la tarde sin caer en las mismas diez recomendaciones masificadas de siempre.
    </p>
    <section class="reader-section">
      <h2>Cómo seleccionamos cada plan</h2>
      <p style="margin-top: 0.5rem;">
        Nos enfocamos en cinco ciudades clave de España (<strong>Madrid, Barcelona, Valencia, Sevilla y Toledo</strong>) y organizamos nuestras guías en tres pilares:
      </p>
      <ul style="margin: 0.85rem 0 0 1.25rem; line-height: 1.8;">
        <li><strong>💸 Planes Gratis y Baratos:</strong> Cultura, miradores, jardines históricos y rutas por menos de 10 €.</li>
        <li><strong>✨ Planes Diferentes:</strong> Rincones poco conocidos, talleres creativos y alternativas fuera del circuito turístico habitual.</li>
        <li><strong>❤️ Planes en Pareja:</strong> Citas originales y escapadas cercanas con encanto.</li>
      </ul>
    </section>
    <section class="reader-section">
      <h2>Datos prácticos verificados</h2>
      <p style="margin-top: 0.5rem;">
        En todas nuestras rutas incluimos la dirección exacta, la parada de transporte público más cercana (Metro, EMT o tren Avant) y el rango de precios real en euros para que puedas planificar sin sorpresas.
      </p>
    </section>
    <section class="reader-section" style="border-bottom: none;">
      <h2>Independencia editorial y enlaces de reserva</h2>
      <p style="margin-top: 0.5rem;">
        Algunas de nuestras guías incluyen enlaces a plataformas oficiales de reserva de actividades y visitas guiadas (como Civitatis, Fever o GetYourGuide). Si reservas a través de ellos, podemos recibir una pequeña comisión sin ningún coste adicional para ti, lo que nos permite mantener esta guía abierta, independiente y sin publicidad intrusiva.
      </p>
    </section>
  </main>
  {render_footer(root_prefix)}
</body>
</html>
"""
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(page_html)


def regenerate_sitemap(articles: list):
  today = date.today().isoformat()
  urls = [
      f"  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n"
      "    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n "
      " </url>",
      f"  <url>\n    <loc>{SITE_URL}/sobre-nosotros/</loc>\n   "
      f" <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n   "
      " <priority>0.6</priority>\n  </url>",
  ]
  for info in CITIES.values():
    c_slug = info["slug"]
    urls.append(
        f"  <url>\n    <loc>{SITE_URL}/{c_slug}/</loc>\n   "
        f" <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n   "
        " <priority>0.9</priority>\n  </url>"
    )
  for art in articles:
    c_slug = CITIES.get(art["city"], {"slug": art["city"].lower()})["slug"]
    pub = art.get("publishedAt", today)
    urls.append(
        f"  <url>\n    <loc>{SITE_URL}/{c_slug}/{art['slug']}/</loc>\n   "
        f" <lastmod>{pub}</lastmod>\n    <changefreq>monthly</changefreq>\n   "
        " <priority>0.8</priority>\n  </url>"
    )
  sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
  with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def build_all():
  with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

  build_listing_page(
      articles=articles,
      output_path=os.path.join(PUBLIC_DIR, "index.html"),
      title=(
          "Qué Plan Hoy | Planes Diferentes, Gratis y en Pareja en Madrid,"
          " Barcelona, Valencia, Sevilla y Toledo"
      ),
      description=(
          "¿Qué plan hoy? Guía local de planes originales, baratos, gratis y"
          " citas en pareja en Madrid, Barcelona, Valencia, Sevilla y Toledo"
          " con precios reales."
      ),
      canonical_url=f"{SITE_URL}/",
      h1="¿Qué plan hoy? Ideas diferentes, baratas y en pareja.",
      subtitle=(
          "Seleccionamos planes fuera de lo típico en Madrid, Barcelona,"
          " Valencia, Sevilla y Toledo: atardeceres en barca, talleres de"
          " cerámica y vino, patios mudéjares gratuitos y callejones con"
          " historia."
      ),
      kicker="QUÉ PLAN HOY · LA GUÍA PARA SALIR DE LA RUTINA",
      root_prefix="",
      active_city="all",
  )

  for city_name, info in CITIES.items():
    city_articles = [a for a in articles if a["city"] == city_name]
    build_listing_page(
        articles=city_articles,
        output_path=os.path.join(PUBLIC_DIR, info["slug"], "index.html"),
        title=info["metaTitle"],
        description=info["metaDesc"],
        canonical_url=f"{SITE_URL}/{info['slug']}/",
        h1=info["h1"],
        subtitle=info["intro"],
        kicker=f"GUÍA LOCAL DE {city_name.upper()} · QUÉ PLAN HOY",
        root_prefix="../",
        active_city=city_name,
    )

  for art in articles:
    build_article_page(art, articles)

  build_about_page()
  regenerate_sitemap(articles)
  with open(os.path.join(PUBLIC_DIR, "CNAME"), "w", encoding="utf-8") as f:
    f.write("queplanhoy.es\n")
  with open(
      os.path.join(PUBLIC_DIR, "googleb24ffbb97ddb75f6.html"),
      "w",
      encoding="utf-8",
  ) as f:
    f.write("google-site-verification: googleb24ffbb97ddb75f6.html")
  print(
      f"[OK] Sitio estático E-E-A-T generado: Portada + {len(CITIES)} ciudades"
      f" + {len(articles)} guías + /sobre-nosotros/ + CNAME + sitemap.xml."
  )


if __name__ == "__main__":
  build_all()
