#!/usr/bin/env python3
"""Generador de Pines verticales (1000x1500 px, 2:3) para Pinterest SEO y Kit de Publicación.

Usa fotografías reales verificadas de `public/images/venues/` y aplica una maquetación
editorial limpia con tipografía Serif/Sans de alto contraste mediante ImageMagick + SVG.
Además, genera `/pinterest-kit/index.html` con botones de descarga y copiado en 1 clic.
"""

import html
from pathlib import Path
import subprocess
import tempfile
import textwrap

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
PINS_DIR = PUBLIC_DIR / "images" / "pinterest"
KIT_DIR = PUBLIC_DIR / "pinterest-kit"

PINS_DATA = [
    {
        "id": "pin-01-madrid-puente-octubre",
        "source_image": "images/venues/madrid-campo-del-moro-portada.jpg",
        "city_badge": "MADRID · PUENTE DE OCTUBRE",
        "accent_hex": "#c84b31",
        "headline": "5 Planes para el Puente de Octubre en Madrid",
        "subheadline": "Museos gratis el 12 de octubre, Campo del Moro en otoño y Mercado de Motores",
        "footer_tag": "GUÍA PASO A PASO + MAPA · QUEPLANHOY.ES",
        "board": "Planes en Madrid | Escapadas, Rutas y Rincones Secretos",
        "pin_title": "5 Planes para el Puente de Octubre en Madrid (10 al 12 Octubre): Museos Gratis y Otoño",
        "pin_description": (
            "¿Te quedas en Madrid este Puente del Pilar (10 al 12 de octubre)? Descubre 5 planes "
            "diferentes sin salir de la ciudad: museos estatales gratis por el 12 de octubre "
            "(Museo Arqueológico Nacional y Cerralbo), paseo otoñal por los jardines históricos "
            "del Campo del Moro, el Real Jardín Botánico en octubre, el Mercado de Motores en el "
            "Museo del Ferrocarril y ruta de vermut por el Barrio de las Letras. Incluye horarios, "
            "precios y mapa en Google Maps. #planesmadrid #puentedeoctubre #madridgratis #otoñoenmadrid"
        ),
        "alt_text": "Vista otoñal de los jardines del Campo del Moro con el Palacio Real de Madrid al fondo",
        "url": "https://queplanhoy.es/madrid/planes-puente-octubre-madrid-12-octubre-gratis/",
    },
    {
        "id": "pin-02-toledo-todos-los-santos-halloween",
        "source_image": "images/venues/tol-puente-san-martin-niebla.jpg",
        "city_badge": "TOLEDO · PUENTE DE NOVIEMBRE",
        "accent_hex": "#b45309",
        "headline": "Toledo en Todos los Santos y Halloween",
        "subheadline": "Subterráneos romanos, leyendas de Bécquer en el Pozo Amargo y mazapán de convento",
        "footer_tag": "RUTA NOCTURNA + MAPA · QUEPLANHOY.ES",
        "board": "Toledo Secreto | Escapadas a 30 Min de Madrid",
        "pin_title": "5 Planes en Toledo para el Puente de Todos los Santos y Halloween: Subterráneos y Leyendas",
        "pin_description": (
            "Escapada de otoño a Toledo para el Puente de Todos los Santos (1 de noviembre) y la "
            "noche de Halloween: baja gratis a las Cuevas de Hércules romanas, recorre los "
            "callejones de las leyendas de Gustavo Adolfo Bécquer (Pozo Amargo y Cobertizo de "
            "Santa Clara), visita las momias de la Iglesia de San Andrés y prueba los huesos de "
            "santo y el mazapán artesano en obradores históricos. Con mapa interactivo. "
            "#toledo #puentedetodoslossantos #halloweentoledo #escapadasdesdemadrid"
        ),
        "alt_text": "Puente medieval de San Martín en Toledo iluminado de noche entre la niebla",
        "url": "https://queplanhoy.es/toledo/planes-puente-todos-los-santos-halloween-toledo-leyendas-noche/",
    },
    {
        "id": "pin-03-madrid-planes-lluvia",
        "source_image": "images/venues/madrid-lluvia-gran-via.jpg",
        "city_badge": "MADRID · DÍAS DE LLUVIA",
        "accent_hex": "#2563eb",
        "headline": "5 Planes en Madrid Cuando Llueve",
        "subheadline": "Invernaderos tropicales, salones palaciegos, cine art déco y cafés con encanto",
        "footer_tag": "100% A CUBIERTO · QUEPLANHOY.ES",
        "board": "Planes en Madrid | Escapadas, Rutas y Rincones Secretos",
        "pin_title": "5 Planes en Madrid Cuando Llueve (100% a Cubierto): Invernaderos, Palacios y Cafés",
        "pin_description": (
            "¿Llueve hoy en Madrid y no sabes qué hacer? Guarda esta guía con 5 refugios "
            "perfectos a cubierto: la Estufa de las Palmas del Real Jardín Botánico, el Museo "
            "del Romanticismo y su Salón de Té secreto, el Palacio de Liria, sesión de tarde en "
            "el Cine Doré (Filmoteca Española) y el Museo Cerralbo. Todos con parada exacta en "
            "Google Maps. #madridconlluvia #planesmadrid #quehacerenmadrid #madridsecreto"
        ),
        "alt_text": "Gran Vía de Madrid bajo la lluvia con reflejos sobre el asfalto mojado",
        "url": "https://queplanhoy.es/madrid/planes-en-madrid-cuando-llueve-cubiertos-originales/",
    },
    {
        "id": "pin-04-madrid-parque-capricho",
        "source_image": "images/venues/madrid-parque-capricho.jpg",
        "city_badge": "MADRID · JARDÍN SECRETO GRATIS",
        "accent_hex": "#15803d",
        "headline": "Visitar el Parque de El Capricho",
        "subheadline": "El jardín romántico del siglo XVIII que solo abre sábados, domingos y festivos",
        "footer_tag": "ENTRADA GRATUITA · QUEPLANHOY.ES",
        "board": "Planes en Madrid | Escapadas, Rutas y Rincones Secretos",
        "pin_title": "Guía para Visitar el Parque de El Capricho en Madrid: Ruta, Horarios y Rincones",
        "pin_description": (
            "El Parque de El Capricho en Alameda de Osuna es uno de los jardines históricos más "
            "bonitos y desconocidos de Madrid. Descubre el itinerario completo paso a paso: "
            "Templete de Baco, Laberinto de Laurel, Casino de Baile, Casa de la Vieja y cómo "
            "visitar su búnker de la Guerra Civil. Entrada gratuita los fines de semana. "
            "#parquedeelcapricho #madridgratis #rinconessecretosmadrid #planesmadrid"
        ),
        "alt_text": "Templete de Baco y jardines románticos del Parque de El Capricho en Madrid",
        "url": "https://queplanhoy.es/madrid/visitar-parque-el-capricho-madrid-guia-completa-gratis/",
    },
    {
        "id": "pin-05-madrid-citas-originales",
        "source_image": "images/venues/madrid-salon-concierto-palacio.jpg",
        "city_badge": "MADRID · CITAS EN PAREJA",
        "accent_hex": "#be185d",
        "headline": "5 Citas Originales en Madrid",
        "subheadline": "Planes en pareja para huir de la típica cena: jardines ocultos, museos y miradores",
        "footer_tag": "PLANES ROMÁNTICOS · QUEPLANHOY.ES",
        "board": "Citas Originales y Planes en Pareja (España)",
        "pin_title": "5 Citas Originales en Madrid para Sorprender a tu Pareja (Más Allá de la Típica Cena)",
        "pin_description": (
            "¿Buscas ideas de citas diferentes en Madrid? Sorprende con estos 5 planes románticos "
            "con encanto: paseo por el Parque de El Capricho, tarde en el Museo Sorolla y su "
            "jardín andaluz, película clásica por 3€ en el Cine Doré, atardecer en el Jardín de "
            "las Vistillas y merienda escondida en el Jardín del Príncipe de Anglona. "
            "#citasenmadrid #planesenpareja #madridromantico #planesoriginales"
        ),
        "alt_text": "Salón palaciego iluminado para una cita cultural diferente en Madrid",
        "url": "https://queplanhoy.es/madrid/citas-originales-madrid-pareja-ceramica-vino/",
    },
    {
        "id": "pin-06-barcelona-laberint-horta",
        "source_image": "images/venues/bcn-laberint-horta.jpg",
        "city_badge": "BARCELONA · RINCÓN SECRETO",
        "accent_hex": "#15803d",
        "headline": "Parc del Laberint d'Horta en Barcelona",
        "subheadline": "El jardín museo más antiguo de la ciudad: laberinto de cipreses, cascadas y pabellones",
        "footer_tag": "GUÍA COMPLETA · QUEPLANHOY.ES",
        "board": "Barcelona Secreta | Planes, Miradores y Rutas Locales",
        "pin_title": "Cómo Visitar el Parc del Laberint d'Horta en Barcelona: Días Gratis, Horarios y Ruta",
        "pin_description": (
            "Escapa de las multitudes en el Parc del Laberint d'Horta, el jardín neoclásico y "
            "romántico del siglo XVIII escondido a los pies de Collserola. Te contamos qué días "
            "es gratis, cómo llegar en Metro L3 (Mundet) y qué rincones no perderte: el laberinto "
            "vegetal, el Pabellón de Carlos IV y la cascada romántica. #barcelonasecreta "
            "#planesbarcelona #laberintdhorta #rinconesbarcelona"
        ),
        "alt_text": "Laberinto de cipreses y estanque neoclásico del Parc del Laberint d'Horta en Barcelona",
        "url": "https://queplanhoy.es/barcelona/visitar-laberinto-de-horta-barcelona-guia-completa-gratis/",
    },
    {
        "id": "pin-07-barcelona-miradores-gratis",
        "source_image": "images/venues/bcn-teatre-grec-laribal.jpg",
        "city_badge": "BARCELONA · MIRADORES GRATIS",
        "accent_hex": "#c84b31",
        "headline": "Miradores Alternativos en Barcelona",
        "subheadline": "Jardines de Laribal, Teatre Grec, Turó del Putxet y vistas panorámicas gratis",
        "footer_tag": "100% GRATIS + MAPA · QUEPLANHOY.ES",
        "board": "Barcelona Secreta | Planes, Miradores y Rutas Locales",
        "pin_title": "5 Miradores Alternativos y Planes Gratis en Barcelona (Sin Masificaciones)",
        "pin_description": (
            "Disfruta de las mejores vistas y jardines de Barcelona sin aglomeraciones ni gastar "
            "nada: los Jardines de Laribal y el Teatre Grec en Montjuïc, el mirador del Turó del "
            "Putxet, el Parque del Guinardó y terrazas panorámicas gratuitas. Con ubicaciones en "
            "Google Maps. #barcelonagratis #planesbarcelona #miradoresbarcelona #quehacerenbarcelona"
        ),
        "alt_text": "Jardines y pérgola de Montjuïc junto al Teatre Grec en Barcelona",
        "url": "https://queplanhoy.es/barcelona/miradores-alternativos-barcelona-planes-gratis/",
    },
    {
        "id": "pin-08-valencia-albufera-atardecer",
        "source_image": "images/venues/vlc-albufera-atardecer-dorado.jpg",
        "city_badge": "VALENCIA · ESCAPADA EN BUS",
        "accent_hex": "#d97706",
        "headline": "Cómo Ir a la Albufera de Valencia",
        "subheadline": "En el autobús EMT 25 por 2€, paseo en barca desde El Palmar y Gola de Pujol",
        "footer_tag": "EL MEJOR ATARDECER · QUEPLANHOY.ES",
        "board": "Planes en Valencia y Sevilla | Escapadas con Encanto",
        "pin_title": "Cómo Ir a la Albufera de Valencia sin Coche: Bus 25, Paseo en Barca al Atardecer y El Palmar",
        "pin_description": (
            "El mejor atardecer de Valencia está a solo 35 minutos del centro en el autobús EMT 25. "
            "Guía práctica para pasar la tarde en el Parque Natural de la Albufera: parada en el "
            "Mirador de la Gola de Pujol, paseo por la Devesa del Saler y recorrido en barca "
            "tradicional (albuferenc) desde los embarcaderos de El Palmar. #valencia #albuferadevalencia "
            "#planesvalencia #atardecervalencia"
        ),
        "alt_text": "Embarcadero de madera en la Albufera de Valencia al atardecer dorado",
        "url": "https://queplanhoy.es/valencia/como-ir-a-la-albufera-valencia-autobus-el-palmar-atardecer/",
    },
    {
        "id": "pin-09-sevilla-patios-secretos",
        "source_image": "images/venues/sev-patio-santa-cruz.jpg",
        "city_badge": "SEVILLA · PLANES EN PAREJA",
        "accent_hex": "#c84b31",
        "headline": "5 Planes en Sevilla en Pareja",
        "subheadline": "Casas-palacio mudéjares, callejones de Santa Cruz y paseo al atardecer junto al río",
        "footer_tag": "RUTA CON MAPA · QUEPLANHOY.ES",
        "board": "Planes en Valencia y Sevilla | Escapadas con Encanto",
        "pin_title": "5 Planes Románticos en Sevilla en Pareja: Casas-Palacio, Jardines y Atardecer",
        "pin_description": (
            "Descubre la Sevilla más íntima y señorial: el patio mudéjar y jardines de la Casa de "
            "Pilatos, el Palacio de las Dueñas en flor, el Callejón del Agua en el Barrio de Santa "
            "Cruz, el Parque de María Luisa y el atardecer cruzando el Puente de Triana. "
            "#sevillaromantica #planessevilla #casadepilatos #quehacerensevilla"
        ),
        "alt_text": "Patio sevillano con fuentes y azulejos en el Barrio de Santa Cruz de Sevilla",
        "url": "https://queplanhoy.es/sevilla/planes-en-sevilla-en-pareja-diferentes-baratos/",
    },
    {
        "id": "pin-10-toledo-senda-ecologica-tajo",
        "source_image": "images/venues/tol-puente-alcantara.jpg",
        "city_badge": "TOLEDO · RUTA A PIE GRATIS",
        "accent_hex": "#15803d",
        "headline": "La Senda Ecológica del Río Tajo en Toledo",
        "subheadline": "Ruta fácil de 5 km entre el Puente de Alcántara y el Puente de San Martín",
        "footer_tag": "RUTA PASO A PASO · QUEPLANHOY.ES",
        "board": "Toledo Secreto | Escapadas a 30 Min de Madrid",
        "pin_title": "Ruta por la Senda Ecológica del Tajo en Toledo: 5 km entre Puentes Medievales y Miradores",
        "pin_description": (
            "La forma más bonita y tranquila de rodear el casco histórico de Toledo a pie: la Senda "
            "Ecológica del Tajo une el Puente de Alcántara con el Puente de San Martín bordeando el "
            "cañón granítico del río. Incluye paso en barca gratuito del Pasaje de Safont, molinos "
            "históricos y el Cerro del Bú. #toledo #sendadelTajo #rutastoledo #escapadasmadrid"
        ),
        "alt_text": "Puente medieval de Alcántara sobre el río Tajo con el Alcázar de Toledo al fondo",
        "url": "https://queplanhoy.es/toledo/senda-ecologica-del-tajo-toledo-ruta-a-pie-gratis/",
    },
]


