
import json

from src.downloader import create_session

BASE_URL = "https://www.nseindia.com"

ENDPOINTS = {
    "top-gainers": "/api/live-analysis-variations?index=gainers",
    "top-losers": "/api/live-analysis-variations?index=loosers",
    "upper-band-hitters": "/api/live-analysis-price-band-hitter",
    "volume-gainers": "/api/live-analysis-volume-gainers",
    "52-week-high": "/api/live-analysis-data-52weekhighstock",
}


def main():
    session = create_session()

    # Open the homepage first to initialize the session.
    try:
        home = session.get(BASE_URL, timeout=30)
        print("NSE homepage status:", home.status_code)
    except Exception as exc:
        print("Could not initialize NSE session:", exc)
        return

    for name, endpoint in ENDPOINTS.items():
        print("\n" + "=" * 60)
        print("DATASET:", name)

        try:
            response = session.get(
                BASE_URL + endpoint,
                headers={
                    "Referer": BASE_URL + "/",
                    "Accept": "application/json, text/plain, */*",
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/130.0.0.0 Safari/537.36"
                    ),
                },
                timeout=30,
            )

            print("HTTP status:", response.status_code)
            print("Content type:", response.headers.get("Content-Type"))

            if response.status_code != 200:
                print("Response preview:", response.text[:500])
                continue

            try:
                data = response.json()
            except ValueError:
                print("Response is not valid JSON.")
                print("Response preview:", response.text[:500])
                continue

            if isinstance(data, dict):
                print("Top-level keys:", list(data.keys()))

            if isinstance(data, list):
                print("Record count:", len(data))
                print("Sample:", json.dumps(data[:2], indent=2)[:2500])

            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"{key}: {len(value)} items")
                        if value:
                            print(
                                "Sample:",
                                json.dumps(value[:2], indent=2)[:1500],
                            )
                    elif isinstance(value, dict):
                        print(f"{key}: object with keys {list(value.keys())[:20]}")

                print(
                    "\nJSON preview:",
                    json.dumps(data, indent=2, ensure_ascii=False)[:2500],
                )

        except Exception as exc:
            print("API request failed:", repr(exc))


if __name__ == "__main__":
    main()