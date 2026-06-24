import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
FONTS_DIR = ROOT / "static" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

font_mappings = {
    "https://cdn.jsdelivr.net/npm/@fontsource/inter@4.5.0/files/inter-latin-400-normal.woff2": "inter-v12-latin-regular.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/inter@4.5.0/files/inter-latin-500-normal.woff2": "inter-v12-latin-500.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/inter@4.5.0/files/inter-latin-600-normal.woff2": "inter-v12-latin-600.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/inter@4.5.0/files/inter-latin-700-normal.woff2": "inter-v12-latin-700.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/inter@4.5.0/files/inter-latin-800-normal.woff2": "inter-v12-latin-800.woff2",
    
    "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc@4.5.0/files/noto-sans-sc-chinese-simplified-400-normal.woff2": "noto-sans-sc-v26-chinese-simplified-regular.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc@4.5.0/files/noto-sans-sc-chinese-simplified-500-normal.woff2": "noto-sans-sc-v26-chinese-simplified-500.woff2",
    "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc@4.5.0/files/noto-sans-sc-chinese-simplified-700-normal.woff2": "noto-sans-sc-v26-chinese-simplified-700.woff2",
}

def download_with_retry(url, local_path, max_retries=5, delay=1.5):
    for attempt in range(1, max_retries + 1):
        # Use curl.exe with a timeout of 10s for connection
        result = subprocess.run(
            ["curl.exe", "-L", "-s", "-f", "--connect-timeout", "10", "-o", str(local_path), url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 0:
            return True, local_path.stat().st_size
        
        print(f"  [RETRY {attempt}/{max_retries}] Failed to download (curl code: {result.returncode}). Retrying in {delay}s...")
        if local_path.exists():
            try:
                local_path.unlink() # remove partial/failed download
            except:
                pass
        time.sleep(delay)
    return False, 0

def main():
    print("Starting download of woff2 fonts from jsDelivr CDN using curl with retries...")
    
    success_count = 0
    for url, filename in font_mappings.items():
        local_path = FONTS_DIR / filename
        
        # Check if already exists and is non-empty
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"{filename} already exists ({local_path.stat().st_size} bytes). Skipping.")
            success_count += 1
            continue
            
        print(f"Downloading {filename}...")
        success, size = download_with_retry(url, local_path)
        if success:
            print(f"  [OK] Saved to {filename} ({size} bytes)")
            success_count += 1
        else:
            print(f"  [ERROR] Permanently failed to download {filename} after all attempts.")
            
    print(f"\nDownload completed: {success_count}/{len(font_mappings)} successful.")

if __name__ == "__main__":
    main()
