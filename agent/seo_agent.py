#!/usr/bin/env python3
"""Agente Automatizado de Contenido SEO para HoyQuePlan (Madrid, Barcelona, Valencia, Sevilla y Toledo)."""

import argparse
from datetime import date
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "data", "articles.json")
QUEUE_FILE = os.path.join(BASE_DIR, "data", "keyword_queue.json")
SITEMAP_FILE = os.path.join(BASE_DIR, "public", "sitemap.xml")

CITY_KNOWLEDGE_BASE = {
    "Madrid": {
        "image": "/images/madrid.jpg",
        "neighborhoods": [
            "Malasaña",
            "Chamberí",
            "Barrio de las Letras",
            "La Latina",
            "Lavapiés",
            "Retiro",
        ],
        "venues": [
            {
                "name": "Invernadero del Palacio de Cristal de Arganzuela",
                "location": "Paseo de la Chopera, 10 (Metro: Legazpi - L3, L6)",
                "price": "Acceso 100% gratuito",
                "desc": (
                    "Un gigantesco invernadero de hierro y cristal del siglo XX"
                    " con más de 9.000 especies de plantas tropicales,"
                    " desérticas y estanques con peces. Es cubierto, cálido y"
                    " perfecto en cualquier época del año."
                ),
            },
            {
                "name": "Jardín Cubierto de Salvador Bachiller en Montera",
                "location": "Calle de la Montera, 37 (Metro: Gran Vía - L1, L5)",
                "price": "Té especial o infusión con tarta casera: 6,50 € – 9,00 €",
                "desc": (
                    "Subiendo por el interior de la tienda se encuentra una"
                    " azotea acristalada cubierta de plantas colgantes donde"
                    " refugiarse del ruido o de la lluvia en pleno centro."
                ),
            },
            {
                "name": "Museo Cerralbo y su Salón de Baile del siglo XIX",
                "location": (
                    "Calle de Ventura Rodríguez, 17 (Metro: Plaza de España -"
                    " L3, L10)"
                ),
                "price": (
                    "3,00 € entrada general (Gratis jueves de 17:00 a 20:00 y"
                    " domingos)"
                ),
                "desc": (
                    "A diferencia de los grandes museos masificados, este"
                    " palacio conserva intacta la decoración original de 1893"
                    " con espejos venecianos y lámparas de cristal."
                ),
            },
        ],
        "affiliate": {
            "partner": "Fever / Civitatis",
            "badge": "Top Experiencia en Madrid",
            "title": (
                "Exposiciones Inmersivas y Conciertos Candlelight a Cubierto en"
                " Madrid"
            ),
            "description": (
                "Descubre las experiencias culturales mejor valoradas de esta"
                " semana en Madrid: desde conciertos a la luz de las velas"
                " hasta rutas históricas."
            ),
            "price": "Desde 15 € por persona",
            "ctaText": "Ver experiencias disponibles esta semana →",
            "commissionNote": (
                "Enlace de afiliado Fever/Civitatis (Comisión media: 10%)"
            ),
        },
    },
    "Barcelona": {
        "image": "/images/barcelona.jpg",
        "neighborhoods": [
            "El Born",
            "Gràcia",
            "Horta-Guinardó",
            "Poblenou",
            "Montjuïc",
            "Sant Antoni",
        ],
        "venues": [
            {
                "name": "Parque del Laberinto de Horta",
                "location": (
                    "Passeig dels Castanyers, 1 (Metro: Mundet - L3, salida"
                    " Velòdrom)"
                ),
                "price": "2,23 € entrada general (Gratis miércoles y domingos)",
                "desc": (
                    "Un jardín neoclásico del siglo XVIII con un laberinto de"
                    " cipreses recortados, templos de columnas italianas,"
                    " estanques románticos y cascadas."
                ),
            },
            {
                "name": "Vermut artesanal y jazz en directo en Gràcia y El Born",
                "location": (
                    "Plaça de la Virreina / Carrer dels Flassaders (Metro:"
                    " Fontana L3 / Jaume I L4)"
                ),
                "price": (
                    "Vermut casero + olivas rellenas y patatas bravas: 7,50 €"
                    " por persona"
                ),
                "desc": (
                    "Huye de las Ramblas y siéntate en las terrazas históricas"
                    " de la Plaça de la Virreina, seguido de una sesión"
                    " acústica en los sótanos abovedados del Born."
                ),
            },
            {
                "name": "Refugio Antiaéreo 307 de Poble-sec y jardines de Miramar",
                "location": "Carrer Nou de la Rambla, 175 (Metro: Paral·lel - L2, L3)",
                "price": "Gratis domingos desde las 15:00 h (3,50 € resto de días)",
                "desc": (
                    "Casi 400 metros de túneles excavados en la falda de"
                    " Montjuïc por los vecinos en 1937, conservados intactos."
                ),
            },
        ],
        "affiliate": {
            "partner": "GetYourGuide / TheFork",
            "badge": "Plan Estrella en Barcelona",
            "title": (
                "Ruta de Tapas, Vino y Jazz en Vivo por el Barrio Gótico y El"
                " Born"
            ),
            "description": (
                "Recorre bodegas centenarias de Barcelona con degustación de"
                " vinos catalanes y tapas artesanas o reserva mesa con"
                " descuento."
            ),
            "price": "Desde 19 € por persona",
            "ctaText": "Ver disponibilidad y descuentos →",
            "commissionNote": (
                "Enlace de afiliado GetYourGuide / TheFork (Comisión: 10% - 12%)"
            ),
        },
    },
    "Valencia": {
        "image": "/images/valencia.jpg",
        "neighborhoods": [
            "El Cabanyal",
            "Ruzafa",
            "El Carmen",
            "Exposición / Monforte",
            "L'Albufera",
        ],
        "venues": [
            {
                "name": "Jardines de Monforte (El jardín neoclásico escondido de Valencia)",
                "location": (
                    "Plaza de la Legión Española, s/n (Metro: Facultats - L3,"
                    " L9)"
                ),
                "price": "Acceso 100% gratuito",
                "desc": (
                    "Un jardín histórico de 1859 con estatuas de mármol,"
                    " galería de buganvillas, fuentes y un pequeño laberinto de"
                    " mirto donde apenas llegan los turistas."
                ),
            },
            {
                "name": "Ruta de vermut y clóchinas en las bodegas centenarias de El Cabanyal",
                "location": (
                    "Calle Reina y Calle Barraca (Tranvía: Líneas 4 y 6 -"
                    " Dr. Lluch)"
                ),
                "price": "Vermut + tapa marinera tradicional: 5,50 € – 8,00 €",
                "desc": (
                    "Pasea entre las fachadas modernistas de azulejos de"
                    " colores de los antiguos pescadores del Cabanyal y haz"
                    " parada en Casa Montaña o en las tabernas jóvenes del"
                    " barrio."
                ),
            },
            {
                "name": "Centro de Arte Hortensia Herrero en el Palacio de Valeriola",
                "location": "Calle del Mar, 31 (Barrio de la Seu - Xerea)",
                "price": "Gratis miércoles por la tarde con reserva previa (10 € general)",
                "desc": (
                    "Un palacio del siglo XVII restaurado que combina restos"
                    " del circo romano subterráneo y un callejón judío medieval"
                    " con instalaciones inmersivas de luz."
                ),
            },
        ],
        "affiliate": {
            "partner": "Fever / Civitatis",
            "badge": "Plan Favorito en Valencia",
            "title": (
                "Paseo en Barca al Atardecer en L'Albufera + Conciertos"
                " Candlelight Valencia"
            ),
            "description": (
                "Vive la puesta de sol desde el agua en la Albufera o disfruta"
                " de un concierto a la luz de las velas en el Ateneo Mercantil"
                " de Valencia."
            ),
            "price": "Desde 12 € por persona",
            "ctaText": "Consultar horarios y entradas en Valencia →",
            "commissionNote": (
                "Enlace de afiliado Fever / Civitatis (Comisión del 10% - 12%)"
            ),
        },
    },
    "Sevilla": {
        "image": "/images/sevilla.jpg",
        "neighborhoods": [
            "Triana",
            "Calle Feria",
            "Santa Cruz",
            "Alameda de Hércules",
            "Macarena",
        ],
        "venues": [
            {
                "name": "Casa de Salinas (Patio renacentista y mudéjar del siglo XVI)",
                "location": "Calle Mateos Gago, 39 (A 2 min de la Giralda)",
                "price": "8,00 € entrada guiada",
                "desc": (
                    "Una casa-palacio privada aún habitada que combina columnas"
                    " de mármol italiano, yeserías mudéjares y azulejos de"
                    " Triana de 1580 sin las aglomeraciones del Alcázar."
                ),
            },
            {
                "name": "Mercadillo Histórico de El Jueves y tapeo en la Calle Feria",
                "location": "Calle Feria (Desde Montesión hasta Omnium Sanctorum)",
                "price": "Paseo gratis / Caña y montadito de pringá: 3,80 €",
                "desc": (
                    "El mercadillo al aire libre más antiguo de España (se"
                    " celebra desde el siglo XIII) lleno de antigüedades,"
                    " cerámica, vinilos y libros viejos, rodeado de las mejores"
                    " tabernas locales."
                ),
            },
            {
                "name": "Jardines del Pabellón de la Navegación y ribera de Triana",
                "location": "Camino de los Descubrimientos, 2 (Isla de la Cartuja)",
                "price": "Gratis los martes por la tarde (4,90 € general)",
                "desc": (
                    "Con una torre mirador sobre toda la dársena del río"
                    " Guadalquivir y pasarelas peatonales ideales para enlazar"
                    " con un paseo al atardecer por la calle Betis."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Top Ventas en Sevilla",
            "title": (
                "Free Tour por Triana y Santa Cruz al Atardecer + Tablao"
                " Íntimo"
            ),
            "description": (
                "Descubre los patios ocultos y leyendas de la antigua judería"
                " y la cuna del flamenco en Triana con un guía local sevillano."
            ),
            "price": "Gratis (Propina libre)",
            "ctaText": "Reservar plaza gratis en Sevilla →",
            "commissionNote": (
                "Enlace de afiliado Civitatis (Alta conversión en escapadas a"
                " Sevilla)"
            ),
        },
    },
    "Toledo": {
        "image": "/images/toledo.jpg",
        "neighborhoods": [
            "Judería Mayor",
            "Barrio de los Conventos",
            "Zocodover",
            "Senda Ecológica del Tajo",
        ],
        "venues": [
            {
                "name": "Senda Ecológica del Río Tajo y Puente de San Martín",
                "location": (
                    "Inicio en el Puente de Alcántara hasta el Puente de San"
                    " Martín"
                ),
                "price": "100% Gratis",
                "desc": (
                    "Un camino peatonal junto al cañón de roca del río Tajo que"
                    " rodea toda la muralla medieval desde abajo junto a"
                    " antiguos molinos de agua."
                ),
            },
            {
                "name": "Torno de mazapán artesano del Convento de San Clemente",
                "location": "Calle San Clemente, 1 (Junto a Santo Tomé)",
                "price": "Cajita de mazapán recién horneado desde 4,50 €",
                "desc": (
                    "Entra al patio silencioso del convento donde se elaboró el"
                    " primer mazapán documentado en 1212 y compra a través del"
                    " torno de madera."
                ),
            },
            {
                "name": "Mirador del Cerro del Bú frente al Alcázar",
                "location": "Cruzando la pasarela peatonal del Tajo",
                "price": "Acceso libre y gratuito",
                "desc": (
                    "Un yacimiento arqueológico al aire libre desde el que se"
                    " obtiene la vista más cercana e imponente de las murallas"
                    " de Toledo sin un solo autobús."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Imprescindible en Toledo",
            "title": (
                "Free Tour por el Toledo de las 3 Culturas + Toledo Subterráneo"
            ),
            "description": (
                "Descubre las historias de cristianos, judíos y musulmanes por"
                " las callejuelas laberínticas de Toledo con guía oficial."
            ),
            "price": "Gratis (Reserva online en 1 minuto)",
            "ctaText": "Reservar plaza gratis en Civitatis →",
            "commissionNote": (
                "Enlace de afiliado Civitatis (Altísima conversión en Toledo)"
            ),
        },
    },
}

CATEGORY_ICONS = {
    "Gratis y Baratos": "💸",
    "Planes Diferentes": "✨",
    "En Pareja": "❤️",
}


def slugify(text: str) -> str:
  text = text.lower()
  replacements = {
      "á": "a",
      "é": "e",
      "í": "i",
      "ó": "o",
      "ú": "u",
      "ñ": "n",
      "ü": "u",
  }
  for k, v in replacements.items():
    text = text.replace(k, v)
  text = re.sub(r"[^a-z0-9\s-]", "", text)
  text = re.sub(r"[\s-]+", "-", text).strip("-")
  return text[:68]


def load_json(filepath: str):
  if not os.path.exists(filepath):
    return []
  with open(filepath, "r", encoding="utf-8") as f:
    return json.load(f)


def save_json(filepath: str, data):
  with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
  # También sincronizamos en public/data/ para que el hosting gratuito (Cloudflare/Vercel/GitHub Pages) funcione sin servidor
  public_data_dir = os.path.join(BASE_DIR, "public", "data")
  os.makedirs(public_data_dir, exist_ok=True)
  public_copy = os.path.join(public_data_dir, os.path.basename(filepath))
  with open(public_copy, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def regenerate_sitemap(
    articles: list, base_url: str = "https://hoyqueplan.es"
):
  """Genera automáticamente public/sitemap.xml para las 5 ciudades y todos los artículos."""
  today = date.today().isoformat()
  urls = [
      "  <url>\n"
      f"    <loc>{base_url}/</loc>\n"
      f"    <lastmod>{today}</lastmod>\n"
      "    <changefreq>daily</changefreq>\n"
      "    <priority>1.0</priority>\n"
      "  </url>"
  ]
  for city in ["madrid", "barcelona", "valencia", "sevilla", "toledo"]:
    urls.append(
        "  <url>\n"
        f"    <loc>{base_url}/ciudad/{city}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>0.9</priority>\n"
        "  </url>"
    )
  for art in articles:
    pub = art.get("publishedAt", today)
    slug = art.get("slug", art.get("id"))
    urls.append(
        "  <url>\n"
        f"    <loc>{base_url}/planes/{slug}</loc>\n"
        f"    <lastmod>{pub}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.8</priority>\n"
        "  </url>"
    )
  xml_content = (
      '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "\n".join(urls)
      + "\n</urlset>\n"
  )
  os.makedirs(os.path.dirname(SITEMAP_FILE), exist_ok=True)
  with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(xml_content)


def generate_seo_article(
    city: str,
    category: str,
    keyword: str,
    suggested_title: str = "",
    search_volume: str = "2.100 búsquedas/mes",
    difficulty: str = "Baja (15/100)",
) -> dict:
  city = city if city in CITY_KNOWLEDGE_BASE else "Madrid"
  kb = CITY_KNOWLEDGE_BASE[city]
  cat_icon = CATEGORY_ICONS.get(category, "✨")

  existing_articles = load_json(ARTICLES_FILE)
  related_in_city = [a for a in existing_articles if a.get("city") == city]

  if not suggested_title:
    suggested_title = (
        f"{keyword.capitalize()}: Guía Local de Planes en {city} (2026)"
    )

  slug = slugify(keyword if len(keyword) > 12 else suggested_title)
  today_str = date.today().isoformat()

  sections = []
  for idx, v in enumerate(kb["venues"], start=1):
    sections.append({
        "heading": f"{idx}. {v['name']}",
        "venue": v["name"],
        "location": v["location"],
        "price": v["price"],
        "content": v["desc"],
    })

  if related_in_city:
    first_rel = related_in_city[0]
    sections[-1]["content"] += (
        f" 💡 Consejo extra: Si buscas más ideas en {city}, "
        f'no te pierdas también nuestra guía: «{first_rel["title"]}».'
    )

  price_range = (
      "0 € – 9,00 €"
      if category == "Gratis y Baratos"
      else ("10 € – 25 €" if category == "En Pareja" else "0 € – 15 €")
  )

  new_article = {
      "id": f"{city.lower()}-{slug[:32]}",
      "slug": slug,
      "title": suggested_title,
      "metaTitle": f"{suggested_title[:50]} | HoyQuePlan",
      "metaDescription": (
          f"Descubre los mejores {keyword.lower()} en {city}: direcciones"
          " exactas, paradas de transporte público, precios reales y planes"
          " originales."
      ),
      "city": city,
      "category": category,
      "categoryIcon": cat_icon,
      "readTime": "6 min",
      "publishedAt": today_str,
      "targetKeyword": keyword.lower(),
      "searchVolume": search_volume,
      "keywordDifficulty": difficulty,
      "image": kb["image"],
      "excerpt": (
          f"Seleccionamos los mejores rincones para quienes buscan"
          f" «{keyword.lower()}» en {city} saliendo de lo típico: direcciones"
          f" reales, precios exactos y cómo llegar."
      ),
      "priceRange": price_range,
      "neighborhoods": kb["neighborhoods"][:4],
      "affiliate": kb["affiliate"],
      "generatedByAgent": True,
      "sections": sections,
      "faqs": [
          {
              "question": (
                  f"¿Cuál es el mejor momento para hacer estos planes en"
                  f" {city}?"
              ),
              "answer": (
                  f"Para disfrutar de estos rincones de {city} sin colas ni"
                  " aglomeraciones, te recomendamos ir los viernes por la"
                  " tarde o los sábados antes de las 12:30 h."
              ),
          },
          {
              "question": (
                  f"¿Se necesita reservar con antelación para estos planes en"
                  f" {city}?"
              ),
              "answer": (
                  "Los espacios gratuitos al aire libre no requieren reserva,"
                  " pero para talleres creativos, espectáculos o tours"
                  " nocturnos conviene reservar online entre 48 y 72 horas"
                  " antes."
              ),
          },
      ],
  }

  existing_articles.insert(0, new_article)
  save_json(ARTICLES_FILE, existing_articles)
  regenerate_sitemap(existing_articles)
  return new_article


def run_next_from_queue() -> dict:
  queue = load_json(QUEUE_FILE)
  target_item = None
  for item in queue:
    if item.get("status") == "pending":
      target_item = item
      break

  if not target_item:
    return generate_seo_article(
        city="Valencia",
        category="Gratis y Baratos",
        keyword="planes gratis en valencia este fin de semana",
        suggested_title=(
            "5 Planes Gratis en Valencia para este Fin de Semana (Huerta,"
            " Jardines y Cultura)"
        ),
    )

  article = generate_seo_article(
      city=target_item["city"],
      category=target_item["category"],
      keyword=target_item["keyword"],
      suggested_title=target_item.get("suggestedTitle", ""),
      search_volume=target_item.get("searchVolume", "2.400 búsquedas/mes"),
      difficulty=target_item.get("keywordDifficulty", "Muy Baja (12/100)"),
  )
  target_item["status"] = "published"
  target_item["publishedArticleId"] = article["id"]
  save_json(QUEUE_FILE, queue)
  return article


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Agente SEO Generador de Artículos para HoyQuePlan"
  )
  parser.add_argument(
      "--next",
      action="store_true",
      help="Publica el siguiente artículo programado en la cola",
  )
  parser.add_argument(
      "--city",
      type=str,
      default="Madrid",
      help="Ciudad (Madrid, Barcelona, Valencia, Sevilla, Toledo)",
  )
  parser.add_argument(
      "--category",
      type=str,
      default="Planes Diferentes",
      help="Categoría (Gratis y Baratos, Planes Diferentes, En Pareja)",
  )
  parser.add_argument(
      "--keyword", type=str, default="", help="Palabra clave Long-Tail a atacar"
  )
  parser.add_argument(
      "--title", type=str, default="", help="Título sugerido opcional"
  )
  args = parser.parse_args()

  if args.next or not args.keyword:
    art = run_next_from_queue()
  else:
    art = generate_seo_article(
        city=args.city,
        category=args.category,
        keyword=args.keyword,
        suggested_title=args.title,
    )
  print(f"[OK] Artículo SEO generado y publicado: {art['title']}")
  print(f"     URL Slug: /planes/{art['slug']}")
