from remotezip import RemoteZip

URL = "https://huggingface.co/datasets/hoskerelab/bridge-eqa/resolve/main/BridgeEQA_2025.zip"

print("Reading ZIP directory remotely...")
print("This should NOT download the full 14.8 GB.\n")

with RemoteZip(URL) as z:
    names = z.namelist()

print(f"Total entries found: {len(names)}\n")

# Show only the first 100 entries
for name in names[:100]:
    print(name)