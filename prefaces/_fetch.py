import sys, time, os, re, urllib.request, ssl
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

BASE = "https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build"
IMG  = BASE + "/_images"
HERE = os.path.dirname(os.path.abspath(__file__))
SCANS = os.path.join(HERE, "scans")
os.makedirs(SCANS, exist_ok=True)

ctx = ssl.create_default_context()
ctx.minimum_version = ssl.TLSVersion.TLSv1_2

def get(url, binary=False, tries=6, pause=8):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    for t in range(1, tries+1):
        try:
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
                data = r.read()
                if data:
                    return data
        except Exception as e:
            print(f"  try {t} {url[-40:]}: {type(e).__name__} {e}", flush=True)
        time.sleep(pause)
    return None

# resolve missing image filenames for pages 03,04,09
known = {
 "01":"inm_Page_809_Image_0001","02":"inm_Page_810_Image_0001",
 "05":"inm_Page_814_Image_0001","06":"inm_Page_815_Image_0001",
 "07":"inm_Page_816_Image_0001","08":"inm_Page_817_Image_0001",
}
for nn in ["03","04","09"]:
    html = get(f"{BASE}/dictionaries/prefaces/inmpref/inmpref{nn}.html", tries=8, pause=10)
    if html:
        m = re.search(rb'_images/([^"]+\.png)', html)
        if m:
            known[nn] = m.group(1).decode().rsplit('.',1)[0]
            print(f"resolved {nn} -> {known[nn]}", flush=True)
        else:
            print(f"NO IMG in {nn} html (len {len(html)})", flush=True)
    else:
        print(f"FAILED html {nn}", flush=True)
    time.sleep(6)

# download all scans
for nn in sorted(known):
    f = known[nn]
    dest = os.path.join(SCANS, f + ".png")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"{nn} {f}: already {os.path.getsize(dest)}", flush=True); continue
    data = get(f"{IMG}/{f}.png", binary=True, tries=8, pause=10)
    if data and len(data) > 1000:
        open(dest, "wb").write(data)
        print(f"{nn} {f}: {len(data)} bytes OK", flush=True)
    else:
        print(f"{nn} {f}: FAILED", flush=True)
    time.sleep(6)

print("MANIFEST:", {k: known[k] for k in sorted(known)}, flush=True)
print("ALLDONE", flush=True)
