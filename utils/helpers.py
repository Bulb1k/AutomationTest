from urllib.parse import urlparse
from data.config import PROXY_FILE

def get_proxies(proxy_file: str = PROXY_FILE) -> list[dict]:
    proxies = []
    with open(proxy_file, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if "://" not in line:
                line = "http://" + line

            parsed = urlparse(line)

            proxies.append({
                "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
                "username": parsed.username,
                "password": parsed.password
            })

    return proxies