from __future__ import annotations

from pathlib import Path
import ipaddress
import json
import pickle
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pickle"
METADATA_PATH = BASE_DIR / "model_metadata.json"

app = Flask(__name__, template_folder="html", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB request limit

with MODEL_PATH.open("rb") as handle:
    model = pickle.load(handle)

try:
    model_metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    model_metadata = {}


def is_public_http_url(raw_url: str) -> bool:
    """Allow normal public HTTP(S) URLs and reject localhost/private-network targets."""
    try:
        parsed = urlparse(raw_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        host = parsed.hostname.lower()
        if host in {"localhost", "0.0.0.0"} or host.endswith(".local"):
            return False
        for info in socket.getaddrinfo(host, None):
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
        return True
    except (ValueError, socket.gaierror):
        return False


def extract_article_text(url: str) -> tuple[str, str]:
    """Best-effort extraction for public articles using only visible paragraph text."""
    url = (url or "").strip()
    if not is_public_http_url(url):
        raise ValueError("Please enter a valid public http:// or https:// news URL.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
    except requests.RequestException as exc:
        raise ValueError("Could not reach that website. Paste the article text instead.") from exc

    if response.status_code in {401, 402, 403}:
        raise ValueError(
            "This publisher blocks automated access or requires a subscription. "
            "Please paste the article text directly."
        )
    if response.status_code >= 400:
        raise ValueError(
            f"The article could not be downloaded (HTTP {response.status_code}). "
            "Please paste the article text directly."
        )
    if not is_public_http_url(response.url):
        raise ValueError("The URL redirected to a location that cannot be fetched safely.")

    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        raise ValueError("That URL does not appear to be an HTML news article.")

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "form", "aside"]):
        tag.decompose()

    container = soup.find("article") or soup.find("main") or soup.body
    paragraphs = []
    if container:
        for p in container.find_all("p"):
            text = " ".join(p.get_text(" ", strip=True).split())
            if len(text) >= 40:
                paragraphs.append(text)

    article_text = "\n".join(paragraphs)
    if len(article_text) < 250:
        raise ValueError(
            "The website did not expose enough readable article text. "
            "Please paste the article text directly."
        )
    return article_text[:50000], response.url


def classify(text: str) -> tuple[str, float | None]:
    text = " ".join((text or "").split())
    if len(text) < 80:
        raise ValueError("Please provide at least a few sentences of article text for a useful prediction.")
    text = text[:50000]
    prediction = str(model.predict([text])[0]).upper()
    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([text])[0]
        confidence = float(max(probabilities))
    return prediction, confidence


@app.get("/")
def home():
    return render_template("main.html", metadata=model_metadata, active_mode="text")


@app.get("/health")
def health():
    return jsonify(status="ok", service="Fake News Detection")


@app.post("/predict")
def predict():
    try:
        if request.is_json:
            payload = request.get_json(silent=True) or {}
            text = str(payload.get("text") or "").strip()
            url = str(payload.get("url") or payload.get("link") or "").strip()
            mode = "text" if text else "url"
        else:
            mode = request.form.get("mode", "text")
            text = (request.form.get("text") or "").strip()
            url = (request.form.get("url") or "").strip()

        source_url = None
        if mode == "url":
            source_text, source_url = extract_article_text(url)
        else:
            source_text = text

        prediction, confidence = classify(source_text)

        if request.is_json:
            return jsonify(
                prediction=prediction,
                isFake=prediction == "FAKE",
                confidence=round(confidence, 4) if confidence is not None else None,
                source_url=source_url,
            )

        return render_template(
            "main.html",
            metadata=model_metadata,
            prediction=prediction,
            confidence=confidence,
            submitted_text=text,
            submitted_url=url,
            source_url=source_url,
            active_mode=mode,
        )
    except ValueError as exc:
        if request.is_json:
            return jsonify(error=str(exc)), 400
        return render_template(
            "main.html",
            metadata=model_metadata,
            error=str(exc),
            submitted_text=request.form.get("text", ""),
            submitted_url=request.form.get("url", ""),
            active_mode=request.form.get("mode", "text"),
        ), 400
    except Exception:
        if request.is_json:
            return jsonify(error="Unexpected prediction error."), 500
        return render_template(
            "main.html",
            metadata=model_metadata,
            error="Something unexpected happened while analyzing the article. Please try pasted text instead.",
            active_mode=request.form.get("mode", "text"),
        ), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
