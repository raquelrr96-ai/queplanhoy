#!/usr/bin/env python3
"""Generador de Sitio Estático (SSG) para ¿Qué Plan Hoy? (queplanhoy.es).

Diseño editorial limpio inspirado en revistas urbanas (Time Out, Madrid Secreto, Traveler):
  - /index.html (Portada general)
  - /madrid/, /barcelona/, /valencia/, /sevilla/, /toledo/ (Páginas de ciudad)
  - /<ciudad>/<slug>/ (Páginas de cada guía con índice rápido, mapa interactivo, datos prácticos y Schema.org)
  - /mapa/ (Mapa interactivo general con todos los planes geolocalizados y enlace directo al pin en Google Maps)
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
        "lat": 40.4168,
        "lng": -3.7038,
        "zoom": 12,
        "ogImage": "images/venues/madrid-parque-capricho.jpg",
        "selectorImage": "images/venues/madrid-palacio-cristal-retiro-2.jpg",
        "h1": "Planes en Madrid: qué hacer hoy y este fin de semana fuera de lo típico",
        "metaTitle": (
            "Planes en Madrid Hoy y Este Fin de Semana (2026): Gratis, Pareja y"
            " Originales | Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Buscas qué plan hacer en Madrid hoy o este fin de semana? Guía"
            " actualizada con jardines secretos gratis, planes si llueve, citas"
            " en pareja y rutas por menos de 10 € con mapa."
        ),
        "intro": (
            "Rutas explicadas paso a paso, ferias históricas, jardines secretos"
            " y citas originales en Madrid con direcciones exactas, paradas de"
            " Metro, mapa interactivo y precios reales."
        ),
        "neighborhoods": [
            "Madrid de los Austrias y La Latina",
            "Alameda de Osuna",
            "Malasaña y Chueca",
            "Barrio de las Letras y Lavapiés",
            "Retiro y Paseo del Arte",
        ],
        "seoText": (
            "Encontrar planes en Madrid que salgan de las terrazas masificadas"
            " de Gran Vía o Sol es mucho más fácil cuando combinas patrimonio"
            " histórico poco conocido con barrios con vida propia. En esta guía"
            " reunimos desde recorridos completos por jardines históricos como"
            " el Parque de El Capricho o el Jardín del Príncipe de Anglona"
            " hasta alternativas a cubierto para días de lluvia (como el Salón"
            " de Baile del Museo Cerralbo, el Invernadero de Atocha o el Cine"
            " Doré por 3 €) y citas en pareja diferentes con talleres de"
            " cerámica y vino o jazz en directo."
        ),
        "faqs": [
            {
                "question": "¿Qué planes gratis se pueden hacer en Madrid este fin de semana?",
                "answer": (
                    "Entre los mejores planes gratuitos en Madrid destacan la"
                    " ruta completa por el Parque de El Capricho en Alameda de"
                    " Osuna (abierto sábados, domingos y festivos con entrada"
                    " libre), el Jardín del Príncipe de Anglona en La Latina,"
                    " el Invernadero de Cristal de Arganzuela y la visita al"
                    " Museo Cerralbo en su horario gratuito de jueves por la"
                    " tarde y domingos."
                ),
            },
            {
                "question": "¿Qué hacer en Madrid hoy si llueve y quieres un plan a cubierto?",
                "answer": (
                    "Si llueve en Madrid puedes refugiarte bajo la bóveda"
                    " acristalada de la Galería de Cristal del Palacio de"
                    " Cibeles, recorrer el Salón de Baile del Museo Cerralbo"
                    " (3 €) o el Palacio de Liria, merendar en el Café del"
                    " Jardín del Museo del Romanticismo o ver cine clásico en"
                    " versión original en el Cine Doré (Filmoteca Española) por"
                    " 3 €."
                ),
            },
            {
                "question": "¿Qué planes originales en pareja hay en Madrid para salir de la típica cena?",
                "answer": (
                    "Para una cita diferente en Madrid recomendamos un taller"
                    " de cerámica y vino de dos horas en Malasaña o Lavapiés,"
                    " un concierto íntimo de cuerda o jazz en directo a"
                    " medianoche en el histórico Café Central (Plaza del Ángel)"
                    " o un paseo al atardecer entre los templetes y el"
                    " laberinto del Parque de El Capricho."
                ),
            },
        ],
    },
    "Barcelona": {
        "slug": "barcelona",
        "lat": 41.3985,
        "lng": 2.1615,
        "zoom": 12,
        "ogImage": "images/venues/bcn-laberint-horta.jpg",
        "selectorImage": "images/venues/bcn-palau-nacional-mnac.jpg",
        "h1": "Planes en Barcelona: miradores, jardines secretos y citas sin colas",
        "metaTitle": (
            "Planes en Barcelona Hoy y Este Fin de Semana (2026): Gratis,"
            " Miradores y Pareja | Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Barcelona este fin de semana o hoy? Guías paso"
            " a paso por el Laberinto de Horta, miradores sin colas en"
            " Montjuïc, jardines gratis y citas originales en pareja."
        ),
        "intro": (
            "Una Barcelona lejos de las aglomeraciones: desde jardines"
            " neoclásicos gratuitos y rutas por el Born y Montjuïc hasta"
            " miradores tranquilos con vistas al Mediterráneo."
        ),
        "neighborhoods": [
            "Horta-Guinardó",
            "Montjuïc y Poble-sec",
            "El Born y Ciutat Vella",
            "Eixample y Sant Antoni",
            "Sarrià-Sant Gervasi",
        ],
        "seoText": (
            "Más allá de las Ramblas y la Sagrada Familia, Barcelona esconde"
            " palacetes, jardines históricos y miradores donde todavía se"
            " respira calma local. En nuestras guías de Barcelona encontrarás"
            " itinerarios detallados con paradas de Metro, horarios gratuitos"
            " verificados (como los domingos tarde en el Laberinto de Horta o"
            " los Jardines de Laribal en Montjuïc) y planes románticos por el"
            " Recinto Modernista de Sant Pau."
        ),
        "faqs": [
            {
                "question": "¿Qué planes gratis hacer en Barcelona este fin de semana sin masificaciones?",
                "answer": (
                    "Puedes recorrer gratis los Jardines de Laribal y el Teatre"
                    " Grec en Montjuïc, visitar el Parque del Laberinto de"
                    " Horta (gratuito miércoles y domingos por la tarde), o"
                    " explorar el yacimiento del Mercat del Born y las"
                    " callejuelas medievales de Sant Pere."
                ),
            },
            {
                "question": "¿Cuáles son los mejores miradores alternativos de Barcelona?",
                "answer": (
                    "Para evitar las aglomeraciones de los Búnkers del Carmel,"
                    " te recomendamos las terrazas ajardinadas de Montjuïc"
                    " junto a la Fundació Miró, los jardines del Mirador del"
                    " Alcalde y el entorno alto del Parque del Laberinto de"
                    " Horta al pie de Collserola."
                ),
            },
        ],
    },
    "Valencia": {
        "slug": "valencia",
        "lat": 39.4699,
        "lng": -0.3763,
        "zoom": 12,
        "ogImage": "images/venues/vlc-albufera-atardecer-dorado.jpg",
        "selectorImage": "images/cities/valencia-selector.jpg",
        "h1": "Planes en Valencia: L'Albufera, jardines secretos y cultura local",
        "metaTitle": (
            "Planes en Valencia Hoy y Este Fin de Semana (2026): Gratis,"
            " Albufera y Pareja | Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Valencia hoy o este fin de semana? Cómo ir a"
            " L'Albufera y El Palmar en autobús por 2 €, Jardines de Monforte,"
            " rutas gratis y bodegas de El Cabanyal."
        ),
        "intro": (
            "Escapadas paso a paso en autobús urbano a L'Albufera, jardines"
            " neoclásicos escondidos y tapeo en las bodegas históricas de El"
            " Cabanyal."
        ),
        "neighborhoods": [
            "Parque Natural de L'Albufera y El Palmar",
            "Ciutat Vella y El Carmen",
            "Jardines de Monforte y Alameda",
            "El Cabanyal y Canyamelar",
            "Ruzafa",
        ],
        "seoText": (
            "Valencia permite pasar en menos de media hora de un jardín"
            " romántico del siglo XIX en pleno centro a los arrozales y"
            " embarcaderos de L'Albufera en autobús público. Todas nuestras"
            " rutas incluyen líneas exactas de EMT, precios reales y enlaces"
            " directos al pin en Google Maps."
        ),
        "faqs": [
            {
                "question": "¿Cómo ir del centro de Valencia a L'Albufera y El Palmar en transporte público?",
                "answer": (
                    "La línea 24 de los autobuses rojos de la EMT conecta el"
                    " centro de Valencia (Puerta de la Mar / Navarro Reverter)"
                    " con el embarcadero de la Gola de Pujol y el pueblo de El"
                    " Palmar por el precio de un billete urbano (2 € o bono"
                    " SUMA)."
                ),
            },
            {
                "question": "¿Qué planes gratis y tranquilos hacer en Valencia?",
                "answer": (
                    "Destacan los Jardines de Monforte (un jardín neoclásico"
                    " gratuito con estatuas de mármol y estanques), el Centro"
                    " Cultural Bancaja, el claustro gótico del Centre del"
                    " Carme (CCCC) y un paseo al atardecer por las casas"
                    " modernistas de El Cabanyal."
                ),
            },
        ],
    },
    "Sevilla": {
        "slug": "sevilla",
        "lat": 37.3891,
        "lng": -5.9845,
        "zoom": 13,
        "ogImage": "images/venues/sev-patio-santa-cruz.jpg",
        "selectorImage": "images/cities/sevilla-selector.jpg",
        "h1": "Planes en Sevilla: casas-palacio, patios ocultos y rutas al atardecer",
        "metaTitle": (
            "Planes en Sevilla Hoy y Este Fin de Semana (2026): Gratis, Patios"
            " y Pareja | Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Sevilla hoy o este fin de semana? Descubre"
            " planes gratis y en pareja: Palacio de los Marqueses de la Algaba,"
            " Calle Feria, patios ocultos, Triana y Santa Cruz."
        ),
        "intro": (
            "Palacios mudéjares gratuitos, mercadillos históricos, patios"
            " silenciosos y rutas al anochecer por la antigua judería y Triana."
        ),
        "neighborhoods": [
            "Calle Feria y Macarena",
            "Barrio de Santa Cruz y Judería",
            "Triana",
            "Parque de María Luisa",
            "Arenal y Museo",
        ],
        "seoText": (
            "Para disfrutar de Sevilla sin colas ni precios inflados, nuestras"
            " guías se centran en casas-palacio mudéjares y renacentistas de"
            " acceso gratuito o muy económico (como el Palacio de los Marqueses"
            " de la Algaba o la Casa de Salinas), combinadas con el tapeo"
            " tradicional del Mercado de la Calle Feria y paseos al caer el sol."
        ),
        "faqs": [
            {
                "question": "¿Qué palacios y patios se pueden visitar gratis en Sevilla?",
                "answer": (
                    "El Palacio de los Marqueses de la Algaba (junto al Mercado"
                    " de la Calle Feria) ofrece entrada completamente gratuita"
                    " a su patio mudéjar y su centro de arte mudéjar. También"
                    " es gratuito pasear por el entorno del Pabellón Mudéjar en"
                    " la Plaza de América y las plazuelas escondidas de Santa"
                    " Cruz."
                ),
            },
            {
                "question": "¿Qué hacer en Sevilla en pareja para una cita tranquila?",
                "answer": (
                    "Un recorrido de mañana o media tarde por los patios de"
                    " Santa Cruz y la Casa de Salinas, seguido de un paseo al"
                    " atardecer por la orilla de Triana (Calle Betis) o el"
                    " Jardín de los Leones del Parque de María Luisa."
                ),
            },
        ],
    },
    "Toledo": {
        "slug": "toledo",
        "lat": 39.8581,
        "lng": -4.0226,
        "zoom": 14,
        "ogImage": "images/venues/tol-panoramica-noche.jpg",
        "selectorImage": "images/cities/toledo-selector.jpg",
        "h1": "Planes en Toledo: rutas por el Tajo, cobertizos y escapadas de noche",
        "metaTitle": (
            "Planes en Toledo Hoy y Este Fin de Semana (2026): Gratis, Pareja y"
            " Noche | Qué Plan Hoy"
        ),
        "metaDesc": (
            "¿Qué plan hacer en Toledo hoy o este fin de semana? Guía completa"
            " de la Senda Ecológica del Tajo, ruta de cobertizos de noche,"
            " miradores gratis y planes en pareja a 33 min de Madrid."
        ),
        "intro": (
            "A 33 minutos en tren desde Madrid: rutas a pie por el cañón del"
            " Tajo, pasadizos iluminados de noche y rincones fuera de lo"
            " turístico."
        ),
        "neighborhoods": [
            "Senda Ecológica del Río Tajo",
            "Zona Conventual y Cobertizos",
            "Judería Mayor y San Martín",
            "Cerro del Bú y Valle de Toledo",
            "Alcántara y Casco Histórico",
        ],
        "seoText": (
            "Toledo cambia por completo cuando te sales del eje comercial de"
            " Zocodover o cuando cae la tarde y se marchan las excursiones de"
            " día. Aquí tienes desde la ruta completa a pie por la Senda"
            " Ecológica del Tajo entre los puentes medievales de Alcántara y"
            " San Martín hasta planes nocturnos en pareja por los cobertizos"
            " conventuales iluminados."
        ),
        "faqs": [
            {
                "question": "¿Cuál es la mejor ruta gratis para hacer a pie en Toledo?",
                "answer": (
                    "La Senda Ecológica del Tajo es un recorrido gratuito y"
                    " llano de unos 5 kilómetros que bordea el cañón del río"
                    " desde el Puente de Alcántara hasta el Puente de San"
                    " Martín, ofreciendo las mejores vistas de la roca de"
                    " Toledo sin multitudes."
                ),
            },
            {
                "question": "¿Qué hacer en Toledo de noche y en pareja?",
                "answer": (
                    "Al anochecer recomendamos ver la puesta de sol sobre la"
                    " ciudad desde el Cerro del Bú o el Valle, recorrer en"
                    " silencio los cobertizos medievales (Santo Domingo el"
                    " Real, Santa Clara) bajo los faroles de forja y cruzar el"
                    " Puente de San Martín iluminado."
                ),
            },
        ],
    },
}


def render_head(
    title: str,
    description: str,
    canonical_url: str,
    root_prefix: str,
    json_ld_list: list,
    og_image: str = "",
    include_leaflet: bool = False,
    og_type: str = "website",
    robots: str = "index, follow, max-image-preview:large",
) -> str:
  ld_scripts = "\n".join(
      '<script type="application/ld+json">\n'
      + json.dumps(ld, ensure_ascii=False, indent=2)
      + "\n</script>"
      for ld in json_ld_list
  )
  resolved_og_image = (
      og_image
      if og_image
      else f"{SITE_URL}/images/planes-este-fin-de-semana-madrid-feria-barroca.jpg"
  )
  og_img_tag = (
      f'<meta property="og:image" content="{html.escape(resolved_og_image)}" />\n'
      f'  <meta name="twitter:card" content="summary_large_image" />\n'
      f'  <meta name="twitter:title" content="{html.escape(title)}" />\n'
      f'  <meta name="twitter:description" content="{html.escape(description)}" />\n'
      f'  <meta name="twitter:image" content="{html.escape(resolved_og_image)}" />'
  )
  leaflet_tags = ""
  if include_leaflet:
    leaflet_tags = """
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" crossorigin="" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js" crossorigin=""></script>"""
  return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="r39_brjoi72KrHzBWebcsqi7PAGZnM9J0CL_H2ydaHY" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}" />
  <meta name="robots" content="{robots}" />
  <meta name="theme-color" content="#c84b31" />
  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png" />
  <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="es-ES" href="{canonical_url}" />
  <link rel="alternate" hreflang="es" href="{canonical_url}" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:site_name" content="Qué Plan Hoy" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(description)}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{canonical_url}" />
  {og_img_tag}
  <link rel="sitemap" type="application/xml" title="Sitemap" href="{root_prefix}sitemap.xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root_prefix}index.css" />{leaflet_tags}
  <script nowprocket data-noptimize="1" data-cfasync="false" data-wpfc-render="false" seraph-accel-crit="1" data-no-defer="1" data-cmp-ab="2">
    (function () {{
        var script = document.createElement("script");
        script.async = 1;
        script.setAttribute("data-cmp-ab","2");
        script.src = 'https://emrldtp.com/NTgxMzAy.js?t=581302';
        document.head.appendChild(script);
    }})();
  </script>
  {ld_scripts}
</head>"""


