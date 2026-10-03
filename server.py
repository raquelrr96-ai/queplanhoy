#!/usr/bin/env python3
"""Servidor Web y API del Agente SEO para RutaSecreta.es."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
sys.path.insert(0, os.path.join(BASE_DIR, "agent"))

import seo_agent  # noqa: E402


class RutaSecretaHandler(SimpleHTTPRequestHandler):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

  def _send_json(self, payload, status=200):
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Content-Length", str(len(raw)))
    self.end_headers()
    self.wfile.write(raw)

  def do_GET(self):
    if self.path == "/api/articles":
      articles = seo_agent.load_json(seo_agent.ARTICLES_FILE)
      return self._send_json(articles)
    if self.path == "/api/queue":
      queue = seo_agent.load_json(seo_agent.QUEUE_FILE)
      return self._send_json(queue)
    return super().do_GET()

  def do_POST(self):
    if self.path == "/api/agent/run-next":
      article = seo_agent.run_next_from_queue()
      return self._send_json({"ok": True, "article": article})

    if self.path == "/api/agent/generate":
      content_len = int(self.headers.get("Content-Length", 0))
      body_raw = self.rfile.read(content_len).decode("utf-8") if content_len else "{}"
      body = json.loads(body_raw)
      article = seo_agent.generate_seo_article(
          city=body.get("city", "Madrid"),
          category=body.get("category", "Planes Diferentes"),
          keyword=body.get("keyword", "planes originales fin de semana"),
      )
      return self._send_json({"ok": True, "article": article})

    return self._send_json({"error": "Ruta no encontrada"}, status=404)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", "8090"))
  articles = seo_agent.load_json(seo_agent.ARTICLES_FILE)
  seo_agent.regenerate_sitemap(articles)
  server = HTTPServer(("0.0.0.0", port), RutaSecretaHandler)
  print(f"Servidor RutaSecreta.es activo en http://raquelrobles.c.googlers.com:{port}")
  server.serve_forever()
