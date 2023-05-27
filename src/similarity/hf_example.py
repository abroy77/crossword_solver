import json
import requests
import os
import openai
# read api ley from environment

API_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


data = query(
    {
        "inputs": {
            "source_sentence": "That is a happy person",
            "sentences": [
                "That is a happy dog",
                "That is a very happy person",
                "Today is a sunny day"
            ]
        }
    }
)
print(json.dumps(data, indent=2))
