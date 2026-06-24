from pathlib import Path
import re
content = Path("public/index.html").read_text(encoding="utf-8")
print("CSP in content:", "Content-Security-Policy" in content)
m = re.search(r'Content-Security-Policy', content)
print("m:", m)
if m:
    idx = m.start()
    print("Surrounding text:")
    print(content[idx-20:idx+300])