def render_header(root_prefix: str, active_city: str = "all") -> str:
  nav_items = [
      (
          "all",
          "Inicio",
          f"{root_prefix}" if root_prefix else "./",
      ),
      ("Madrid", "Madrid", f"{root_prefix}madrid/"),
      ("Barcelona", "Barcelona", f"{root_prefix}barcelona/"),
      ("Valencia", "Valencia", f"{root_prefix}valencia/"),
      ("Sevilla", "Sevilla", f"{root_prefix}sevilla/"),
      ("Toledo", "Toledo", f"{root_prefix}toledo/"),
      ("mapa", "🗺️ Mapa de Planes", f"{root_prefix}mapa/"),
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
      <a href="{root_prefix if root_prefix else './'}" class="brand-logo" id="brand-home-link" style="display:flex;align-items:center;gap:0.55rem;">
        <img src="/favicon.svg" alt="" width="30" height="30" style="border-radius:7px;flex-shrink:0;box-shadow:0 2px 6px rgba(200,75,49,0.22);" />
        <span style="display:flex;flex-direction:column;">
          <span class="brand-name">¿Qué<span>Plan</span>Hoy?</span>
          <span class="brand-tagline">Guía de planes originales</span>
        </span>
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
      <div style="font-family: var(--font-serif); font-size: 1.25rem; color: var(--ink-primary); font-weight: 700; display: flex; align-items: center; gap: 0.45rem;">
        <img src="/favicon.svg" alt="" width="24" height="24" style="border-radius:6px;" />
        <span>¿Qué<span style="color: var(--terracotta); font-style: italic;">Plan</span>Hoy?</span>
      </div>
      <p>Guía independiente de planes diferentes, gratuitos y citas en pareja con direcciones, mapa interactivo y precios reales.</p>
      <nav aria-label="Enlaces de ciudades y criterio editorial" style="display: flex; gap: 1.15rem; flex-wrap: wrap; justify-content: center; margin-top: 0.25rem;">
        <a href="{root_prefix}madrid/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Madrid</a>
        <a href="{root_prefix}barcelona/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Barcelona</a>
        <a href="{root_prefix}valencia/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Valencia</a>
        <a href="{root_prefix}sevilla/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Sevilla</a>
        <a href="{root_prefix}toledo/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Toledo</a>
        <span>·</span>
        <a href="{root_prefix}mapa/" style="color: var(--terracotta); text-decoration: none; font-weight: 700;">🗺️ Mapa de Planes</a>
        <span>·</span>
        <a href="{root_prefix}sobre-nosotros/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Sobre nosotros</a>
        <span>·</span>
        <a href="{root_prefix}privacidad-y-cookies/" style="color: var(--ink-secondary); text-decoration: none; font-weight: 600;">Privacidad y Cookies</a>
        <span>·</span>
        <button type="button" onclick="window.openCookieBanner && window.openCookieBanner()" style="background:none;border:none;padding:0;font:inherit;color:var(--ink-secondary);font-weight:600;cursor:pointer;text-decoration:underline;">Configurar cookies</button>
      </nav>
      <p style="font-size: 0.78rem; margin-top: 0.5rem;">© {date.today().year} Qué Plan Hoy</p>
    </div>
  </footer>

  <div id="qph-cookie-banner" role="dialog" aria-live="polite" aria-label="Aviso de cookies" style="display:none;position:fixed;bottom:0.85rem;left:0.85rem;right:0.85rem;max-width:620px;margin:0 auto;background:var(--bg-elevated, #fff);border:1px solid var(--border-subtle, #e5e0d5);border-radius:14px;box-shadow:0 14px 36px rgba(28,25,23,0.22);padding:1rem 1.15rem;z-index:9999;font-family:var(--font-sans, sans-serif);">
    <div style="display:flex;flex-direction:column;gap:0.8rem;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;">
        <p style="margin:0;font-size:0.83rem;line-height:1.48;color:var(--ink-secondary, #57534e);">
          🍪 Usamos cookies técnicas y de colaboradores (como Tiqets) para que la web funcione y medir las reservas desde nuestras guías. Puedes aceptarlas y seguir viendo todos los planes o mantener solo las necesarias.
        </p>
        <button type="button" id="qph-cookie-close" aria-label="Cerrar aviso de cookies" style="background:none;border:none;color:var(--ink-muted, #78716c);font-size:1.1rem;line-height:1;padding:0.15rem 0.3rem;cursor:pointer;flex-shrink:0;">✕</button>
      </div>
      <div style="display:flex;gap:0.6rem;align-items:center;justify-content:space-between;flex-wrap:wrap;">
        <a href="{root_prefix}privacidad-y-cookies/" style="color:var(--ink-muted, #78716c);font-size:0.74rem;text-decoration:underline;">Más info sobre privacidad</a>
        <div style="display:flex;gap:0.55rem;flex:1;justify-content:flex-end;min-width:230px;">
          <button type="button" id="qph-cookie-reject" style="flex:1;max-width:160px;min-height:42px;background:var(--bg-sand, #f5f2eb);color:var(--ink-primary, #1c1917);border:1px solid var(--border-subtle, #e5e0d5);padding:0.55rem 0.85rem;border-radius:9px;font-size:0.82rem;font-weight:600;cursor:pointer;">Solo necesarias</button>
          <button type="button" id="qph-cookie-accept" style="flex:1;max-width:170px;min-height:42px;background:var(--terracotta, #c84b31);color:#fff;border:1px solid var(--terracotta, #c84b31);padding:0.55rem 0.95rem;border-radius:9px;font-size:0.84rem;font-weight:700;cursor:pointer;">Aceptar y continuar</button>
        </div>
      </div>
    </div>
  </div>
  <script>
    (function() {{
      var KEY = 'qph_cookie_consent_v1';
      var banner = document.getElementById('qph-cookie-banner');
      if (!banner) return;
      function hideBanner() {{ banner.style.display = 'none'; }}
      function showBanner() {{ banner.style.display = 'block'; }}
      function handleChoice(val) {{
        try {{ localStorage.setItem(KEY, val); }} catch (e) {{}}
        hideBanner();
        if (window.location.pathname.indexOf('privacidad-y-cookies') !== -1) {{
          window.location.href = '/';
        }}
      }}
      window.openCookieBanner = showBanner;
      try {{
        var saved = localStorage.getItem(KEY);
        if (!saved) {{ showBanner(); }}
      }} catch (e) {{}}
      var btnAccept = document.getElementById('qph-cookie-accept');
      var btnReject = document.getElementById('qph-cookie-reject');
      var btnClose = document.getElementById('qph-cookie-close');
      if (btnAccept) {{
        btnAccept.addEventListener('click', function() {{ handleChoice('accepted'); }});
      }}
      if (btnReject) {{
        btnReject.addEventListener('click', function() {{ handleChoice('necessary'); }});
      }}
      if (btnClose) {{
        btnClose.addEventListener('click', function() {{ handleChoice('necessary'); }});
      }}
    }})();
  </script>"""


def render_article_card(
    art: dict,
    root_prefix: str,
    is_lead: bool = False,
    initial_hidden: bool = False,
) -> str:
  city_slug = CITIES.get(art["city"], {"slug": art["city"].lower()})["slug"]
  article_href = f"{root_prefix}{city_slug}/{art['slug']}/"
  img_src = f"{root_prefix}{art['image'].lstrip('/')}"
  img_alt = art.get("imageAlt", art["title"])
  cat_label = art["category"]
  if art.get("weekendDates"):
    cat_label = f"{cat_label} · {art['weekendDates']}"
  lead_cls = " lead-card" if is_lead else ""
  style_attr = ' style="display: none;"' if initial_hidden else ""
  read_cta = "Leer guía →"
  return f"""
  <article class="article-card{lead_cls}"{style_attr} data-city="{html.escape(art['city'])}" data-category="{html.escape(art['category'])}" data-search="{html.escape((art['title'] + ' ' + art['excerpt'] + ' ' + ' '.join(art['neighborhoods'])).lower())}">
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
          <span class="card-read-link">{read_cta}</span>
        </div>
      </div>
    </a>
  </article>"""


def render_filter_script(active_city: str = "all") -> str:
  return f"""
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const pageCityMode = {json.dumps(active_city)};
      const CITY_STORAGE_KEY = 'qph_preferred_city';
      const pills = document.querySelectorAll('.style-pill-btn');
      const cityPickCards = document.querySelectorAll('.city-pick-card');
      const searchInput = document.getElementById('article-search-input');
      const cards = document.querySelectorAll('.article-card');
      const heroKicker = document.getElementById('main-hero-kicker');
      const heroHeading = document.getElementById('main-hero-heading');
      const heroSubtitle = document.getElementById('main-hero-subtitle');
      const hubDirectLink = document.getElementById('city-hub-direct-link');
      const mapBannerTitle = document.getElementById('map-banner-title');
      const mapBannerLink = document.getElementById('map-banner-link');

      let currentCat = 'all';
      let currentQuery = '';
      let currentCity = pageCityMode === 'all' ? 'Madrid' : pageCityMode;

      if (pageCityMode !== 'all') {{
        try {{ localStorage.setItem(CITY_STORAGE_KEY, pageCityMode); }} catch (e) {{}}
      }} else {{
        try {{
          const params = new URLSearchParams(window.location.search);
          const urlCity = params.get('ciudad');
          const savedCity = localStorage.getItem(CITY_STORAGE_KEY);
          if (urlCity && document.querySelector(`.city-pick-card[data-city="${{urlCity}}"]`)) {{
            currentCity = urlCity;
          }} else if (savedCity && document.querySelector(`.city-pick-card[data-city="${{savedCity}}"]`)) {{
            currentCity = savedCity;
          }}
        }} catch (e) {{}}
      }}

      function updateCityContext(cityBtn) {{
        if (!cityBtn) return;
        const cName = cityBtn.getAttribute('data-city');
        const cSlug = cityBtn.getAttribute('data-slug');
        const cH1 = cityBtn.getAttribute('data-h1');
        const cIntro = cityBtn.getAttribute('data-intro');
        const cKicker = cityBtn.getAttribute('data-kicker');

        cityPickCards.forEach(b => b.classList.toggle('active', b === cityBtn));
        if (heroKicker && cKicker) heroKicker.textContent = cKicker;
        if (heroHeading && cH1) heroHeading.textContent = cH1;
        if (heroSubtitle && cIntro) heroSubtitle.textContent = cIntro;
        if (hubDirectLink && cSlug) {{
          hubDirectLink.href = cSlug + '/';
          hubDirectLink.textContent = 'Ir a la página completa de ' + cName + ' →';
        }}
        if (mapBannerTitle) {{
          mapBannerTitle.textContent = 'Explora todos los planes de ' + cName + ' en el mapa con enlace directo a Google Maps';
        }}
        if (mapBannerLink) {{
          mapBannerLink.href = 'mapa/?ciudad=' + encodeURIComponent(cName);
        }}
      }}

      function applyFilters() {{
        let firstVisible = true;
        cards.forEach(card => {{
          const cardCity = card.getAttribute('data-city');
          const cat = card.getAttribute('data-category');
          const text = card.getAttribute('data-search') || '';
          const matchCity = pageCityMode !== 'all' || cardCity === currentCity;
          const matchCat = currentCat === 'all' || cat === currentCat;
          const matchQuery = !currentQuery || text.includes(currentQuery);
          if (matchCity && matchCat && matchQuery) {{
            card.style.display = 'flex';
            if (firstVisible && currentCat === 'all' && !currentQuery) {{
              card.classList.add('lead-card');
            }} else {{
              card.classList.remove('lead-card');
            }}
            firstVisible = false;
          }} else {{
            card.style.display = 'none';
            card.classList.remove('lead-card');
          }}
        }});
      }}

      if (pageCityMode === 'all' && cityPickCards.length > 0) {{
        const initialBtn = document.querySelector(`.city-pick-card[data-city="${{currentCity}}"]`) || cityPickCards[0];
        if (initialBtn) {{
          currentCity = initialBtn.getAttribute('data-city');
          updateCityContext(initialBtn);
          applyFilters();
        }}
        cityPickCards.forEach(btn => {{
          btn.addEventListener('click', () => {{
            currentCity = btn.getAttribute('data-city');
            try {{ localStorage.setItem(CITY_STORAGE_KEY, currentCity); }} catch (e) {{}}
            updateCityContext(btn);
            applyFilters();
          }});
        }});
      }}

      pills.forEach(btn => {{
        btn.addEventListener('click', () => {{
          pills.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentCat = btn.getAttribute('data-category');
          applyFilters();
        }});
      }});

      if (searchInput) {{
        searchInput.addEventListener('input', e => {{
          currentQuery = e.target.value.trim().toLowerCase();
          applyFilters();
        }});
      }}
    }});
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
  cards_html_list = []
  seen_lead = False
  for a in articles:
    if active_city == "all":
      is_visible_default = a["city"] == "Madrid"
      is_lead = is_visible_default and not seen_lead
      if is_lead:
        seen_lead = True
      cards_html_list.append(
          render_article_card(
              a,
              root_prefix,
              is_lead=is_lead,
              initial_hidden=not is_visible_default,
          )
      )
    else:
      is_lead = not seen_lead and len(articles) > 1
      if is_lead:
        seen_lead = True
      cards_html_list.append(
          render_article_card(
              a, root_prefix, is_lead=is_lead, initial_hidden=False
          )
      )
  cards_html = "\n".join(cards_html_list)

  city_label = active_city if active_city != "all" else "Madrid"
  seo_city_label = (
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
        f"<strong>{html.escape(a['city'])}:</strong> {html.escape(a['title'])}</a> — {html.escape(a['priceRange'])}</li>"
    )

  city_selector_html = ""
  if active_city == "all":
    city_order = ["Madrid", "Toledo", "Barcelona", "Valencia", "Sevilla"]
    city_buttons = []
    for c_name in city_order:
      c_info = CITIES[c_name]
      active_cls = " active" if c_name == "Madrid" else ""
      selector_img = c_info.get("selectorImage", c_info["ogImage"])
      thumb_src = f"{root_prefix}{selector_img.lstrip('/')}"
      city_buttons.append(f"""
          <button
            type="button"
            class="city-pick-card{active_cls}"
            data-city="{html.escape(c_name)}"
            data-slug="{html.escape(c_info['slug'])}"
            data-h1="{html.escape(c_info['h1'])}"
            data-intro="{html.escape(c_info['intro'])}"
            data-kicker="GUÍA DE {html.escape(c_name.upper())}"
          >
            <img src="{thumb_src}" alt="Planes en {html.escape(c_name)}" class="city-pick-photo" loading="eager" width="320" height="180" />
            <span class="city-pick-overlay"></span>
            <span class="city-pick-name">{html.escape(c_name)}</span>
          </button>""")
    city_selector_html = f"""
      <div class="city-selector-showcase" aria-label="Selector de ciudad">
        <div class="city-selector-header">
          <span class="city-selector-title">📍 ¿En qué ciudad buscas plan hoy? <span style="font-weight:500;color:var(--ink-muted);font-size:0.78rem;">(Toca tu ciudad para ver solo sus planes)</span></span>
          <a href="madrid/" id="city-hub-direct-link" class="city-selector-hub-link">Ir a la página completa de Madrid →</a>
        </div>
        <div class="city-selector-grid">
          {''.join(city_buttons)}
        </div>
      </div>"""

  map_href = (
      f"{root_prefix}mapa/?ciudad={urllib.parse.quote(city_label)}"
  )
  map_banner = f"""
    <div style="margin: 0 0 2rem 0; padding: 1.1rem 1.4rem; background: var(--bg-sand); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
      <div>
        <span style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--terracotta);">🗺️ Nuevo · Mapa Interactivo</span>
        <div id="map-banner-title" style="font-family: var(--font-serif); font-size: 1.15rem; font-weight: 700; color: var(--ink-primary); margin-top: 0.15rem;">
          Explora todos los planes de {html.escape(city_label)} en el mapa con enlace directo a Google Maps
        </div>
      </div>
      <a id="map-banner-link" href="{map_href}" style="background: var(--terracotta); color: #fff; text-decoration: none; font-weight: 600; font-size: 0.88rem; padding: 0.6rem 1.15rem; border-radius: var(--radius-pill); white-space: nowrap;">
        Abrir Mapa de Planes →
      </a>
    </div>"""

  city_info = CITIES.get(active_city, {})
  city_seo_text = city_info.get(
      "seoText",
      "Seleccionamos planes originales, rutas explicadas paso a paso con"
      " horarios y paradas de transporte público, programas oficiales de"
      " fiestas y puentes, jardines secretos gratuitos y citas en pareja en"
      " Madrid, Barcelona, Valencia, Sevilla y Toledo.",
  )
  city_neighborhoods = city_info.get(
      "neighborhoods",
      ["Madrid", "Toledo", "Barcelona", "Valencia", "Sevilla"],
  )
  neighborhood_pills = "".join(
      f'<span style="background:var(--bg-sand);border:1px solid var(--border-subtle);padding:0.3rem 0.7rem;border-radius:var(--radius-pill);font-size:0.8rem;font-weight:600;color:var(--ink-secondary);">{html.escape(nb)}</span>'
      for nb in city_neighborhoods
  )

  city_faqs = city_info.get("faqs", [])
  city_faqs_html = ""
  if city_faqs:
    faq_cards = "".join(
        f"""
        <div style="background: var(--bg-elevated); border: 1px solid var(--border-hairline); border-radius: var(--radius-sm); padding: 1.05rem 1.25rem; margin-bottom: 0.75rem;">
          <h3 style="font-size: 0.98rem; font-weight: 700; color: var(--ink-primary); margin-bottom: 0.35rem;">{html.escape(f['question'])}</h3>
          <p style="font-size: 0.92rem; color: var(--ink-secondary); line-height: 1.65; margin: 0;">{html.escape(f['answer'])}</p>
        </div>"""
        for f in city_faqs
    )
    city_faqs_html = f"""
      <div style="margin-top: 2rem;">
        <h2 style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--ink-primary); margin-bottom: 0.85rem;">
          Preguntas frecuentes sobre planes en {html.escape(seo_city_label)}
        </h2>
        {faq_cards}
      </div>"""

  seo_bottom_section = f"""
    <section style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--border-hairline); max-width: 820px; color: var(--ink-secondary); font-size: 0.95rem;">
      <h2 style="font-family: var(--font-serif); font-size: 1.4rem; color: var(--ink-primary); margin-bottom: 0.65rem;">
        ¿Qué plan hacer en {html.escape(seo_city_label)} hoy y este fin de semana?
      </h2>
      <p style="margin-bottom: 0.85rem; line-height: 1.72;">
        {html.escape(city_seo_text)}
      </p>
      <div style="display:flex;flex-wrap:wrap;gap:0.45rem;margin-bottom:1.15rem;">
        {neighborhood_pills}
      </div>
      <p style="margin-bottom: 0.65rem; font-weight: 600; color: var(--ink-primary);">
        Índice completo de guías verificadas en {html.escape(seo_city_label)}:
      </p>
      <ul style="margin-left: 1.25rem; line-height: 1.75;">
        {''.join(guide_links)}
      </ul>
      {city_faqs_html}
    </section>"""

  og_img_rel = city_info.get(
      "ogImage", "images/planes-este-fin-de-semana-madrid-feria-barroca.jpg"
  )
  full_og_img = f"{SITE_URL}/{og_img_rel.lstrip('/')}"

  schema_ld = [
      {
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          "name": title,
          "description": description,
          "url": canonical_url,
          "inLanguage": "es-ES",
          "image": full_og_img,
      },
      {
          "@context": "https://schema.org",
          "@type": "ItemList",
          "name": h1,
          "numberOfItems": len(articles),
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

  if active_city == "all":
    schema_ld.append({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Qué Plan Hoy",
        "alternateName": "¿Qué Plan Hoy?",
        "url": f"{SITE_URL}/",
        "inLanguage": "es-ES",
        "publisher": {
            "@type": "Organization",
            "name": "Qué Plan Hoy",
            "url": f"{SITE_URL}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/favicon-512x512.png",
                "width": 512,
                "height": 512,
            },
        },
    })
    schema_ld.append({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Qué Plan Hoy",
        "alternateName": "¿Qué Plan Hoy?",
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/favicon-512x512.png",
    })
  else:
    schema_ld.append({
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
                "name": f"Planes en {active_city}",
                "item": canonical_url,
            },
        ],
    })
    if city_faqs:
      schema_ld.append({
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
              {
                  "@type": "Question",
                  "name": f["question"],
                  "acceptedAnswer": {"@type": "Answer", "text": f["answer"]},
              }
              for f in city_faqs
          ],
      })

  initial_kicker = (
      "GUÍA DE MADRID" if active_city == "all" else kicker
  )
  initial_h1 = CITIES["Madrid"]["h1"] if active_city == "all" else h1
  initial_subtitle = (
      CITIES["Madrid"]["intro"] if active_city == "all" else subtitle
  )

  page_html = f"""{render_head(title, description, canonical_url, root_prefix, schema_ld, og_image=full_og_img)}
<body>
  {render_header(root_prefix, active_city)}

  <main class="main-container">
    <section class="page-header-section" aria-labelledby="main-hero-heading">
      {city_selector_html}
      <span class="hero-kicker" id="main-hero-kicker">{html.escape(initial_kicker)}</span>
      <h1 class="hero-title" id="main-hero-heading">{html.escape(initial_h1)}</h1>
      <p class="hero-subtitle" id="main-hero-subtitle">{html.escape(initial_subtitle)}</p>

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

    {map_banner}

    <section aria-label="Guías de planes">
      <div class="articles-grid" id="articles-grid-container">
        {cards_html}
      </div>
    </section>

    {seo_bottom_section}
  </main>

  {render_footer(root_prefix)}
  {render_filter_script(active_city)}
</body>
</html>
"""
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(page_html)


