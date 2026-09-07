from huggingface_hub import hf_hub_url
import requests

REPO_ID = "hoskerelab/bridge-eqa"
FILENAME = "BridgeEQA_2025.zip"

url = hf_hub_url(
    repo_id=REPO_ID,
    filename=FILENAME,
    repo_type="dataset"
)

print("Checking remote ZIP...")
print(url)

response = requests.head(url, allow_redirects=True)

print("\nHTTP status:", response.status_code)
print("File size:", response.headers.get("Content-Length"))
print("Accept-Ranges:", response.headers.get("Accept-Ranges"))