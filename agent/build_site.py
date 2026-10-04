#!/usr/bin/env python3
"""Generador de Sitio Estático (SSG) para ¿Qué Plan Hoy? (queplanhoy.es).

Diseño editorial limpio inspirado en revistas urbanas (Time Out, Madrid Secreto, Traveler):
  - /index.html (Portada general)
  - /madrid/, /barcelona/, /valencia/, /sevilla/, /toledo/ (Páginas de ciudad)
  - /<ciudad>/<slug>/ (Páginas de cada guía con índice rápido, datos prácticos y Schema.org)
  - /sobre-nosotros/ (Página de criterio editorial)
"""

from datetime import date
import html
import json
import os
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "data", "articles.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
SITE_URL = "https://queplanhoy.es"

CITIES = {
    "Madrid": {
        "slug": "madrid",
        "h1": "Planes en Madrid: qué hacer fuera de lo típico",
        "metaTitle": (
            "Qué Plan Hacer en Madrid este Fin de Semana y Hoy (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "¿Buscas qué plan hacer en Madrid este fin de semana o qué planes"
            " hacer hoy? Feria Barroca de Valdemoro, mercadillos, ideas gratis"
            " por menos de 10 € y citas en pareja."
        ),
        "intro": (
            "Ferias históricas, mercados al aire libre, jardines secretos y"
            " citas originales en Madrid con direcciones exactas y precios"
            " reales."
        ),
    },
    "Barcelona": {
        "slug": "barcelona",
        "h1": "Planes en Barcelona: miradores, citas y rincones sin colas",
        "metaTitle": (
            "Qué Plan Hacer en Barcelona este Fin de Semana y Hoy (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Barcelona este fin de semana o hoy? Guía de"
            " miradores sin colas, jardines gratis y citas originales en"
            " pareja."
        ),
        "intro": (
            "Una Barcelona lejos de las aglomeraciones: desde jardines"
            " neoclásicos gratuitos hasta terrazas con vistas al Mediterráneo."
        ),
    },
    "Valencia": {
        "slug": "valencia",
        "h1": "Planes en Valencia: atardeceres, huerta y cultura local",
        "metaTitle": (
            "Qué Plan Hacer en Valencia este Fin de Semana y Hoy (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Valencia este fin de semana? Ideas baratas y"
            " en pareja: atardecer en barca en L'Albufera, rutas por la huerta"
            " y El Cabanyal."
        ),
        "intro": (
            "Escapadas en autobús urbano a L'Albufera, jardines escondidos y"
            " tapeo en las bodegas históricas de El Cabanyal."
        ),
    },
    "Sevilla": {
        "slug": "sevilla",
        "h1": "Planes en Sevilla: casas-palacio, patios y rutas al atardecer",
        "metaTitle": (
            "Qué Plan Hacer en Sevilla este Fin de Semana y Hoy (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Sevilla este fin de semana? Descubre planes"
            " gratis y en pareja: casas-palacio mudéjares sin colas, Triana y"
            " Santa Cruz."
        ),
        "intro": (
            "Palacios gratuitos, mercadillos históricos, rutas al anochecer por"
            " la antigua judería y planes auténticos en Triana."
        ),
    },
    "Toledo": {
        "slug": "toledo",
        "h1": "Planes en Toledo: escapadas, rutas nocturnas y rincones ocultos",
        "metaTitle": (
            "Qué Plan Hacer en Toledo este Fin de Semana y Hoy (2026) | Qué"
            " Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Toledo este fin de semana? Ruta de cobertizos"
            " iluminados, baños árabes en pareja, senda del Tajo y subterráneos"
            " a 33 min de Madrid."
        ),
        "intro": (
            "A 33 minutos en tren desde Madrid: qué hacer en Toledo cuando se"
            " marchan los autobuses turísticos, desde pasadizos iluminados"
            " hasta baños árabes."
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
  <meta name="google-site-verification" content="r39_brjoi72KrHzBWebcsqi7PAGZnM9J0CL_H2ydaHY" />
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
          "Inicio",
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
        f' id="nav-{key.lower()}">{label}</a>'
    )

  return f"""
  <header class="site-header">
    <div class="header-inner">
      <a href="{root_prefix if root_prefix else './'}" class="brand-logo" id="brand-home-link">
        <span class="brand-name">¿Qué<span>Plan</span>Hoy?</span>
        <span class="brand-tagline">Guía de planes originales</span>
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
        <a href="{root_prefix}madrid/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Madrid</a>
        <a href="{root_prefix}barcelona/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Barcelona</a>
        <a href="{root_prefix}valencia/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Valencia</a>
        <a href="{root_prefix}sevilla/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Sevilla</a>
        <a href="{root_prefix}toledo/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Toledo</a>
        <span>·</span>
        <a href="{root_prefix}sobre-nosotros/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Sobre nosotros</a>
      </nav>
      <p style="font-size: 0.78rem; margin-top: 0.5rem;">© {date.today().year} Qué Plan Hoy</p>
    </div>
  </footer>"""


def render_article_card(
    art: dict, root_prefix: str, is_lead: bool = False
) -> str:
  city_slug = CITIES.get(art["city"], {"slug": art["city"].lower()})["slug"]
  article_href = f"{root_prefix}{city_slug}/{art['slug']}/"
  img_src = f"{root_prefix}{art['image'].lstrip('/')}"
  img_alt = art.get("imageAlt", art["title"])
  cat_label = art["category"]
  if art.get("weekendDates"):
    cat_label = f"{cat_label} · {art['weekendDates']}"
  lead_cls = " lead-card" if is_lead else ""
  return f"""
  <article class="article-card{lead_cls}" data-category="{html.escape(art['category'])}" data-search="{html.escape((art['title'] + ' ' + art['excerpt'] + ' ' + ' '.join(art['neighborhoods'])).lower())}">
    <a href="{article_href}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
      <div class="card-image-wrap">
        <img src="{img_src}" alt="{html.escape(img_alt)}" class="card-image" loading="lazy" width="640" height="360" />
        <span class="card-city-tag">{html.escape(art['city'])}</span>
      </div>
      <div class="card-body">
        <div class="card-meta-top">
          <span class="card-category">{html.escape(cat_label)}</span>
          <span style="color: var(--ink-muted);">{html.escape(art['priceRange'])}</span>
        </div>
        <h2 class="card-title">{html.escape(art['title'])}</h2>
        <p class="card-excerpt">{html.escape(art['excerpt'])}</p>
        <div class="card-footer">
          <span class="card-neighborhoods">{html.escape(' · '.join(art['neighborhoods']))}</span>
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
        let firstVisible = true;
        cards.forEach(card => {
          const cat = card.getAttribute('data-category');
          const text = card.getAttribute('data-search') || '';
          const matchCat = currentCat === 'all' || cat === currentCat;
          const matchQuery = !currentQuery || text.includes(currentQuery);
          if (matchCat && matchQuery) {
            card.style.display = 'flex';
            if (firstVisible && cards.length > 1 && currentCat === 'all' && !currentQuery) {
              card.classList.add('lead-card');
            } else {
              card.classList.remove('lead-card');
            }
            firstVisible = false;
          } else {
            card.style.display = 'none';
          }
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
  cards_html = "\n".join(
      render_article_card(
          a, root_prefix, is_lead=(idx == 0 and len(articles) > 1)
      )
      for idx, a in enumerate(articles)
  )

  city_label = (
      active_city
      if active_city != "all"
      else "Madrid, Barcelona, Valencia, Sevilla y Toledo"
  )
  guide_links = []
  for a in articles:
    c_slug = CITIES.get(a["city"], {"slug": a["city"].lower()})["slug"]
    href = f"{root_prefix}{c_slug}/{a['slug']}/"
    guide_links.append(
        f'<li style="margin-bottom:0.35rem;"><a href="{href}"'
        ' style="color:var(--terracotta);font-weight:600;text-decoration:none;">'
        f"{html.escape(a['title'])}</a> — {html.escape(a['priceRange'])}</li>"
    )

  seo_bottom_section = f"""
    <section style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--border-hairline); max-width: 780px; color: var(--ink-secondary); font-size: 0.94rem;">
      <h2 style="font-family: var(--font-serif); font-size: 1.35rem; color: var(--ink-primary); margin-bottom: 0.65rem;">
        ¿Qué plan hacer en {html.escape(city_label)} este fin de semana?
      </h2>
      <p style="margin-bottom: 0.85rem;">
        Si estás buscando <strong>qué plan hacer en {html.escape(city_label)} este fin de semana</strong> o ideas para salir hoy sin caer en los sitios turísticos de siempre, en nuestras guías seleccionamos cada semana ferias históricas, mercadillos de fin de semana, jardines ocultos gratuitos y citas originales en pareja con direcciones exactas y precios reales:
      </p>
      <ul style="margin-left: 1.25rem; line-height: 1.7;">
        {''.join(guide_links)}
      </ul>
    </section>"""

  schema_ld = [
      {
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          "name": title,
          "description": description,
          "url": canonical_url,
      },
      {
          "@context": "https://schema.org",
          "@type": "ItemList",
          "name": h1,
          "itemListElement": [
              {
                  "@type": "ListItem",
                  "position": idx,
                  "name": a["title"],
                  "url": (
                      f"{SITE_URL}/{CITIES.get(a['city'], {'slug': a['city'].lower()})['slug']}/{a['slug']}/"
                  ),
              }
              for idx, a in enumerate(articles, start=1)
          ],
      },
  ]

  page_html = f"""{render_head(title, description, canonical_url, root_prefix, schema_ld)}
<body>
  {render_header(root_prefix, active_city)}

  <main class="main-container">
    <section class="page-header-section" aria-labelledby="main-hero-heading">
      <span class="hero-kicker">{html.escape(kicker)}</span>
      <h1 class="hero-title" id="main-hero-heading">{html.escape(h1)}</h1>
      <p class="hero-subtitle">{html.escape(subtitle)}</p>

      <div class="filter-toolbar" aria-label="Filtrar por tipo de plan">
        <div class="style-pills">
          <button type="button" class="style-pill-btn active" data-category="all" id="filter-cat-all">Todos</button>
          <button type="button" class="style-pill-btn" data-category="Este Fin de Semana" id="filter-cat-weekend">Este fin de semana</button>
          <button type="button" class="style-pill-btn" data-category="Gratis y Baratos" id="filter-cat-cheap">Gratis y baratos</button>
          <button type="button" class="style-pill-btn" data-category="Planes Diferentes" id="filter-cat-unique">Planes diferentes</button>
          <button type="button" class="style-pill-btn" data-category="En Pareja" id="filter-cat-couple">En pareja</button>
        </div>
        <div class="search-box-wrapper">
          <input
            type="search"
            id="article-search-input"
            class="search-input"
            placeholder="Buscar plan o barrio..."
            aria-label="Buscar planes"
          />
        </div>
      </div>
    </section>

    <section aria-label="Guías de planes">
      <div class="articles-grid" id="articles-grid-container">
        {cards_html}
      </div>
    </section>

    {seo_bottom_section}
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
          "name": "Qué Plan Hoy",
          "url": f"{SITE_URL}/sobre-nosotros/",
      },
      "publisher": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": SITE_URL,
      },
  }
  itemlist_schema = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": art["title"],
      "description": art["metaDescription"],
      "numberOfItems": len(art.get("sections", [])),
      "itemListElement": [
          {
              "@type": "ListItem",
              "position": idx,
              "name": sec.get("venue", sec["heading"]),
              "description": sec["content"],
              "url": f"{canonical_url}#plan-{idx}",
          }
          for idx, sec in enumerate(art.get("sections", []), start=1)
      ],
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

  toc_items = []
  for idx, sec in enumerate(art.get("sections", []), start=1):
    venue_label = sec.get("venue", sec["heading"])
    toc_items.append(
        f'<li><a href="#plan-{idx}">{idx}. {html.escape(venue_label)}</a></li>'
    )

  wa_text = urllib.parse.quote(
      f"Mira estos planes en {city_name}: {art['title']} {canonical_url}"
  )
  wa_share_url = f"https://api.whatsapp.com/send?text={wa_text}"

  toc_html = f"""
    <nav class="article-toc" aria-label="Índice de planes">
      <div class="article-toc-header">
        <span class="article-toc-title">En este artículo</span>
        <a href="{wa_share_url}" target="_blank" rel="noopener" style="font-size: 0.78rem; font-weight: 600; color: var(--olive); text-decoration: none;">
          Enviar por WhatsApp ↗
        </a>
      </div>
      <ol class="article-toc-list">
        {''.join(toc_items)}
      </ol>
    </nav>"""

  sections_html = []
  for idx, sec in enumerate(art.get("sections", []), start=1):
    venue_name = sec.get("venue", sec["heading"])
    maps_query = urllib.parse.quote(f"{venue_name}, {city_name}, España")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
    sections_html.append(f"""
      <section class="reader-section" id="plan-{idx}" style="scroll-margin-top: 90px;">
        <h2>{html.escape(sec['heading'])}</h2>
        <p style="font-size: 1.05rem; color: var(--ink-primary); line-height: 1.75;">{html.escape(sec['content'])}</p>
        <div class="venue-meta-bar">
          <span><strong>Dónde:</strong> {html.escape(sec['location'])}</span>
          <span><strong>Precio:</strong> {html.escape(sec['price'])}</span>
          <a href="{maps_url}" target="_blank" rel="noopener" style="color: var(--terracotta); font-weight: 600; text-decoration: none; margin-left: auto;">Cómo llegar (Google Maps) ↗</a>
        </div>
      </section>""")

  aff = art.get("affiliate", {})
  aff_url = aff.get(
      "url", f"https://www.civitatis.com/es/{city_slug}/"
  )
  civitatis_aid = os.environ.get("CIVITATIS_AID", "").strip()
  if (
      civitatis_aid
      and "civitatis.com" in aff_url
      and "aid=" not in aff_url
  ):
    sep = "&" if "?" in aff_url else "?"
    aff_url = f"{aff_url}{sep}aid={civitatis_aid}"
  affiliate_html = ""
  if aff:
    affiliate_html = f"""
      <aside class="affiliate-callout" aria-label="Actividad recomendada">
        <div style="flex: 1; min-width: 240px;">
          <span class="affiliate-badge">Para completar el plan</span>
          <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 0.3rem;">
            {html.escape(aff.get('title', ''))}
          </h3>
          <p style="font-size: 0.92rem; color: var(--ink-secondary);">
            {html.escape(aff.get('description', ''))}
          </p>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 600; font-size: 0.9rem; color: var(--ink-secondary); margin-bottom: 0.45rem;">{html.escape(aff.get('price', ''))}</div>
          <a href="{html.escape(aff_url)}" target="_blank" rel="noopener sponsored" class="affiliate-cta-btn">
            {html.escape(aff.get('ctaText', 'Ver horarios y reservar →'))}
          </a>
        </div>
      </aside>"""

  faqs_html = []
  for faq in art.get("faqs", []):
    faqs_html.append(f"""
      <div style="background: var(--bg-elevated); border: 1px solid var(--border-hairline); border-radius: var(--radius-sm); padding: 1.15rem 1.35rem; margin-bottom: 0.85rem;">
        <h3 style="font-size: 1rem; font-weight: 700; margin-bottom: 0.35rem;">{html.escape(faq['question'])}</h3>
        <p style="font-size: 0.94rem; color: var(--ink-secondary);">{html.escape(faq['answer'])}</p>
      </div>""")

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
      render_article_card(r, root_prefix, is_lead=False) for r in related[:3]
  )

  cat_header = art["category"]
  if art.get("weekendDates"):
    cat_header = f"{cat_header} · {art['weekendDates']}"

  page_html = f"""{render_head(art['metaTitle'], art['metaDescription'], canonical_url, root_prefix, [article_schema, itemlist_schema, faq_schema, breadcrumb_schema], full_img_url)}
<body>
  {render_header(root_prefix, city_name)}

  <main class="main-container" style="max-width: 820px;">
    <nav aria-label="Migas de pan" style="font-size: 0.84rem; color: var(--ink-muted); margin-bottom: 1.25rem;">
      <a href="{root_prefix}" style="color: var(--ink-secondary); text-decoration: none;">Inicio</a>
      <span> / </span>
      <a href="{root_prefix}{city_slug}/" style="color: var(--ink-secondary); text-decoration: none;">{html.escape(city_name)}</a>
      <span> / </span>
      <span style="color: var(--ink-primary);">{html.escape(art['category'])}</span>
    </nav>

    <article>
      <div style="display: flex; gap: 0.5rem; align-items: center; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--terracotta); margin-bottom: 0.6rem; flex-wrap: wrap;">
        <span>{html.escape(city_name)}</span>
        <span>·</span>
        <span>{html.escape(cat_header)}</span>
        <span>·</span>
        <span style="color: var(--ink-muted); font-weight: 500; text-transform: none; letter-spacing: 0;">{html.escape(art['priceRange'])}</span>
      </div>

      <h1 style="font-family: var(--font-serif); font-size: clamp(1.85rem, 3.4vw, 2.55rem); line-height: 1.16; margin-bottom: 0.9rem;">
        {html.escape(art['title'])}
      </h1>

      <p style="font-size: 1.1rem; color: var(--ink-secondary); margin-bottom: 1.35rem;">
        {html.escape(art['excerpt'])}
      </p>

      <figure style="margin: 0 0 1.6rem 0;">
        <img src="{img_src}" alt="{html.escape(img_alt)}" class="reader-hero-img" width="820" height="460" style="margin-bottom: 0.45rem;" />
        <figcaption style="font-size: 0.78rem; color: var(--ink-muted); text-align: right;">{html.escape(img_alt)}</figcaption>
      </figure>

      {toc_html}

      {''.join(sections_html)}

      {affiliate_html}

      <section style="margin-top: 2.5rem;" aria-labelledby="faq-heading">
        <h2 id="faq-heading" style="font-family: var(--font-serif); font-size: 1.45rem; margin-bottom: 1rem;">
          Preguntas frecuentes
        </h2>
        {''.join(faqs_html)}
      </section>
    </article>

    <section style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--border-hairline);">
      <h2 style="font-family: var(--font-serif); font-size: 1.45rem; margin-bottom: 1.25rem;">
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
  page_html = f"""{render_head("Sobre Nosotros | Qué Plan Hoy", "Conoce cómo seleccionamos los planes locales, gratuitos y en pareja de Qué Plan Hoy en Madrid, Barcelona, Valencia, Sevilla y Toledo.", canonical_url, root_prefix, [org_schema])}