def build_article_page(art: dict, all_articles: list):
  city_name = art["city"]
  city_info = CITIES.get(
      city_name,
      {
          "slug": city_name.lower(),
          "lat": 40.4168,
          "lng": -3.7038,
          "h1": f"Planes en {city_name}",
      },
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
  is_single_plan = art.get("articleType") == "single_plan"
  today_iso = date.today().isoformat()

  article_schema = {
      "@context": "https://schema.org",
      "@type": "Article",
      "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": canonical_url,
      },
      "headline": art["title"],
      "description": art["metaDescription"],
      "image": [full_img_url],
      "inLanguage": "es-ES",
      "datePublished": art["publishedAt"],
      "dateModified": today_iso,
      "about": {
          "@type": "City",
          "name": city_name,
      },
      "keywords": ", ".join(
          [f"planes en {city_name}", art["category"]]
          + art.get("neighborhoods", [])
      ),
      "author": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": f"{SITE_URL}/sobre-nosotros/",
      },
      "publisher": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": SITE_URL,
          "logo": {
              "@type": "ImageObject",
              "url": f"{SITE_URL}/favicon-512x512.png",
              "width": 512,
              "height": 512,
          },
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
              "description": sec["content"].replace("\n\n", " "),
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
  article_pins = []
  for idx, sec in enumerate(art.get("sections", []), start=1):
    venue_label = sec.get("venue", sec["heading"])
    toc_prefix = f"Paso {idx}: " if is_single_plan else f"{idx}. "
    toc_items.append(
        f'<li><a href="#plan-{idx}">{toc_prefix}{html.escape(venue_label)}</a></li>'
    )
    maps_query = urllib.parse.quote(f"{venue_label}, {city_name}, España")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
    article_pins.append({
        "idx": idx,
        "name": venue_label,
        "location": sec.get("location", ""),
        "price": sec.get("price", ""),
        "lat": sec.get("lat", city_info.get("lat", 40.4168)),
        "lng": sec.get("lng", city_info.get("lng", -3.7038)),
        "image": (
            f"{root_prefix}{sec['image'].lstrip('/')}"
            if sec.get("image")
            else img_src
        ),
        "mapsUrl": maps_url,
        "anchor": f"#plan-{idx}",
    })

  wa_text = urllib.parse.quote(
      f"Mira este plan en {city_name}: {art['title']} {canonical_url}"
  )
  wa_share_url = f"https://api.whatsapp.com/send?text={wa_text}"

  toc_heading = (
      "Guía paso a paso de este plan"
      if is_single_plan
      else "En este artículo"
  )
  toc_html = f"""
    <nav class="article-toc" aria-label="Índice del artículo">
      <div class="article-toc-header">
        <span class="article-toc-title">{toc_heading}</span>
        <a href="{wa_share_url}" target="_blank" rel="noopener" style="font-size: 0.78rem; font-weight: 600; color: var(--olive); text-decoration: none;">
          Enviar por WhatsApp ↗
        </a>
      </div>
      <ol class="article-toc-list">
        {''.join(toc_items)}
      </ol>
    </nav>"""

  map_title = (
      "🗺️ Mapa interactivo del recorrido (Pulsa en cada pin para abrir en Google Maps)"
      if is_single_plan
      else f"🗺️ Mapa con las ubicaciones en {html.escape(city_name)} (Pulsa un pin para ir a Google Maps)"
  )
  pins_json = json.dumps(article_pins, ensure_ascii=False)
  article_map_html = f"""
    <section style="margin: 1.75rem 0 2.25rem; background: var(--bg-sand); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); overflow: hidden;" aria-label="Mapa de ubicaciones del artículo">
      <div style="padding: 0.85rem 1.15rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; border-bottom: 1px solid var(--border-hairline);">
        <span style="font-size: 0.88rem; font-weight: 700; color: var(--ink-primary);">{map_title}</span>
        <a href="{root_prefix}mapa/?ciudad={urllib.parse.quote(city_name)}" style="font-size: 0.78rem; font-weight: 600; color: var(--terracotta); text-decoration: none;">
          Ver todos los planes de {html.escape(city_name)} en el gran mapa →
        </a>
      </div>
      <div id="article-leaflet-map" style="width: 100%; height: 340px; z-index: 1;"></div>
    </section>
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        var pins = {pins_json};
        if (!pins.length || typeof L === 'undefined') return;
        var map = L.map('article-leaflet-map', {{ scrollWheelZoom: false }});
        L.tileLayer('https://{{s}}.tile.openstreetmap.fr/hot/{{z}}/{{x}}/{{y}}.png', {{
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">HOT</a>',
          maxZoom: 19
        }}).addTo(map);
        var bounds = [];
        pins.forEach(function(p) {{
          bounds.push([p.lat, p.lng]);
          var icon = L.divIcon({{
            className: 'custom-num-pin',
            html: '<div style="background:#c84b31;color:#fff;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.3);">' + p.idx + '</div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15],
            popupAnchor: [0, -14]
          }});
          var popupHtml = '<div style="width:220px;font-family:Plus Jakarta Sans,sans-serif;">' +
            '<img src="' + p.image + '" alt="' + p.name.replace(/"/g, '&quot;') + '" style="width:100%;height:105px;object-fit:cover;border-radius:6px;margin-bottom:6px;display:block;" />' +
            '<div style="font-weight:700;font-size:13px;color:#1c1917;line-height:1.3;margin-bottom:4px;">' + p.idx + '. ' + p.name + '</div>' +
            '<div style="font-size:11.5px;color:#57534e;margin-bottom:8px;">' + p.price + '</div>' +
            '<a href="' + p.mapsUrl + '" target="_blank" rel="noopener" style="display:block;text-align:center;background:#c84b31;color:#fff;text-decoration:none;font-weight:600;font-size:12px;padding:6px 10px;border-radius:6px;">📍 Abrir pin en Google Maps ↗</a>' +
          '</div>';
          L.marker([p.lat, p.lng], {{ icon: icon }}).addTo(map).bindPopup(popupHtml);
        }});
        if (bounds.length === 1) {{
          map.setView(bounds[0], 15);
        }} else {{
          map.fitBounds(bounds, {{ padding: [38, 38], maxZoom: 15 }});
        }}
      }});
    </script>"""

  sections_html = []
  for idx, sec in enumerate(art.get("sections", []), start=1):
    venue_name = sec.get("venue", sec["heading"])
    maps_query = urllib.parse.quote(f"{venue_name}, {city_name}, España")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
    sec_img = sec.get("image", "")
    sec_alt = sec.get("imageAlt", venue_name)
    sec_img_html = ""
    if sec_img:
      sec_img_html = f"""
        <figure style="margin: 1.15rem 0 1.25rem; border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--border-subtle); background: var(--bg-sand);">
          <img src="{root_prefix}{html.escape(sec_img)}" alt="{html.escape(sec_alt)}" loading="lazy" width="800" height="450" style="width: 100%; height: auto; max-height: 420px; object-fit: cover; display: block;" />
          <figcaption style="padding: 0.55rem 0.95rem; font-size: 0.8rem; color: var(--ink-muted);">
            {html.escape(sec_alt)}
          </figcaption>
        </figure>"""

    paragraphs = [
        p.strip() for p in sec.get("content", "").split("\n\n") if p.strip()
    ]
    paragraphs_html = "\n        ".join(
        f'<p style="font-size: 1.05rem; color: var(--ink-primary); line-height: 1.78; margin-bottom: 0.95rem;">{html.escape(p)}</p>'
        for p in paragraphs
    )

    sections_html.append(f"""
      <section class="reader-section" id="plan-{idx}" style="scroll-margin-top: 90px;">
        <h2>{html.escape(sec['heading'])}</h2>
        {paragraphs_html}{sec_img_html}
        <div class="venue-meta-bar">
          <span><strong>Dónde:</strong> {html.escape(sec['location'])}</span>
          <span><strong>Precio:</strong> {html.escape(sec['price'])}</span>
          <a href="{maps_url}" target="_blank" rel="noopener" class="venue-map-link">📍 Abrir pin en Google Maps ↗</a>
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
        <div class="affiliate-info">
          <span class="affiliate-badge">{html.escape(aff.get('badge', 'Para completar el plan'))}</span>
          <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 0.3rem;">
            {html.escape(aff.get('title', ''))}
          </h3>
          <p style="font-size: 0.92rem; color: var(--ink-secondary);">
            {html.escape(aff.get('description', ''))}
          </p>
        </div>
        <div class="affiliate-action">
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

  page_html = f"""{render_head(art['metaTitle'], art['metaDescription'], canonical_url, root_prefix, [article_schema, itemlist_schema, faq_schema, breadcrumb_schema], full_img_url, include_leaflet=True, og_type="article")}
<body>
  {render_header(root_prefix, city_name)}

  <main class="main-container" style="max-width: 820px;">
    <nav aria-label="Migas de pan" style="font-size: 0.84rem; color: var(--ink-muted); margin-bottom: 1.25rem;">
      <a href="{root_prefix}" style="color: var(--ink-secondary); text-decoration: none;">Inicio</a>
      <span> / </span>
      <a href="{root_prefix}{city_slug}/" style="color: var(--ink-secondary); text-decoration: none;">Planes en {html.escape(city_name)}</a>
      <span> / </span>
      <span style="color: var(--ink-primary);">{html.escape(art['category'])}</span>
    </nav>

    <article>
      <div style="display: flex; gap: 0.5rem; align-items: center; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--terracotta); margin-bottom: 0.6rem; flex-wrap: wrap;">
        <a href="{root_prefix}{city_slug}/" style="color: var(--terracotta); text-decoration: none;">{html.escape(city_name)}</a>
        <span>·</span>
        <span>{html.escape(cat_header)}</span>
        <span>·</span>
        <span style="color: var(--ink-muted); font-weight: 500; text-transform: none; letter-spacing: 0;">{html.escape(art['priceRange'])}</span>
      </div>

      <h1 style="font-family: var(--font-serif); font-size: clamp(1.65rem, 3.4vw, 2.55rem); line-height: 1.18; margin-bottom: 0.9rem;">
        {html.escape(art['title'])}
      </h1>

      <p style="font-size: 1.05rem; color: var(--ink-secondary); margin-bottom: 1.35rem;">
        {html.escape(art['excerpt'])}
      </p>

      <figure style="margin: 0 0 1.6rem 0;">
        <img src="{img_src}" alt="{html.escape(img_alt)}" class="reader-hero-img" width="820" height="460" style="margin-bottom: 0.45rem;" />
        <figcaption style="font-size: 0.78rem; color: var(--ink-muted); text-align: right;">{html.escape(img_alt)}</figcaption>
      </figure>

      {toc_html}

      {article_map_html}

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
      <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.25rem;">
        <h2 style="font-family: var(--font-serif); font-size: 1.45rem; margin: 0;">
          Más planes en {html.escape(city_name)} que te pueden gustar
        </h2>
        <a href="{root_prefix}{city_slug}/" style="color:var(--terracotta);font-weight:700;font-size:0.9rem;text-decoration:none;">
          Ver todas las guías de {html.escape(city_name)} →
        </a>
      </div>
      <div class="related-articles-grid">
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

  # Crear redirección limpia en la raíz /<slug>/index.html hacia /<ciudad>/<slug>/ para evitar 404 si se omite la carpeta de ciudad
  redirect_dir = os.path.join(PUBLIC_DIR, art["slug"])
  os.makedirs(redirect_dir, exist_ok=True)
  redirect_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>{html.escape(art['metaTitle'])}</title>
  <link rel="canonical" href="{canonical_url}" />
  <meta name="robots" content="noindex, follow" />
  <meta http-equiv="refresh" content="0; url={canonical_url}" />
  <script>window.location.replace({json.dumps(canonical_url)});</script>
</head>
<body>
  <p>Redirigiendo a <a href="{canonical_url}">{html.escape(art['title'])}</a>...</p>
</body>
</html>
"""
  with open(os.path.join(redirect_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(redirect_html)


def build_map_page(articles: list):
  """Genera /mapa/index.html con todos los planes geolocalizados y redirección directa a Google Maps."""
  root_prefix = "../"
  output_path = os.path.join(PUBLIC_DIR, "mapa", "index.html")
  canonical_url = f"{SITE_URL}/mapa/"

  # Recopilar todos los pines únicos por (ciudad, nombre de lugar) para evitar duplicados exactos en la misma coordenada
  all_pins = []
  seen_coords = {}
  for art in articles:
    city = art["city"]
    city_slug = CITIES.get(city, {"slug": city.lower()})["slug"]
    art_url = f"../{city_slug}/{art['slug']}/"
    for idx, sec in enumerate(art.get("sections", []), start=1):
      venue_name = sec.get("venue", sec["heading"])
      lat = float(sec.get("lat", CITIES.get(city, {}).get("lat", 40.4168)))
      lng = float(sec.get("lng", CITIES.get(city, {}).get("lng", -3.7038)))
      # Pequeño offset si dos planes comparten exactamente la misma coordenada para que ambos pines se puedan pulsar
      coord_key = (round(lat, 4), round(lng, 4))
      occ = seen_coords.get(coord_key, 0)
      seen_coords[coord_key] = occ + 1
      if occ > 0:
        lat += 0.00045 * ((occ + 1) // 2) * (1 if occ % 2 == 1 else -1)
        lng += 0.00045 * ((occ + 1) // 2) * (1 if occ % 2 == 0 else -1)

      maps_query = urllib.parse.quote(f"{venue_name}, {city}, España")
      maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
      img_rel = sec.get("image") or art.get("image", "")
      all_pins.append({
          "id": f"{art['id']}-{idx}",
          "name": venue_name,
          "heading": sec["heading"],
          "city": city,
          "category": art["category"],
          "location": sec.get("location", ""),
          "price": sec.get("price", ""),
          "lat": round(lat, 5),
          "lng": round(lng, 5),
          "image": f"../{img_rel.lstrip('/')}",
          "mapsUrl": maps_url,
          "articleUrl": f"{art_url}#plan-{idx}",
          "articleTitle": art["title"],
      })

  pins_json = json.dumps(all_pins, ensure_ascii=False)
  cities_coords_json = json.dumps(
      {
          k: {"lat": v["lat"], "lng": v["lng"], "zoom": v["zoom"]}
          for k, v in CITIES.items()
      },
      ensure_ascii=False,
  )

  map_schema = {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": (
          "Mapa de Planes en Madrid, Barcelona, Valencia, Sevilla y Toledo |"
          " Qué Plan Hoy"
      ),
      "description": (
          "Mapa interactivo con todos los planes originales, gratuitos y en"
          " pareja de Qué Plan Hoy con enlace directo al pin en Google Maps."
      ),
      "url": canonical_url,
  }

  page_html = f"""{render_head("Mapa de Planes en Madrid, Barcelona, Valencia, Sevilla y Toledo | Qué Plan Hoy", "Explora en nuestro mapa interactivo más de 100 planes originales, jardines secretos y rutas gratis en Madrid, Barcelona, Valencia, Sevilla y Toledo con enlace directo a Google Maps.", canonical_url, root_prefix, [map_schema], include_leaflet=True)}
<body>
  {render_header(root_prefix, "mapa")}

  <main class="main-container">
    <section class="page-header-section" style="margin-bottom: 1.5rem;">
      <span class="hero-kicker">MAPA INTERACTIVO CON REDIRECCIÓN A GOOGLE MAPS</span>
      <h1 class="hero-title">Mapa de Planes: todos nuestros rincones geolocalizados</h1>
      <p class="hero-subtitle">
        Filtra por ciudad o tipo de plan, pulsa en cualquier chincheta para ver su fotografía real y abre directamente el pin exacto en <strong>Google Maps</strong> para calcular cómo llegar.
      </p>

      <div style="display: flex; flex-wrap: wrap; gap: 0.65rem; margin-top: 1.1rem; align-items: center;">
        <span style="font-size: 0.82rem; font-weight: 700; color: var(--ink-secondary); margin-right: 0.25rem;">Ciudad:</span>
        <button type="button" class="style-pill-btn city-map-btn active" data-city="all">Todas ({len(all_pins)})</button>
        <button type="button" class="style-pill-btn city-map-btn" data-city="Madrid">Madrid</button>
        <button type="button" class="style-pill-btn city-map-btn" data-city="Barcelona">Barcelona</button>
        <button type="button" class="style-pill-btn city-map-btn" data-city="Valencia">Valencia</button>
        <button type="button" class="style-pill-btn city-map-btn" data-city="Sevilla">Sevilla</button>
        <button type="button" class="style-pill-btn city-map-btn" data-city="Toledo">Toledo</button>
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: 0.55rem; margin-top: 0.75rem; align-items: center;">
        <span style="font-size: 0.82rem; font-weight: 700; color: var(--ink-secondary); margin-right: 0.25rem;">Categoría:</span>
        <button type="button" class="style-pill-btn cat-map-btn active" data-cat="all">Todos los planes</button>
        <button type="button" class="style-pill-btn cat-map-btn" data-cat="Gratis y Baratos">💸 Gratis y baratos</button>
        <button type="button" class="style-pill-btn cat-map-btn" data-cat="Este Fin de Semana">📅 Este fin de semana</button>
        <button type="button" class="style-pill-btn cat-map-btn" data-cat="Planes Diferentes">✨ Planes diferentes</button>
        <button type="button" class="style-pill-btn cat-map-btn" data-cat="En Pareja">❤️ En pareja</button>
      </div>
    </section>

    <section style="border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--border-subtle); box-shadow: 0 8px 28px rgba(28, 25, 23, 0.07); margin-bottom: 2.25rem;">
      <div id="global-plans-map" style="width: 100%; height: 540px; z-index: 1;"></div>
    </section>

    <section aria-labelledby="pins-list-heading">
      <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
        <h2 id="pins-list-heading" style="font-family: var(--font-serif); font-size: 1.45rem;">
          Planes mostrados en el mapa (<span id="visible-pins-count">{len(all_pins)}</span>)
        </h2>
      </div>
      <div id="pins-cards-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)); gap: 1.1rem;"></div>
    </section>
  </main>

  {render_footer(root_prefix)}

  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      var allPins = {pins_json};
      var cityCoords = {cities_coords_json};
      var selectedCity = 'all';
      var selectedCat = 'all';

      // Comprobar si viene ?ciudad=Madrid en la URL
      var params = new URLSearchParams(window.location.search);
      var urlCity = params.get('ciudad');
      if (urlCity && cityCoords[urlCity]) {{
        selectedCity = urlCity;
        document.querySelectorAll('.city-map-btn').forEach(function(b) {{
          b.classList.toggle('active', b.getAttribute('data-city') === selectedCity);
        }});
      }}

      var map = L.map('global-plans-map').setView([40.2, -3.5], 6);
      var osmHotLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.fr/hot/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">HOT</a>',
        maxZoom: 19
      }}).addTo(map);
      var esriStreetLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        attribution: 'Tiles &copy; Esri',
        maxZoom: 19
      }});
      L.control.layers({{
        "Callejero Editorial (ES)": osmHotLayer,
        "Mapa Detallado (Esri)": esriStreetLayer
      }}, null, {{ position: 'topright' }}).addTo(map);

      var markersLayer = (typeof L.markerClusterGroup === 'function')
        ? L.markerClusterGroup({{
            showCoverageOnHover: false,
            maxClusterRadius: 42,
            spiderfyOnMaxZoom: true,
            iconCreateFunction: function(cluster) {{
              var count = cluster.getChildCount();
              var size = count > 20 ? 44 : (count > 10 ? 38 : 34);
              return L.divIcon({{
                html: '<div style="background:#c84b31;color:#fff;width:' + size + 'px;height:' + size + 'px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13.5px;border:3px solid #fff;box-shadow:0 3px 10px rgba(28,25,23,0.35);font-family:Plus Jakarta Sans,sans-serif;">' + count + '</div>',
                className: 'custom-cluster-pin',
                iconSize: [size, size]
              }});
            }}
          }}).addTo(map)
        : L.layerGroup().addTo(map);
      var markerRefs = {{}};

      window.focusPinOnMap = function(pinId) {{
        var m = markerRefs[pinId];
        if (!m) return;
        document.getElementById('global-plans-map').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        if (typeof markersLayer.zoomToShowLayer === 'function') {{
          markersLayer.zoomToShowLayer(m, function() {{
            m.openPopup();
          }});
        }} else {{
          map.setView(m.getLatLng(), 16);
          m.openPopup();
        }}
      }};

      function renderPins(shouldRebound) {{
        markersLayer.clearLayers();
        markerRefs = {{}};
        var grid = document.getElementById('pins-cards-grid');
        grid.innerHTML = '';
        var filtered = allPins.filter(function(p) {{
          var okCity = (selectedCity === 'all' || p.city === selectedCity);
          var okCat = (selectedCat === 'all' || p.category === selectedCat);
          return okCity && okCat;
        }});

        document.getElementById('visible-pins-count').textContent = filtered.length;
        var bounds = [];

        filtered.forEach(function(p) {{
          bounds.push([p.lat, p.lng]);
          var pinColor = p.category === 'Gratis y Baratos' ? '#2e6f40' : (p.category === 'En Pareja' ? '#b83253' : '#c84b31');
          var icon = L.divIcon({{
            className: 'global-custom-pin',
            html: '<div style="background:' + pinColor + ';color:#fff;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.3);">📍</div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15],
            popupAnchor: [0, -14]
          }});

          var popupHtml = '<div style="width:235px;font-family:Plus Jakarta Sans,sans-serif;">' +
            '<img src="' + p.image + '" alt="' + p.name.replace(/"/g, '&quot;') + '" style="width:100%;height:115px;object-fit:cover;border-radius:6px;margin-bottom:7px;display:block;" />' +
            '<div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#c84b31;margin-bottom:2px;">' + p.city + ' · ' + p.category + '</div>' +
            '<div style="font-weight:700;font-size:13.5px;color:#1c1917;line-height:1.3;margin-bottom:4px;">' + p.name + '</div>' +
            '<div style="font-size:11.5px;color:#57534e;margin-bottom:4px;">' + p.location + '</div>' +
            '<div style="font-size:11.5px;font-weight:600;color:#2e6f40;margin-bottom:8px;">' + p.price + '</div>' +
            '<div style="display:flex;flex-direction:column;gap:5px;">' +
              '<a href="' + p.mapsUrl + '" target="_blank" rel="noopener" style="display:block;text-align:center;background:#c84b31;color:#fff;text-decoration:none;font-weight:600;font-size:12px;padding:6px 10px;border-radius:6px;">📍 Abrir pin en Google Maps ↗</a>' +
              '<a href="' + p.articleUrl + '" style="display:block;text-align:center;background:#f5f2eb;color:#1c1917;text-decoration:none;font-weight:600;font-size:11.5px;padding:5px 10px;border-radius:6px;border:1px solid #e5e0d5;">📖 Leer el plan completo →</a>' +
            '</div>' +
          '</div>';

          var m = L.marker([p.lat, p.lng], {{ icon: icon }}).bindPopup(popupHtml);
          markersLayer.addLayer(m);
          markerRefs[p.id] = m;

          var card = document.createElement('div');
          card.style.cssText = 'background:var(--bg-elevated);border:1px solid var(--border-subtle);border-radius:var(--radius-md);overflow:hidden;display:flex;flex-direction:column;';
          card.innerHTML =
            '<img src="' + p.image + '" alt="' + p.name.replace(/"/g, '&quot;') + '" loading="lazy" style="width:100%;height:150px;object-fit:cover;display:block;cursor:pointer;" data-pin-id="' + p.id + '" onclick="focusPinOnMap(this.dataset.pinId)" />' +
            '<div style="padding:0.95rem 1.05rem;display:flex;flex-direction:column;flex:1;">' +
              '<div style="font-size:0.73rem;font-weight:700;text-transform:uppercase;color:var(--terracotta);margin-bottom:0.25rem;">' + p.city + ' · ' + p.category + '</div>' +
              '<h3 style="font-family:var(--font-serif);font-size:1.05rem;line-height:1.28;margin-bottom:0.35rem;cursor:pointer;" data-pin-id="' + p.id + '" onclick="focusPinOnMap(this.dataset.pinId)">' + p.name + '</h3>' +
              '<p style="font-size:0.83rem;color:var(--ink-secondary);margin-bottom:0.35rem;">' + p.location + '</p>' +
              '<p style="font-size:0.82rem;font-weight:600;color:var(--olive);margin-bottom:0.85rem;">' + p.price + '</p>' +
              '<div style="margin-top:auto;display:flex;gap:0.4rem;flex-wrap:wrap;">' +
                '<button type="button" data-pin-id="' + p.id + '" onclick="focusPinOnMap(this.dataset.pinId)" style="flex:1;text-align:center;background:var(--bg-sand);color:var(--ink-primary);border:1px solid var(--border-subtle);font-weight:600;font-size:0.78rem;padding:0.48rem 0.5rem;border-radius:var(--radius-sm);cursor:pointer;">🎯 Ver en mapa</button>' +
                '<a href="' + p.mapsUrl + '" target="_blank" rel="noopener" style="flex:1;text-align:center;background:var(--terracotta);color:#fff;text-decoration:none;font-weight:600;font-size:0.78rem;padding:0.48rem 0.5rem;border-radius:var(--radius-sm);">📍 Maps ↗</a>' +
                '<a href="' + p.articleUrl + '" style="flex:1;text-align:center;background:var(--bg-sand);color:var(--ink-primary);text-decoration:none;font-weight:600;font-size:0.78rem;padding:0.48rem 0.5rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">Guía →</a>' +
              '</div>' +
            '</div>';
          grid.appendChild(card);
        }});

        if (shouldRebound && bounds.length > 0) {{
          if (selectedCity !== 'all' && cityCoords[selectedCity]) {{
            map.fitBounds(bounds, {{ padding: [40, 40], maxZoom: 14 }});
          }} else {{
            map.fitBounds(bounds, {{ padding: [35, 35], maxZoom: 12 }});
          }}
        }}
      }}

      document.querySelectorAll('.city-map-btn').forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          document.querySelectorAll('.city-map-btn').forEach(function(b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
          selectedCity = btn.getAttribute('data-city');
          renderPins(true);
        }});
      }});

      document.querySelectorAll('.cat-map-btn').forEach(function(btn) {{
        btn.addEventListener('click', function() {{
          document.querySelectorAll('.cat-map-btn').forEach(function(b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
          selectedCat = btn.getAttribute('data-cat');
          renderPins(true);
        }});
      }});

      renderPins(true);
    }});
  </script>
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
      "name": "Sobre Qué Plan Hoy: Por Qué Nace Esta Guía y Criterio Editorial",
      "url": canonical_url,
      "mainEntity": {
          "@type": "Organization",
          "name": "Qué Plan Hoy",
          "url": SITE_URL,
          "logo": f"{SITE_URL}/favicon-512x512.png",
          "description": (
              "Guía local e independiente de planes originales, agendas"
              " municipales de festivos, rutas paso a paso, planes gratis y"
              " citas en pareja en Madrid, Barcelona, Valencia, Sevilla y"
              " Toledo."
          ),
      },
  }
  page_html = f"""{render_head("Sobre Nosotros: Por Qué Nace Qué Plan Hoy y Criterio Editorial", "Descubre por qué nació ¿Qué Plan Hoy? (queplanhoy.es): una guía local, honesta y sin relleno para encontrar planes reales hoy y este fin de semana.", canonical_url, root_prefix, [org_schema])}
<body>
  {render_header(root_prefix, "none")}
  <main class="main-container" style="max-width: 760px;">
    <span class="hero-kicker">SOBRE QUÉ PLAN HOY · NUESTRA HISTORIA</span>
    <h1 class="hero-title" style="margin-bottom: 1.15rem;">Por qué nace ¿Qué Plan Hoy?</h1>
    <p style="font-size: 1.08rem; color: var(--ink-secondary); line-height: 1.75; margin-bottom: 1.75rem;">
      <strong>¿Qué Plan Hoy?</strong> comenzó como una pregunta que todos nos hacemos cada jueves o viernes por la tarde y que en internet casi nunca tenía una buena respuesta.
    </p>

    <section class="reader-section">
      <h2>El problema de buscar un plan hoy en internet</h2>
      <p style="margin-top: 0.65rem; line-height: 1.75;">
        La pregunta era sencilla: <em>«¿qué hacemos hoy o este puente?»</em>. Sin embargo, cada búsqueda en internet devolvía siempre lo mismo: páginas saturadas de anuncios intrusivos que tapan la pantalla del móvil, listas interminables de diez párrafos de relleno antes de decirte dónde está el sitio, notas de prensa copiadas sin verificar o las mismas recomendaciones turísticas que parecen sacadas de un folleto de hace quince años.
      </p>
      <p style="margin-top: 0.75rem; line-height: 1.75;">
        Nuestras ciudades —<strong>Madrid, Toledo, Barcelona, Valencia y Sevilla</strong>— tienen un ritmo, unos barrios y un calendario cultural vivo que ningún agregador genérico sabe contar bien. <strong>¿Qué Plan Hoy? existe para cambiar eso.</strong>
      </p>
    </section>

    <section class="reader-section" style="border-bottom: none;">
      <h2>Una guía hecha desde dentro (y cero relleno)</h2>
      <p style="margin-top: 0.65rem; line-height: 1.75;">
        Nuestro compromiso editorial se basa en cuatro reglas que aplicamos en cada guía que publicamos:
      </p>
      <ul style="margin: 0.9rem 0 0 1.25rem; line-height: 1.85;">
        <li style="margin-bottom: 0.55rem;"><strong>Agendas oficiales de Ayuntamientos en festivos y puentes:</strong> Cuando llega una fecha señalada (como el <em>12 de Octubre y la Fiesta de la Hispanidad en Madrid</em>, el <em>Puente de Todos los Santos en Toledo</em> o el <em>9 d'Octubre en Valencia</em>), consultamos directamente los programas oficiales de los Ayuntamientos y Comunidades Autónomas para explicarte los eventos reales que suceden en la calle: recorridos de desfiles, escenarios de conciertos gratuitos en plazas, jornadas de puertas abiertas y qué bocas de Metro o calles cortadas conviene evitar.</li>
        <li style="margin-bottom: 0.55rem;"><strong>Planes de un único rincón a fondo y selecciones con sentido:</strong> No creemos en poner siempre 5 o 10 planes porque sí. Hay mañanas de domingo en las que el mejor plan es dedicarle tres horas a un único lugar explicado paso a paso (como el <em>Parque de El Capricho</em>, el <em>Laberinto de Horta</em> o la <em>Senda Ecológica del Tajo</em>), y días de lluvia en los que necesitas cinco refugios cubiertos con encanto para elegir.</li>
        <li style="margin-bottom: 0.55rem;"><strong>Datos prácticos al grano (horario, transporte, precio y pin en Google Maps):</strong> Ni quien vive en la ciudad ni quien viene de escapada tiene tiempo de leer párrafos vacíos antes de saber a qué hora cierra un jardín o cuánto cuesta la entrada. Cada parada incluye dirección exacta, parada de Metro, Cercanías o autobús, precio real verificado y enlace directo al <strong>pin exacto en Google Maps</strong>.</li>
        <li><strong>Fotografías reales verificadas:</strong> Todas las fotografías que ilustran nuestros planes corresponden a imágenes reales de los monumentos, jardines, calles y eventos, para que sepas exactamente qué vas a encontrar al llegar.</li>
      </ul>
      <div style="margin-top: 1.5rem; display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <a href="/" style="background: var(--terracotta); color: #fff; text-decoration: none; font-weight: 700; font-size: 0.9rem; padding: 0.65rem 1.2rem; border-radius: var(--radius-pill);">Explorar planes por ciudad →</a>
        <a href="/mapa/" style="background: var(--bg-sand); color: var(--ink-primary); border: 1px solid var(--border-strong); text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 0.65rem 1.2rem; border-radius: var(--radius-pill);">🗺️ Abrir Mapa Interactivo</a>
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


def build_privacy_cookies_page():
  output_path = os.path.join(PUBLIC_DIR, "privacidad-y-cookies", "index.html")
  root_prefix = "../"
  canonical_url = f"{SITE_URL}/privacidad-y-cookies/"
  page_html = f"""{render_head("Aviso Legal, Privacidad y Política de Cookies | Qué Plan Hoy", "Aviso legal, condiciones de uso, descargo de responsabilidad sobre eventos, política de privacidad RGPD y gestión de cookies de Qué Plan Hoy (queplanhoy.es).", canonical_url, root_prefix, [], robots="noindex, follow")}
