import asyncio
import httpx

URL = "https://gamma-api.polymarket.com/markets"


async def fetch_weather_markets():
    """Fetch active weather markets from the Polymarket Gamma API.

    Returns:
        list[dict]: A list of market objects returned by the API.

    Raises:
        httpx.HTTPStatusError: If the server returns a non-2xx response.
        httpx.ConnectError: If the host cannot be reached.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(URL, params={
            "tag": "weather",
            "active": True,
            "limit": 50
        })
        resp.raise_for_status()
        data = resp.json()

    return data


if __name__ == "__main__":
    try:
        markets = asyncio.run(fetch_weather_markets())
        print(f"Fetched {len(markets)} weather market(s).")
        for m in markets[:5]:
            print(m.get("question", m))
    except httpx.ConnectError as e:
        print(f"Network error: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e}")