<body>
  {render_header(root_prefix, "none")}
  <main class="main-container" style="max-width: 740px;">
    <span class="hero-kicker">SOBRE NOSOTROS</span>
    <h1 class="hero-title" style="margin-bottom: 1.25rem;">¿Qué es Qué Plan Hoy?</h1>
    <p style="font-size: 1.06rem; color: var(--ink-secondary); margin-bottom: 1.5rem;">
      <strong>¿Qué Plan Hoy?</strong> nació con una idea sencilla: responder a la pregunta de cada viernes por la tarde sin caer siempre en las mismas diez recomendaciones masificadas.
    </p>
    <section class="reader-section">
      <h2>Qué tipo de planes publicamos</h2>
      <p style="margin-top: 0.5rem;">
        Seleccionamos propuestas en <strong>Madrid, Barcelona, Valencia, Sevilla y Toledo</strong> pensadas tanto para quien vive en la ciudad como para quien hace una escapada de fin de semana:
      </p>
      <ul style="margin: 0.85rem 0 0 1.25rem; line-height: 1.8;">
        <li><strong>Este fin de semana:</strong> Ferias históricas (como la Feria Barroca de Valdemoro), mercados puntuales y citas de agenda con sus fechas exactas.</li>
        <li><strong>Gratis y baratos:</strong> Jardines ocultos, museos desconocidos, miradores y rutas por menos de 10 €.</li>
        <li><strong>Planes diferentes:</strong> Alternativas fuera del circuito turístico habitual para salir de la rutina.</li>
        <li><strong>En pareja:</strong> Citas originales, talleres creativos y paseos al atardecer.</li>
      </ul>
    </section>
    <section class="reader-section">
      <h2>Datos prácticos en cada ruta</h2>
      <p style="margin-top: 0.5rem;">
        En cada propuesta incluimos la dirección exacta, cómo llegar en transporte público (Metro, Cercanías, autobús o tren), el enlace directo a Google Maps y el precio real en euros.
      </p>
    </section>
    <section class="reader-section" style="border-bottom: none;">
      <h2>Enlaces y reservas</h2>
      <p style="margin-top: 0.5rem;">
        En nuestras guías facilitamos enlaces directos a las páginas oficiales de reserva de entradas y visitas guiadas para que puedas consultar horarios actualizados.
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
          "Qué Plan Hoy | Qué Planes Hacer Hoy y Este Fin de Semana en Madrid,"
          " Barcelona, Valencia, Sevilla y Toledo"
      ),
      description=(
          "¿Qué planes hacer hoy o este fin de semana? Guía local de planes"
          " originales, ferias, ideas gratis y citas en pareja en Madrid,"
          " Barcelona, Valencia, Sevilla y Toledo."
      ),
      canonical_url=f"{SITE_URL}/",
      h1="Planes originales en tu ciudad: qué hacer fuera de lo típico",
      subtitle=(
          "Ferias de fin de semana, jardines secretos, ideas por menos de 10 €"
          " y citas en pareja en Madrid, Barcelona, Valencia, Sevilla y Toledo."
      ),
      kicker="GUÍA EDITORIAL DE PLANES",
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
        kicker=f"GUÍA DE {city_name.upper()}",
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
      "[OK] Sitio estático E-E-A-T generado: Portada + 5 ciudades +"
      f" {len(articles)} guías + /sobre-nosotros/ + CNAME + sitemap.xml."
  )


if __name__ == "__main__":
  build_all()