def build_svg_overlay(pin_info):
    head_lines = textwrap.wrap(pin_info["headline"], width=22)
    sub_lines = textwrap.wrap(pin_info["subheadline"], width=42)

    footer_y = 1412
    div_y = footer_y - 38

    sub_line_h = 44
    sub_start_y = div_y - 26 - (len(sub_lines) - 1) * sub_line_h

    head_line_h = 74
    head_start_y = sub_start_y - 58 - (len(head_lines) - 1) * head_line_h

    badge_text = html.escape(pin_info["city_badge"])
    pill_w = max(500, int(len(pin_info["city_badge"]) * 25) + 130)
    pill_x = (1000 - pill_w) // 2

    head_svg_elems = []
    for i, line in enumerate(head_lines):
        y = head_start_y + i * head_line_h
        esc = html.escape(line)
        head_svg_elems.append(
            f'<text x="503" y="{y+4}" text-anchor="middle" font-family="Liberation Serif, DejaVu Serif, serif" '
            f'font-weight="bold" font-size="64" fill="#000000" fill-opacity="0.75">{esc}</text>'
        )
        head_svg_elems.append(
            f'<text x="500" y="{y}" text-anchor="middle" font-family="Liberation Serif, DejaVu Serif, serif" '
            f'font-weight="bold" font-size="64" fill="#ffffff">{esc}</text>'
        )

    sub_svg_elems = []
    for i, line in enumerate(sub_lines):
        y = sub_start_y + i * sub_line_h
        esc = html.escape(line)
        sub_svg_elems.append(
            f'<text x="502" y="{y+2}" text-anchor="middle" font-family="Roboto, Liberation Sans, sans-serif" '
            f'font-weight="500" font-size="31" fill="#000000" fill-opacity="0.65">{esc}</text>'
        )
        sub_svg_elems.append(
            f'<text x="500" y="{y}" text-anchor="middle" font-family="Roboto, Liberation Sans, sans-serif" '
            f'font-weight="500" font-size="31" fill="#f3f4f6">{esc}</text>'
        )

    footer_esc = html.escape(pin_info["footer_tag"])
    accent = pin_info["accent_hex"]

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
  <!-- Subtle inset frame -->
  <rect x="34" y="34" width="932" height="1432" rx="22" ry="22" fill="none" stroke="#ffffff" stroke-opacity="0.42" stroke-width="2.5"/>

  <!-- Top Category Pill -->
  <rect x="{pill_x}" y="72" width="{pill_w}" height="58" rx="29" ry="29" fill="{accent}"/>
  <text x="500" y="110" text-anchor="middle" font-family="Roboto, Liberation Sans, sans-serif" font-weight="bold" font-size="23" letter-spacing="1.5" fill="#ffffff">{badge_text}</text>

  <!-- Headline -->
  {"".join(head_svg_elems)}

  <!-- Subheadline -->
  {"".join(sub_svg_elems)}

  <!-- Accent divider -->
  <line x1="410" y1="{div_y}" x2="590" y2="{div_y}" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>

  <!-- Footer -->
  <text x="500" y="{footer_y}" text-anchor="middle" font-family="Roboto, Liberation Sans, sans-serif" font-weight="bold" font-size="22" letter-spacing="2.5" fill="#f8d49b">{footer_esc}</text>
