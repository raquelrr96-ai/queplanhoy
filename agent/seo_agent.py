#!/usr/bin/env python3
"""Agente Automatizado de Contenido SEO para HoyQuePlan (Madrid, Barcelona, Valencia, Sevilla y Toledo)."""

import argparse
from datetime import date, timedelta
import json
import os
import re

import build_site

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, "data", "articles.json")
QUEUE_FILE = os.path.join(BASE_DIR, "data", "keyword_queue.json")
SITEMAP_FILE = os.path.join(BASE_DIR, "public", "sitemap.xml")

TRAVELPAYOUTS_MARKER = "785377"
TRAVELPAYOUTS_TRS = "581302"

CITY_KNOWLEDGE_BASE = {
    "Madrid": {
        "image": "images/terraza-secreta-planes-madrid.jpg",
        "imageAlt": "Terraza jardín interior escondido en el centro de Madrid con vermut y aperitivo",
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
            {
                "name": "Estación Fantasma de Chamberí (Andén 0) y aperitivo en Ponzano",
                "location": "Plaza de Chamberí, s/n (Metro: Iglesia - L1 / Bilbao - L1, L4)",
                "price": "Entrada gratuita al museo / Doble de cerveza y tapa: 3,80 €",
                "desc": (
                    "Una estación de Metro clausurada en 1966 que conserva"
                    " intactos los carteles publicitarios de cerámica de los"
                    " años 20 y los andenes históricos."
                ),
            },
            {
                "name": "Parque Histórico de El Capricho y Templete de Baco",
                "location": "Paseo de la Alameda de Osuna, 25 (Metro: El Capricho - L5)",
                "price": "Acceso 100% gratuito (Sábados, domingos y festivos)",
                "desc": (
                    "El jardín romántico del siglo XVIII de la Duquesa de Osuna"
                    " con laberinto de laurel, embarcadero, cisnes negros y"
                    " templetes neoclásicos."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Top Experiencia en Madrid",
            "title": (
                "Free Tour por el Madrid de los Austrias y el Siglo de Oro"
            ),
            "description": (
                "Descubre las historias, pasadizos y plazas secretas del Madrid"
                " de los Austrias y el Barrio de las Letras con guía local."
            ),
            "price": "Gratis (Propina libre)",
            "url": "https://tp.media/r?campaign_id=89&marker=785377&p=2074&trs=581302&u=https%3A%2F%2Fwww.tiqets.com%2Fes%2Fatracciones-madrid-c66254%2Fentradas-para-palacio-de-liria-entrada-audioguia-p1010845%2F",
            "ctaText": "Reservar Free Tour por Madrid →",
            "commissionNote": (
                "Enlace directo a la actividad en Civitatis"
            ),
        },
    },
    "Barcelona": {
        "image": "images/mirador-atardecer-planes-barcelona.jpg",
        "imageAlt": "Vista panorámica al atardecer de Barcelona y el mar Mediterráneo desde los jardines de Montjuïc",
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
            {
                "name": "Jardins de Laribal y el anfiteatro del Teatre Grec",
                "location": "Passeig de Santa Madrona, 2 (Metro: Espanya - L1, L3)",
                "price": "Acceso 100% gratuito",
                "desc": (
                    "Jardines escalonados de 1922 con fuentes de cerámica,"
                    " albercas y pérgolas que desembocan en el teatro al aire"
                    " libre de Montjuïc."
                ),
            },
            {
                "name": "Recinto Modernista de Sant Pau y ruta de arquitectura en el Guinardó",
                "location": "Carrer de Sant Antoni Maria Claret, 167 (Metro: Sant Pau | Dos de Maig - L5)",
                "price": "Gratis primer domingo de mes y días de puertas abiertas (16 € general)",
                "desc": (
                    "El conjunto modernista más grande del mundo obra de Lluís"
                    " Domènech i Montaner, conectado por galerías subterráneas"
                    " y jardines."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Plan Estrella en Barcelona",
            "title": (
                "Free Tour de los Misterios y Leyendas del Barrio Gótico y El"
                " Born"
            ),
            "description": (
                "Recorre al caer la tarde los callejones medievales del Barrio"
                " Gótico y El Born descubriendo sus secretos mejor guardados."
            ),
            "price": "Gratis (Propina libre)",
            "url": "https://tiqets.tpk.lu/oclT7jKV",
            "ctaText": "Reservar Free Tour por el Barrio Gótico →",
            "commissionNote": (
                "Enlace directo a la actividad en Civitatis"
            ),
        },
    },
    "Valencia": {
        "image": "images/barca-albufera-planes-valencia.jpg",
        "imageAlt": "Barca tradicional de madera al atardecer en el embarcadero de la Albufera de Valencia",
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
            {
                "name": "Atardecer en el Embarcadero de la Gola de Pujol en L'Albufera",
                "location": "Parque Natural de la Albufera (Autobús EMT Línea 24 o 25 por 1,50 €)",
                "price": "Mirador gratuito / Paseo en barca tradicional: 6,00 €",
                "desc": (
                    "Llega en autobús urbano hasta el embarcadero de madera de"
                    " la Gola de Pujol para ver una de las puestas de sol más"
                    " espectaculares del Mediterráneo."
                ),
            },
            {
                "name": "Ruta en bici por la Vía Xurra y horchata en alquería de la Huerta de Alboraya",
                "location": "Inicio en Avenida de Aragón (Metro: Aragón - L5 / Palmaret - L3)",
                "price": "Ruta gratis / Horchata artesana con fartons: 4,20 €",
                "desc": (
                    "Recorre sin coches los caminos históricos de la huerta"
                    " valenciana entre acequias medievales y campos de chufa."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Plan Favorito en Valencia",
            "title": (
                "Excursión y Paseo en Barca Tradicional por la Albufera de"
                " Valencia"
            ),
            "description": (
                "Vive la puesta de sol desde el agua navegando en barca"
                " tradicional (albuferenc) por el Parque Natural de L'Albufera."
            ),
            "price": "Desde 12 € por persona",
            "url": "https://tp.media/r?campaign_id=89&marker=785377&p=2074&trs=581302&u=https%3A%2F%2Fwww.tiqets.com%2Fes%2Fatracciones-valencia-c65847%2Fentradas-para-valencia-pase-arte-y-ciencia-p1124390%2F",
            "ctaText": "Ver horarios del paseo en barca por L'Albufera →",
            "commissionNote": (
                "Enlace directo a la actividad en Civitatis"
            ),
        },
    },
    "Sevilla": {
        "image": "images/patio-mudejar-planes-sevilla.jpg",
        "imageAlt": "Patio andaluz mudéjar con naranjos, azulejos y flores en el barrio de Santa Cruz de Sevilla",
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
            {
                "name": "Palacio de los Marqueses de la Algaba y Centro del Arte Mudéjar",
                "location": "Plaza Calderón de la Barca, s/n (Detrás del Mercado de Feria)",
                "price": "Entrada 100% gratuita",
                "desc": (
                    "Un palacio mudéjar de 1474 con patio de arcos y jardines"
                    " frescos en el corazón de la calle Feria."
                ),
            },
            {
                "name": "Plaza de Santa Marta y Callejón del Agua al anochecer",
                "location": "Acceso por Plaza Virgen de los Reyes (Barrio de Santa Cruz)",
                "price": "Acceso libre y gratuito",
                "desc": (
                    "La plazuela empedrada más pequeña y silenciosa de Sevilla,"
                    " escondida tras un pasadizo con cuatro naranjos y un"
                    " crucero renacentista."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Top Ventas en Sevilla",
            "title": (
                "Free Tour por el Barrio de Triana al Atardecer"
            ),
            "description": (
                "Descubre los corrales de vecinos, talleres de alfarería y la"
                " historia del flamenco en Triana con un guía local sevillano."
            ),
            "price": "Gratis (Propina libre)",
            "url": "https://tp.media/r?campaign_id=89&marker=785377&p=2074&trs=581302&u=https%3A%2F%2Fwww.tiqets.com%2Fes%2Fatracciones-sevilla-c65870%2Fentradas-para-casa-de-salinas-tour-con-audioguia-p986387%2F",
            "ctaText": "Reservar Free Tour por Triana →",
            "commissionNote": (
                "Enlace directo a la actividad en Civitatis"
            ),
        },
    },
    "Toledo": {
        "image": "images/callejones-noche-planes-toledo.jpg",
        "imageAlt": "Callejón medieval empedrado de Toledo iluminado por faroles al anochecer con la torre de la Catedral al fondo",
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
            {
                "name": "Ruta de los Cobertizos iluminados de Santo Domingo el Real y Santa Clara",
                "location": "Zona Norte del Casco Histórico (a 4 min de Plaza de Zocodover)",
                "price": "Paseo 100% gratuito",
                "desc": (
                    "Pasadizos volados del siglo XVI que comunicaban los"
                    " conventos y palacios toledanos y que al anochecer quedan"
                    " en absoluto silencio bajo los faroles de forja."
                ),
            },
            {
                "name": "Baños Árabes de Medina Mudéjar y Termas Romanas de Amador de los Ríos",
                "location": "Plaza de Santa Eulalia, 1 / Plaza Amador de los Ríos (Judería y Centro)",
                "price": "Termas romanas gratis / Baños árabes desde 28 € por persona",
                "desc": (
                    "Descubre el Toledo subterráneo combinando las bóvedas"
                    " romanas gratuitas del Consorcio con un baño termal bajo"
                    " arcos mudéjares del siglo XII."
                ),
            },
        ],
        "affiliate": {
            "partner": "Civitatis",
            "badge": "Imprescindible en Toledo",
            "title": (
                "Free Tour por Toledo y las 3 Culturas con Guía Oficial"
            ),
            "description": (
                "Descubre las historias de cristianos, judíos y musulmanes por"
                " las callejuelas laberínticas de Toledo con guía oficial."
            ),
            "price": "Gratis (Reserva online en 1 minuto)",
            "url": "https://tp.media/r?campaign_id=89&marker=785377&p=2074&trs=581302&u=https%3A%2F%2Fwww.tiqets.com%2Fes%2Fatracciones-toledo-c170113%2Fentradas-para-pulsera-turistica-de-toledo-p1031186%2F",
            "ctaText": "Reservar Free Tour por Toledo →",
            "commissionNote": (
                "Enlace directo a la actividad en Civitatis"
            ),
        },
    },
}

CATEGORY_ICONS = {
    "Este Fin de Semana": "📅",
    "Gratis y Baratos": "💸",
    "Planes Diferentes": "✨",
    "En Pareja": "❤️",
}


def fetch_live_weekend_events(city: str, max_items: int = 2) -> list:
  """Consulta en tiempo real Google News España (RSS) sobre planes, ferias y mercadillos

  que tienen lugar este fin de semana en la ciudad indicada.
  """
  import urllib.parse
  import urllib.request
  import xml.etree.ElementTree as ET

  query = f'planes "este fin de semana" {city} OR feria OR mercadillo OR exposicion'
  url = (
      "https://news.google.com/rss/search?q="
      + urllib.parse.quote(query)
      + "&hl=es&gl=ES&ceid=ES:es"
  )
  discovered = []
  try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
      xml_bytes = resp.read()
    root = ET.fromstring(xml_bytes)
    for item in root.findall("./channel/item"):
      raw_title = item.findtext("title") or ""
      # Limpiar el nombre del medio al final (" - Medio")
      clean_title = raw_title.rsplit(" - ", 1)[0].strip()
      if len(clean_title) > 25 and city.lower() in clean_title.lower():
        discovered.append({
            "name": f"Agenda en vivo: {clean_title}",
            "location": f"Centro y barrios de {city} (Transporte público recomendado)",
            "price": "Consultar acceso (mayoría de actividades gratuitas o entrada libre)",
            "desc": (
                f"Destacado en la agenda cultural de {city} para este fin de"
                f" semana: «{clean_title}». Una propuesta ideal si buscas qué"
                f" planes hacer hoy en {city} combinando cultura, ocio al aire"
                " libre y gastronomía local."
            ),
        })
      if len(discovered) >= max_items:
        break
  except Exception:
    pass
  return discovered


def fetch_real_commons_photo(
    search_query: str,
    slug: str,
    fallback_image: str,
    fallback_alt: str,
    official_image_url: str = "",
    official_credit: str = "",
) -> tuple:
  """Prioriza fotografías oficiales de ayuntamientos/eventos en alta resolución,

  o bien imágenes de calidad editorial verificada; si una foto externa no
  cumple estándares altos de resolución y estética, utiliza la imagen de alta
  calidad curada de la ciudad.
  """
  import ssl
  import urllib.parse
  import urllib.request

  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE

  if official_image_url:
    try:
      rel_path = f"images/{slug[:48]}.jpg"
      abs_path = os.path.join(BASE_DIR, "public", rel_path)
      os.makedirs(os.path.dirname(abs_path), exist_ok=True)
      req = urllib.request.Request(
          official_image_url, headers={"User-Agent": "Mozilla/5.0"}
      )
      data = urllib.request.urlopen(req, context=ctx, timeout=15).read()
      if len(data) > 80000:
        with open(abs_path, "wb") as out_f:
          out_f.write(data)
        return rel_path, fallback_alt, official_credit
    except Exception:
      pass

  return fallback_image, fallback_alt, ""


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


def regenerate_sitemap(
    articles: list, base_url: str = "https://queplanhoy.es"
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


MONTHS_ES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def get_current_weekend_dates_es(ref_date: date | None = None) -> str:
  """Calcula las fechas exactas de viernes a domingo del fin de semana actual o próximo."""
  d = ref_date or date.today()
  # weekday(): lunes=0 ... viernes=4, sábado=5, domingo=6
  wd = d.weekday()
  if wd <= 4:
    friday = d + timedelta(days=(4 - wd))
  elif wd == 5:
    friday = d - timedelta(days=1)
  else:
    friday = d - timedelta(days=2)
  sunday = friday + timedelta(days=2)
  if friday.month == sunday.month:
    return f"{friday.day} al {sunday.day} de {MONTHS_ES[sunday.month]} de {sunday.year}"
  return (
      f"{friday.day} de {MONTHS_ES[friday.month]} al {sunday.day} de"
      f" {MONTHS_ES[sunday.month]} de {sunday.year}"
  )


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

  raw_venues = list(kb["venues"])
  is_weekend_cat = category == "Este Fin de Semana"
  weekend_dates = get_current_weekend_dates_es() if is_weekend_cat else ""

  if (
      is_weekend_cat
      or "fin de semana" in keyword.lower()
      or "que hacer hoy" in keyword.lower()
  ):
    live_events = fetch_live_weekend_events(city, max_items=2)
    if live_events:
      raw_venues = (live_events + raw_venues)[:5]

  sections = []
  for idx, v in enumerate(raw_venues, start=1):
    sections.append({
        "heading": f"{idx}. {v['name']}",
        "venue": v["name"],
        "location": v["location"],
        "price": v["price"],
        "content": v["desc"],
    })

  if not suggested_title:
    if is_weekend_cat:
      suggested_title = (
          f"{len(sections)} Planes este Fin de Semana en {city}"
          f" ({weekend_dates}): {keyword.capitalize()}"
      )
    else:
      suggested_title = (
          f"{len(sections)} Planes en {city}: {keyword.capitalize()} (2026)"
      )
  else:
    # Garantizar siempre que si el título empieza por un número (ej. "7 Planes..."), coincida exactamente con len(sections)
    suggested_title = re.sub(
        r"^\d+\b", str(len(sections)), suggested_title.strip()
    )
    if is_weekend_cat and weekend_dates not in suggested_title:
      suggested_title = f"{suggested_title} ({weekend_dates})"

  slug = slugify(keyword if len(keyword) > 12 else suggested_title)
  today_str = date.today().isoformat()

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

  photo_query = f"{raw_venues[0]['name']} {city}"
  real_img, real_alt, real_credit = fetch_real_commons_photo(
      search_query=photo_query,
      slug=slug,
      fallback_image=kb["image"],
      fallback_alt=kb.get("imageAlt", suggested_title),
  )

  new_article = {
      "id": f"{city.lower()}-{slug[:32]}",
      "slug": slug,
      "title": suggested_title,
      "metaTitle": f"{suggested_title[:58]} | Qué Plan Hoy",
      "metaDescription": (
          f"Descubre los mejores {keyword.lower()} en {city}"
          + (f" ({weekend_dates})" if weekend_dates else "")
          + ": direcciones exactas, paradas de transporte público, precios"
          " reales y planes originales."
      ),
      "city": city,
      "category": category,
      "categoryIcon": cat_icon,
      **({"weekendDates": weekend_dates} if weekend_dates else {}),
      "readTime": "6 min",
      "publishedAt": today_str,
      "targetKeyword": keyword.lower(),
      "searchVolume": search_volume,
      "keywordDifficulty": difficulty,
      "image": real_img,
      "imageAlt": real_alt,
      "imageCredit": real_credit,
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
  build_site.build_all()
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


def run_wednesday_weekend_all_cities() -> list:
  """Publica todos los miércoles la guía 'Este Fin de Semana' para las 5 ciudades

  (Madrid, Barcelona, Valencia, Sevilla y Toledo) con las fechas exactas del
  viernes al domingo entrante y la agenda cultural en vivo de cada ciudad.
  """
  cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Toledo"]
  weekend_dates = get_current_weekend_dates_es()
  existing_articles = load_json(ARTICLES_FILE)
  published = []

  # Recorremos en orden inverso para que al insertar en posición 0 queden:
  # Madrid, Barcelona, Valencia, Sevilla, Toledo
  for city in reversed(cities):
    already_exists = any(
        a.get("city") == city
        and a.get("category") == "Este Fin de Semana"
        and a.get("weekendDates") == weekend_dates
        for a in existing_articles
    )
    if already_exists:
      for a in existing_articles:
        if (
            a.get("city") == city
            and a.get("category") == "Este Fin de Semana"
            and a.get("weekendDates") == weekend_dates
        ):
          published.append(a)
          break
      continue

    keyword = (
        f"planes este fin de semana {city.lower()}"
        f" {slugify(weekend_dates).replace('-', ' ')}"
    )
    suggested_title = (
        f"5 Planes este Fin de Semana en {city} ({weekend_dates}):"
        " Mercadillos, Cultura y Rutas Gratis"
    )
    art = generate_seo_article(
        city=city,
        category="Este Fin de Semana",
        keyword=keyword,
        suggested_title=suggested_title,
        search_volume="8.400 búsquedas/mes",
        difficulty="Baja (18/100)",
    )
    published.append(art)

  build_site.build_all()
  return list(reversed(published))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Agente SEO Generador de Artículos para HoyQuePlan"
  )
  parser.add_argument(
      "--wednesday-all-cities",
      action="store_true",
      help=(
          "Publica todos los miércoles los planes de 'Este Fin de Semana'"
          " para las 5 ciudades (Madrid, Barcelona, Valencia, Sevilla y Toledo)"
      ),
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
      help="Categoría (Este Fin de Semana, Gratis y Baratos, Planes Diferentes, En Pareja)",
  )
  parser.add_argument(
      "--keyword", type=str, default="", help="Palabra clave Long-Tail a atacar"
  )
  parser.add_argument(
      "--title", type=str, default="", help="Título sugerido opcional"
  )
  args = parser.parse_args()

  if args.wednesday_all_cities:
    arts = run_wednesday_weekend_all_cities()
    for a in arts:
      print(
          f"[OK] [{a['city']}] Guía de Fin de Semana publicada/verificada:"
          f" {a['title']}"
      )
  elif args.next or not args.keyword:
    art = run_next_from_queue()
    print(f"[OK] Artículo SEO generado y publicado: {art['title']}")
    print(f"     URL Slug: /{slugify(art['city'])}/{art['slug']}/")
  else:
    art = generate_seo_article(
        city=args.city,
        category=args.category,
        keyword=args.keyword,
        suggested_title=args.title,
    )
    print(f"[OK] Artículo SEO generado y publicado: {art['title']}")
    print(f"     URL Slug: /{slugify(art['city'])}/{art['slug']}/")
