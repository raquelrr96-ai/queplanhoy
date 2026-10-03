# ¿HoyQuéPlan? — Guía de Planes Originales, Gratis y en Pareja

Web editorial automatizada con Agente SEO para **Madrid, Barcelona, Valencia, Sevilla y Toledo**.

- 🌐 **Web en vivo:** [https://raquelrr96-ai.github.io/queplanhoy/](https://raquelrr96-ai.github.io/queplanhoy/)
- 🤖 **Agente SEO Automatizado:** [`agent/seo_agent.py`](agent/seo_agent.py)
- ⏰ **Publicación automática cada 3 días:** [`.github/workflows/publicar_articulo.yml`](.github/workflows/publicar_articulo.yml)

## Cómo funciona la automatización (0 €/mes)
1. Cada 3 días a las 09:00 AM (`cron: '0 7 */3 * *'`), GitHub Actions ejecuta `python3 agent/seo_agent.py --next`.
2. El agente toma la siguiente palabra clave Long-Tail de [`data/keyword_queue.json`](data/keyword_queue.json), redacta la guía con locales reales, paradas de transporte, precios, preguntas frecuentes (`Schema.org FAQPage`) y enlaces de afiliado.
3. Actualiza [`public/sitemap.xml`](public/sitemap.xml) y despliega la web automáticamente en GitHub Pages.
