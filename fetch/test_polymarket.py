import asyncio
import json
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from fetch.polymarket import fetch_weather_markets, URL


SAMPLE_MARKETS = [
    {"id": "1", "question": "Will it rain in NYC this week?", "active": True},
    {"id": "2", "question": "Will it snow in Chicago?", "active": True},
]


@pytest.mark.asyncio
async def test_fetch_weather_markets_success():
    mock_response = MagicMock()
    mock_response.json.return_value = SAMPLE_MARKETS
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        result = await fetch_weather_markets()

    assert result == SAMPLE_MARKETS
    mock_client.get.assert_called_once_with(
        URL,
        params={"tag": "weather", "active": True, "limit": 50},
    )


@pytest.mark.asyncio
async def test_fetch_weather_markets_returns_list():
    mock_response = MagicMock()
    mock_response.json.return_value = SAMPLE_MARKETS
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        result = await fetch_weather_markets()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["question"] == "Will it rain in NYC this week?"


@pytest.mark.asyncio
async def test_fetch_weather_markets_http_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found",
        request=MagicMock(),
        response=MagicMock(status_code=404),
    )

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        with pytest.raises(httpx.HTTPStatusError):
            await fetch_weather_markets()
