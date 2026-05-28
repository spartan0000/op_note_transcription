import pytest
from unittest.mock import AsyncMock, patch

from types import SimpleNamespace

from backend.app.services.functions import _empty_report, extract_structured_data


@pytest.mark.asyncio
async def test_bad_llm_output():
    fake = {
        "transcript": "this is a test"
    }

    with patch("backend.app.services.functions.chat_client.responses.parse", new_callable=AsyncMock) as mock_generate:

        mock_generate.return_value = "This is the llm making up some random stuff"

        result = await extract_structured_data(fake['transcript']) 
    
    assert result == _empty_report()

@pytest.mark.asyncio
async def test_extraction_exception():
    with patch("backend.app.services.functions.chat_client.responses.parse", new_callable=AsyncMock) as mock_generate:

        mock_generate.side_effect = Exception("LLM parsing failed")

        result = await extract_structured_data("this is a test")

    assert result == _empty_report()