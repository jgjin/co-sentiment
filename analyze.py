"""Analyze text of tweets."""

import json

import requests

from auth import get_ibm_syntax_credentials, get_ibm_tone_credentials


def get_sentences(
        text,
):
    """Get sentences from text."""
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "features": {
            "syntax": {
                "sentences": True,
            },
        },
        "language": "en",
    }
    response = requests.post(
        "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12",
        headers=headers,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        auth=requests.auth.HTTPBasicAuth(
            "apikey",
            get_ibm_syntax_credentials(),
        ),
    ).json()

    return list(filter(
        lambda sentence: len(sentence) > 0,
        map(
            lambda sentence: sentence["text"].strip(),
            response["syntax"]["sentences"],
        ),
    ))


def analyze_sentences(
        sentences_chunk,
):
    """Analyze emotional sentiment of sentences."""
    document = "\n".join(sentences_chunk)

    headers = {
        "Content-Type": "text/plain",
    }
    response = requests.post(
        "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2019-06-06",
        headers=headers,
        data=document.encode("utf-8"),
        auth=requests.auth.HTTPBasicAuth(
            "apikey",
            get_ibm_tone_credentials(),
        ),
    )

    return response.json()
