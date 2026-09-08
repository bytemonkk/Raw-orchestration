import requests


response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen3:4b",
        "prompt": "What is 25 * 17?",
        "stream": False,
    },
)

print("STATUS:", response.status_code)
print("HEADERS:", response.headers)
print("RAW RESPONSE:")
print(response.text)