<body>
  <script>
    (function() {{
      try {{
        var saved = localStorage.getItem('qph_cookie_consent_v1');
        var ref = document.referrer || '';
        if (!saved && ref.indexOf('queplanhoy.es') === -1 && ref.indexOf('localhost') === -1) {{
          window.location.replace('/');
        }}
      }} catch (e) {{}}
    }})();
  </script>
  {render_header(root_prefix, "none")}
  <main class="main-container" style="max-width: 760px;">
    <div style="margin-bottom: 1.35rem;">
      <a href="/" style="display:inline-flex;align-items:center;gap:0.45rem;background:var(--terracotta);color:#fff;text-decoration:none;font-weight:700;font-size:0.9rem;padding:0.6rem 1.1rem;border-radius:10px;box-shadow:0 4px 12px rgba(200,75,49,0.22);">← Ir a la página principal de planes</a>
    </div>
    <span class="hero-kicker">INFORMACIÓN LEGAL · RGPD, LOPDGDD Y LSSI-CE</span>
    <h1 class="hero-title" style="margin-bottom: 1.1rem;">Aviso Legal, Privacidad y Política de Cookies</h1>
    <p style="font-size: 1.02rem; color: var(--ink-secondary); line-height: 1.7; margin-bottom: 1.65rem;">
      En <strong>¿Qué Plan Hoy?</strong> (<code>queplanhoy.es</code>) apostamos por la transparencia y la claridad, sin letra pequeña. En esta página encontrarás las condiciones de uso de nuestra guía, el alcance de la información publicada sobre eventos y cómo protegemos tu privacidad conforme al Reglamento General de Protección de Datos (RGPD).
    </p>

    <section class="reader-section">
      <h2>1. Finalidad del sitio web y condiciones de uso</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        <strong>¿Qué Plan Hoy?</strong> (<code>https://queplanhoy.es</code>) es una guía cultural y de ocio independiente de acceso gratuito que publica y selecciona información sobre eventos municipales, rutas urbanas, patrimonio histórico y actividades en ciudades de España (Madrid, Barcelona, Valencia, Sevilla y Toledo). El acceso y navegación por el sitio web son gratuitos y atribuyen la condición de usuario, implicando la aceptación del presente Aviso Legal y Política de Privacidad.
      </p>
    </section>

    <section class="reader-section">
      <h2>2. Descargo de responsabilidad sobre la información de eventos, horarios y precios</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        Los detalles de los eventos, monumentos, museos, jardines y actividades publicados en <strong>queplanhoy.es</strong> (incluyendo fechas, horarios de apertura, tarifas, franjas de entrada gratuita, recorridos de desfiles y ubicaciones) se obtienen y contrastan a partir de fuentes oficiales municipales (Ayuntamientos y Comunidades Autónomas), organismos públicos, recintos culturales y plataformas oficiales de venta en el momento de su redacción.
      </p>
      <p style="margin-top: 0.65rem; line-height: 1.72;">
        No obstante, los organizadores, ayuntamientos o recintos pueden modificar horarios, tarifas, aforos o cancelar actividades sin previo aviso (por ejemplo, por alertas meteorológicas en parques históricos o cambios de protocolo en actos oficiales). Por ello, <strong>¿Qué Plan Hoy? ofrece esta información con fines informativos y orientativos, y no asume responsabilidad por cambios imprevistos, cancelaciones, errores u omisiones de terceros</strong>. Recomendamos verificar siempre los detalles actualizados directamente en la web oficial del organizador o recinto antes de desplazarse.
      </p>
    </section>

    <section class="reader-section">
      <h2>3. Enlaces a terceros y transparencia de afiliación</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        Para facilitar la planificación al lector, nuestras guías incluyen enlaces externos tanto a portales institucionales y webs oficiales de museos como a plataformas autorizadas de reserva de entradas y visitas guiadas (como <strong>Tiqets</strong>, <strong>Civitatis</strong> o la red <strong>Travelpayouts</strong>).
      </p>
      <p style="margin-top: 0.65rem; line-height: 1.72;">
        Algunos de estos enlaces son enlaces de afiliación: si reservas tu entrada a través de ellos, <em>Qué Plan Hoy</em> puede recibir una pequeña comisión del proveedor sin que ello suponga ningún sobrecoste ni variación en el precio oficial para ti. Cualquier compra o reserva se celebra única y exclusivamente entre el usuario y la plataforma proveedora correspondiente; <em>Qué Plan Hoy</em> no interviene en la transacción ni asume responsabilidad sobre la prestación del servicio de dichos terceros.
      </p>
    </section>

    <section class="reader-section">
      <h2>4. Política de Cookies y cómo configurar tu consentimiento</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        Al navegar por <strong>queplanhoy.es</strong> se pueden emplear dos tipos de almacenamiento local o cookies:
      </p>
      <ul style="margin: 0.85rem 0 0 1.25rem; line-height: 1.8;">
        <li style="margin-bottom: 0.45rem;"><strong>Almacenamiento técnico y de preferencias (Estrictamente necesario):</strong> Guarda en tu propio navegador (<code>localStorage</code>) tu decisión sobre el aviso de cookies (<code>qph_cookie_consent_v1</code>), recuerda la última ciudad que has consultado en la portada (<code>qph_preferred_city</code>) para no mezclarte planes de otras ciudades y permite visualizar los mapas interactivos de OpenStreetMap / Leaflet.</li>
        <li><strong>Cookies de atribución y reserva de entradas (Terceros):</strong> Cuando aceptas las cookies o interactúas con enlaces de plataformas colaboradoras de entradas (Tiqets / Travelpayouts), estos proveedores pueden utilizar una cookie técnica de atribución para reconocer que la visita procede de <em>Qué Plan Hoy</em>.</li>
      </ul>
      <p style="margin-top: 0.8rem; line-height: 1.72;">
        <strong>Retirada o cambio del consentimiento en 1 clic:</strong> De conformidad con el artículo 13.2.c) del RGPD, puedes cambiar o retirar tu consentimiento en cualquier momento pulsando en <button type="button" onclick="window.openCookieBanner && window.openCookieBanner()" style="background:none;border:none;padding:0;font:inherit;color:var(--terracotta);font-weight:700;cursor:pointer;text-decoration:underline;">Configurar cookies</button> (también disponible en el pie de página de toda la web) o eliminando los datos de navegación desde la configuración de tu navegador.
      </p>
    </section>

    <section class="reader-section">
      <h2>5. Protección de datos personales y derechos RGPD / AEPD</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        En <strong>queplanhoy.es</strong> no exigimos registro de usuarios, no contamos con formularios que recopilen datos personales identificables ni vendemos ni cedemos listados de datos a terceros. Los únicos datos técnicos tratados durante la navegación (como la dirección IP necesaria para servir las páginas a través de la infraestructura de alojamiento web en GitHub Pages) se procesan sobre la base del interés legítimo para garantizar la seguridad técnica y el funcionamiento del servicio.
      </p>
      <p style="margin-top: 0.65rem; line-height: 1.72;">
        Como usuario, la normativa europea (RGPD) y española (LOPDGDD) te garantiza en todo momento el ejercicio de los siguientes derechos:
      </p>
      <ul style="margin: 0.75rem 0 0 1.25rem; line-height: 1.8;">
        <li><strong>Derecho de acceso, rectificación y supresión (derecho al olvido).</strong></li>
        <li><strong>Derecho a la limitación del tratamiento, portabilidad y oposición.</strong></li>
        <li><strong>Derecho a presentar una reclamación ante la Autoridad de Control:</strong> Si consideras que el tratamiento de datos vulnera la normativa vigente, tienes derecho a acudir ante la <strong>Agencia Española de Protección de Datos (AEPD)</strong> a través de su sede electrónica oficial en <a href="https://www.aepd.es/" target="_blank" rel="noopener noreferrer" style="color:var(--terracotta);font-weight:600;">https://www.aepd.es/</a>.</li>
      </ul>
    </section>

    <section class="reader-section" style="border-bottom: none;">
      <h2>6. Propiedad intelectual y prohibición de extracción automatizada</h2>
      <p style="margin-top: 0.55rem; line-height: 1.72;">
        El diseño editorial, la estructura, el código fuente, los textos originales de las rutas, los mapas interactivos, el logotipo y las creatividades gráficas propias de <strong>¿Qué Plan Hoy?</strong> están protegidos por la legislación española e internacional sobre propiedad intelectual e industrial. Queda expresamente prohibida la reproducción, distribución, reutilización o extracción sistemática o automatizada (<em>web scraping</em>) de los contenidos de este sitio web con fines comerciales o para la creación o entrenamiento de servicios competidores sin autorización expresa.
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
      f"  <url>\n    <loc>{SITE_URL}/mapa/</loc>\n   "
      f" <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n   "
      " <priority>0.9</priority>\n  </url>",
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
    urls.append(
        f"  <url>\n    <loc>{SITE_URL}/{c_slug}/{art['slug']}/</loc>\n   "
        f" <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n   "
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
          "¿Qué planes hacer hoy o este fin de semana? Guía local de rutas"
          " paso a paso, ferias, ideas gratis, citas en pareja y"
          " mapa interactivo en Madrid, Barcelona, Valencia, Sevilla y Toledo."
      ),
      canonical_url=f"{SITE_URL}/",
      h1="Planes originales en tu ciudad: qué hacer fuera de lo típico",
      subtitle=(
          "Rutas explicadas paso a paso, ferias de fin de semana,"
          " jardines secretos y citas en pareja en Madrid, Barcelona,"
          " Valencia, Sevilla y Toledo."
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

  build_map_page(articles)
  build_about_page()
  build_privacy_cookies_page()
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
      f" {len(articles)} guías + /mapa/ + /sobre-nosotros/ + /privacidad-y-cookies/ + CNAME + sitemap.xml."
  )


if __name__ == "__main__":
  build_all()
