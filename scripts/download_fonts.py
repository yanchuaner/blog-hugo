import os
import urllib.request
import re
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
FONTS_DIR = ROOT / "static" / "fonts"
CSS_OUT_DIR = ROOT / "assets" / "css" / "extended"

# Ensure directories exist
FONTS_DIR.mkdir(parents=True, exist_ok=True)
CSS_OUT_DIR.mkdir(parents=True, exist_ok=True)

# Google Fonts URL
URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap"

# Modern User-Agent to ensure Google Fonts returns woff2 files
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
}

def main():
    print("Fetching stylesheet from Google Fonts...")
    req = urllib.request.Request(URL, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            css_content = response.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching Google Fonts stylesheet: {e}")
        return

    # Find all font URLs
    urls = re.findall(r'url\((https://[^\)]+\.woff2)\)', css_content)
    print(f"Found {len(urls)} woff2 font files to download.")

    # Dictionary to map remote URLs to local paths
    url_map = {}

    for i, font_url in enumerate(urls, 1):
        filename = font_url.split("/")[-1]
        local_path = FONTS_DIR / filename
        
        print(f"[{i}/{len(urls)}] Downloading {filename}...")
        
        # Download the file
        try:
            # We can download via urllib
            urllib.request.urlretrieve(font_url, str(local_path))
            url_map[font_url] = f"/fonts/{filename}"
            print("  Done.")
        except Exception as e:
            print(f"  Error downloading {filename}: {e}")
            return

    # Replace remote URLs with local URLs in the CSS content
    local_css_content = css_content
    for remote, local in url_map.items():
        local_css_content = local_css_content.replace(remote, local)

    # Add global body and code styling declarations to the CSS as well
    # so they are bundled into the main CSS and not inlined in extend_head.html
    style_suffix = """
body { font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif; }
code, pre, kbd, samp { font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace; }
"""
    local_css_content += style_suffix

    # Write the fonts.css file
    css_out_path = CSS_OUT_DIR / "fonts.css"
    css_out_path.write_text(local_css_content, encoding="utf-8")
    print(f"Successfully generated {css_out_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