</svg>
"""


def create_pin_image(pin_info):
    PINS_DIR.mkdir(parents=True, exist_ok=True)
    src_path = PUBLIC_DIR / pin_info["source_image"]
    out_path = PINS_DIR / f"{pin_info['id']}.jpg"

    svg_content = build_svg_overlay(pin_info)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as tmp_svg:
        tmp_svg.write(svg_content)
        tmp_svg_path = tmp_svg.name

    try:
        cmd = [
            "/usr/bin/magick",
            str(src_path),
            "-resize",
            "1000x1500^",
            "-gravity",
            "center",
            "-extent",
            "1000x1500",
            "-modulate",
            "102,108,100",
            # Smooth top vignette gradient
            "(",
            "-size",
            "1000x300",
            "gradient:rgba(11,15,23,0.72)-rgba(11,15,23,0.0)",
            ")",
            "-gravity",
            "north",
            "-composite",
            # Smooth bottom editorial gradient
            "(",
            "-size",
            "1000x820",
            "gradient:rgba(11,15,23,0.0)-rgba(11,15,23,0.94)",
            ")",
            "-gravity",
            "south",
            "-composite",
            # Reset -size and composite crisp 1000x1500 SVG typography & badge overlay
            "+size",
            "(",
            "-background",
            "none",
            tmp_svg_path,
            ")",
            "-gravity",
            "north",
            "-composite",
            "-quality",
            "90",
            str(out_path),
        ]
        subprocess.run(cmd, check=True)
    finally:
        Path(tmp_svg_path).unlink(missing_ok=True)

    return out_path


def generate_kit_html():
    KIT_DIR.mkdir(parents=True, exist_ok=True)
    cards_html = []
    for idx, pin in enumerate(PINS_DATA, start=1):
        img_url = f"/images/pinterest/{pin['id']}.jpg"
        title_esc = html.escape(pin["pin_title"])
        desc_esc = html.escape(pin["pin_description"])
        board_esc = html.escape(pin["board"])
        alt_esc = html.escape(pin["alt_text"])
        url_esc = html.escape(pin["url"])

        cards_html.append(f"""
        <article class="pin-card">
          <div class="pin-preview">
            <span class="pin-num">Pin #{idx:02d} · 1000×1500 px (2:3)</span>
            <img src="{img_url}" alt="{alt_esc}" loading="lazy" width="1000" height="1500">
            <a class="download-btn" href="{img_url}" download="{pin['id']}.jpg">⬇ Descargar Imagen Vertical (.JPG)</a>
          </div>
          <div class="pin-meta">
            <div class="field-group">
              <div class="field-header">
                <label>1. Tablero de Pinterest recomendado</label>
                <button type="button" class="copy-btn" data-copy="{board_esc}">Copiar tablero</button>
              </div>
              <div class="field-box board-box">{board_esc}</div>
            </div>

            <div class="field-group">
              <div class="field-header">
                <label>2. Título SEO del Pin (máx. 100 caracteres)</label>
                <button type="button" class="copy-btn" data-copy="{title_esc}">Copiar título</button>
              </div>
              <div class="field-box title-box">{title_esc}</div>
            </div>

            <div class="field-group">
              <div class="field-header">
                <label>3. Descripción SEO + Keywords + Hashtags</label>
                <button type="button" class="copy-btn" data-copy="{desc_esc}">Copiar descripción</button>
              </div>
              <div class="field-box desc-box">{desc_esc}</div>
            </div>

            <div class="field-group">
              <div class="field-header">
                <label>4. Enlace de destino directo (URL canónica)</label>
                <button type="button" class="copy-btn" data-copy="{url_esc}">Copiar URL</button>
              </div>
              <div class="field-box url-box"><a href="{url_esc}" target="_blank" rel="noopener">{url_esc}</a></div>
            </div>

            <div class="field-group">
              <div class="field-header">
                <label>5. Texto Alternativo (Alt Text para accesibilidad SEO)</label>
                <button type="button" class="copy-btn" data-copy="{alt_esc}">Copiar Alt Text</button>
              </div>
              <div class="field-box">{alt_esc}</div>
            </div>
          </div>
        </article>
        """)

    page_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Kit de Publicación en Pinterest · ¿Qué Plan Hoy?</title>
  <link rel="stylesheet" href="/css/styles.css">
  <style>
    .kit-container {{ max-width: 1120px; margin: 2.5rem auto 4rem; padding: 0 1.25rem; }}
    .kit-hero {{ background: #fff; border: 1px solid #e6e1d6; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,0.04); }}
    .kit-hero h1 {{ font-size: 2rem; margin: 0 0 0.6rem; color: #1b1f24; }}
    .kit-hero p {{ margin: 0.4rem 0; color: #4b5563; line-height: 1.6; }}
    .boards-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-top: 1.25rem; }}
    .board-pill {{ background: #faf7f2; border: 1px solid #e6e1d6; border-radius: 10px; padding: 0.9rem 1rem; }}
    .board-pill strong {{ display: block; color: #c84b31; font-size: 0.95rem; margin-bottom: 0.3rem; }}
    .board-pill span {{ font-size: 0.85rem; color: #555; }}
    .pin-card {{ display: grid; grid-template-columns: 320px 1fr; gap: 2rem; background: #fff; border: 1px solid #e6e1d6; border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 8px 24px rgba(0,0,0,0.05); align-items: start; }}
    @media (max-width: 820px) {{ .pin-card {{ grid-template-columns: 1fr; }} }}
    .pin-preview {{ display: flex; flex-direction: column; gap: 0.75rem; }}
    .pin-num {{ font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #c84b31; }}
    .pin-preview img {{ width: 100%; height: auto; border-radius: 12px; border: 1px solid #e5e7eb; display: block; }}
    .download-btn {{ display: inline-block; text-align: center; background: #c84b31; color: #fff !important; font-weight: 700; padding: 0.75rem 1rem; border-radius: 10px; text-decoration: none; font-size: 0.92rem; transition: opacity 0.15s; }}
    .download-btn:hover {{ opacity: 0.92; }}
    .pin-meta {{ display: flex; flex-direction: column; gap: 1rem; }}
    .field-group {{ display: flex; flex-direction: column; gap: 0.35rem; }}
    .field-header {{ display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; }}
    .field-header label {{ font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #6b7280; }}
    .copy-btn {{ background: #1f2937; color: #fff; border: none; border-radius: 6px; padding: 0.35rem 0.7rem; font-size: 0.78rem; font-weight: 600; cursor: pointer; }}
    .copy-btn.copied {{ background: #15803d; }}
    .field-box {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.75rem 0.9rem; font-size: 0.93rem; line-height: 1.55; color: #1f2937; word-break: break-word; }}
    .board-box {{ font-weight: 700; color: #c84b31; background: #fff8f5; border-color: #f3d2c9; }}
    .title-box {{ font-weight: 700; font-size: 1rem; }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">¿Qué Plan <span>Hoy</span>?</a>
      <nav class="main-nav">
        <a href="/madrid/">Madrid</a>
        <a href="/barcelona/">Barcelona</a>
        <a href="/valencia/">Valencia</a>
        <a href="/sevilla/">Sevilla</a>
        <a href="/toledo/">Toledo</a>
        <a href="/mapa/">🗺️ Mapa</a>
      </nav>
    </div>
  </header>

  <main class="kit-container">
    <section class="kit-hero">
      <h1>📌 Kit de Pinterest SEO · ¿Qué Plan Hoy?</h1>
      <p>Aquí tienes tus <strong>10 primeros Pines verticales (1000×1500 px, formato 2:3 oficial de Pinterest)</strong> generados con las fotografías reales verificadas de cada lugar, listos para descargar y publicar en menos de 1 minuto por Pin.</p>
      <div class="boards-grid">
        <div class="board-pill">
          <strong>Tablero 1 · Madrid</strong>
          <span>Planes en Madrid | Escapadas, Rutas y Rincones Secretos</span>
        </div>
        <div class="board-pill">
          <strong>Tablero 2 · Toledo</strong>
          <span>Toledo Secreto | Escapadas a 30 Min de Madrid</span>
        </div>
        <div class="board-pill">
          <strong>Tablero 3 · Barcelona</strong>
          <span>Barcelona Secreta | Planes, Miradores y Rutas Locales</span>
        </div>
        <div class="board-pill">
          <strong>Tablero 4 · Citas en Pareja</strong>
          <span>Citas Originales y Planes en Pareja (España)</span>
        </div>
        <div class="board-pill">
          <strong>Tablero 5 · Valencia y Sevilla</strong>
          <span>Planes en Valencia y Sevilla | Escapadas con Encanto</span>
        </div>
      </div>
    </section>

    {"".join(cards_html)}
  </main>

  <script>
    document.querySelectorAll('.copy-btn').forEach(btn => {{
      btn.addEventListener('click', async () => {{
        const text = btn.getAttribute('data-copy');
        try {{
          await navigator.clipboard.writeText(text);
          const orig = btn.textContent;
          btn.textContent = '✓ Copiado';
          btn.classList.add('copied');
          setTimeout(() => {{
            btn.textContent = orig;
            btn.classList.remove('copied');
          }}, 1800);
        }} catch (e) {{
          alert('Texto copiado');
        }}
      }});
    }});
  </script>
</body>
</html>
"""
    (KIT_DIR / "index.html").write_text(page_html, encoding="utf-8")


def main():
    for pin in PINS_DATA:
        out = create_pin_image(pin)
        print(f"Generado: {out.relative_to(BASE_DIR)}")
    generate_kit_html()
    print("Generado: public/pinterest-kit/index.html")


if __name__ == "__main__":
    main()
