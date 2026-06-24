from pathlib import Path
import re

PUBLIC_DIR = Path("c:/Users/lucky dog/Desktop/web_projects/blog-hugo/public")

def check_html_files():
    print("--- Starting HTML Quality Verification ---")
    
    index_html_path = PUBLIC_DIR / "index.html"
    if not index_html_path.exists():
        print("❌ Error: index.html not found in public/!")
        return False
        
    index_content = index_html_path.read_text(encoding="utf-8")
    
    # 1. Check Favicon links
    print("\n[1/5] Checking Favicon links...")
    favicons = ["favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png", "safari-pinned-tab.svg"]
    favicon_ok = True
    for fav in favicons:
        if fav in index_content:
            print(f"  ✅ Found {fav}")
        else:
            print(f"  ❌ Missing {fav}")
            favicon_ok = False
            
    # 2. Check CSP header
    print("\n[2/5] Checking Content-Security-Policy (CSP) headers...")
    csp_match = re.search(r'http-equiv=?["\']?Content-Security-Policy["\']?\s+content=["\']([^"\']+)["\']', index_content, re.IGNORECASE)
    if csp_match:
        csp_content = csp_match.group(1)
        print("  Found CSP header content:")
        print(f"    {csp_content.strip()}")
        
        # Verify no unsafe-inline for script-src
        if "script-src" in csp_content:
            script_src = [part for part in csp_content.split(";") if "script-src" in part][0]
            if "unsafe-inline" in script_src:
                print("  ❌ CSP violation: 'unsafe-inline' found in script-src!")
            else:
                print("  ✅ CSP success: 'unsafe-inline' removed from script-src!")
                
            if "sha256-9+XWnYTFVgY682OAV67M8L4Q1RlYMmLD3EiWQxZdlOg=" in script_src:
                print("  ✅ CSP success: Dark mode script SHA-256 hash registered!")
            else:
                print("  ❌ CSP warning: Dark mode script SHA-256 hash not found!")
                
        # Verify no unsafe-inline for style-src
        if "style-src" in csp_content:
            style_src = [part for part in csp_content.split(";") if "style-src" in part][0]
            if "unsafe-inline" in style_src:
                print("  ❌ CSP violation: 'unsafe-inline' found in style-src!")
            else:
                print("  ✅ CSP success: 'unsafe-inline' removed from style-src!")
    else:
        print("  ❌ CSP header not found in index.html!")

    # 3. Check target="_blank" safety
    print("\n[3/5] Checking target=\"_blank\" safety...")
    unsafe_links = 0
    total_blank_links = 0
    
    for html_file in PUBLIC_DIR.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        # Find all <a> tags with target="_blank" or target=_blank
        links = re.findall(r'<a[^>]+target=?["\']?_blank["\']?[^>]*>', content)
        for link in links:
            total_blank_links += 1
            if "noopener" not in link or "noreferrer" not in link:
                print(f"  ❌ Unsafe link in {html_file.relative_to(PUBLIC_DIR)}: {link}")
                unsafe_links += 1
                
    if unsafe_links == 0:
        print(f"  ✅ All {total_blank_links} target=\"_blank\" links are safe (noopener noreferrer)!")
    else:
        print(f"  ❌ Found {unsafe_links} unsafe target=\"_blank\" links!")

    # 4. Check inline styles in Projects list
    print("\n[4/5] Checking inline styles in Projects page...")
    projects_html_path = PUBLIC_DIR / "projects" / "index.html"
    if projects_html_path.exists():
        projects_content = projects_html_path.read_text(encoding="utf-8")
        # Check if we still have inline styling for the cards
        if "display:grid" in projects_content or "grid-template-columns" in projects_content:
            print("  ❌ Inline styling still present in projects page!")
        else:
            print("  ✅ Projects page inline styles successfully replaced with CSS classes!")
    else:
        print("  ⚠️ projects/index.html not generated or does not exist.")

    # 5. Check local font files
    print("\n[5/5] Checking local font files in public/fonts/...")
    fonts_dir = PUBLIC_DIR / "fonts"
    fonts_css_path = PUBLIC_DIR.parent / "assets" / "css" / "extended" / "fonts.css"
    
    if not fonts_dir.exists():
        print("  ❌ Fonts directory not found in public/!")
    elif not fonts_css_path.exists():
        print("  ❌ fonts.css not found in assets/css/extended/!")
    else:
        fonts_css_content = fonts_css_path.read_text(encoding="utf-8")
        referenced_fonts = re.findall(r"url\('/fonts/([^']+)'\)", fonts_css_content)
        if not referenced_fonts:
            referenced_fonts = re.findall(r'url\("/fonts/([^"]+)"\)', fonts_css_content)
            
        if not referenced_fonts:
            print("  ⚠️ No referenced local fonts found in fonts.css.")
        else:
            print(f"  Found {len(referenced_fonts)} referenced fonts in fonts.css.")
            fonts_ok = True
            for font in referenced_fonts:
                local_font_file = fonts_dir / font
                if local_font_file.exists() and local_font_file.stat().st_size > 0:
                    print(f"  ✅ Font file exists: {font} ({local_font_file.stat().st_size} bytes)")
                else:
                    print(f"  ❌ Font file missing or empty: {font}")
                    fonts_ok = False
            if fonts_ok:
                print("  ✅ All referenced local fonts are present and non-empty in public/fonts/!")
            else:
                print("  ❌ Some local fonts are missing or empty in public/fonts/!")

    print("\n--- Verification Completed ---")

if __name__ == "__main__":
    check_html_files()
