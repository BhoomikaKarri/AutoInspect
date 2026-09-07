from remotezip import RemoteZip
import os

URL = "https://huggingface.co/datasets/hoskerelab/bridge-eqa/resolve/main/BridgeEQA_2025.zip"

BRIDGES = [
    "BridgeInspRpt-PUTNEY-00001",
    "BridgeInspRpt-RICHFORD-00003",
    "BridgeInspRpt-GROTON-00036",
    "BridgeInspRpt-DOVER-00028",
    "BridgeInspRpt-MIDDLEBURY-0011A",
]

OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with RemoteZip(URL) as z:
    all_files = z.namelist()

    for bridge in BRIDGES:
        prefix = f"BridgeEQA_2025/{bridge}/"

        matching_files = [
            name for name in all_files
            if name.startswith(prefix)
            and not name.endswith("/")
        ]

        print(f"\n{bridge}")
        print(f"Found {len(matching_files)} files")

        bridge_dir = os.path.join(OUTPUT_DIR, bridge)
        os.makedirs(bridge_dir, exist_ok=True)

        for name in matching_files:
            relative_path = name[len(prefix):]

          
            if relative_path.startswith("."):
                continue

            output_path = os.path.join(bridge_dir, relative_path)

            os.makedirs(
                os.path.dirname(output_path),
                exist_ok=True
            )

            print(f"  Downloading: {relative_path}")

            with z.open(name) as source:
                with open(output_path, "wb") as target:
                    target.write(source.read())

print("\nDone!")
print(f"Files saved in: {OUTPUT_DIR}")