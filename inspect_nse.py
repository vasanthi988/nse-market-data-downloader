import re
from urllib.parse import urljoin

from src.downloader import create_session, fetch_page
from src.config import DATASETS

BASE_URL = "https://www.nseindia.com"

KEYWORDS = [
    "fetch(", "axios", "xmlhttprequest", "$.ajax",
    "api/", "api.", "endpoint", "gainers", "losers",
    "json", "volume-gainers", "upper-band",
    "52-week", "url:", "url =",
]


def inspect_javascript(session, page_url, html):
    scripts = re.findall(
        r'<script\b[^>]*\bsrc=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )

    relevant_scripts = [
        src for src in scripts
        if any(word in src.lower() for word in [
            "live-analysis",
            "volumegainers",
            "gainers",
            "losers",
            "upper-band",
            "52-week",
        ])
    ]

    print("\nRelevant JavaScript files:", len(relevant_scripts))

    for src in relevant_scripts:
        js_url = urljoin(page_url, src)

        try:
            response = session.get(js_url, timeout=30)
            print(f"\n--- JS: {js_url} ---")
            print("HTTP status:", response.status_code)
            print("Response length:", len(response.text))

            if response.status_code != 200:
                continue

            matches = []
            for number, line in enumerate(
                response.text.splitlines(), start=1
            ):
                if any(word in line.lower() for word in KEYWORDS):
                    matches.append((number, line.strip()[:500]))

            if matches:
                for number, line in matches[:50]:
                    print(f"{number}: {line}")
            else:
                print("No matching references found.")

        except Exception as exc:
            print("JavaScript inspection failed:", exc)


def main():
    session = create_session()

    for dataset_name in DATASETS:
        print("\n" + "=" * 65)
        print("DATASET:", dataset_name)

        try:
            response = fetch_page(session, dataset_name)
            html = response.text

            print("HTTP status:", response.status_code)
            print("Response length:", len(html))
            print("Contains table tag:", "<table" in html.lower())
            print(
                "Contains JSON marker:",
                "application/json" in html.lower(),
            )

            page_url = response.url or urljoin(
                BASE_URL, "/market-data/" + dataset_name
            )

            inspect_javascript(session, page_url, html)

        except Exception as exc:
            print("Inspection failed:", repr(exc))


if __name__ == "__main__":
    main()