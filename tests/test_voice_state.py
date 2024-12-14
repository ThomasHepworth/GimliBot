from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.cogs.music_bot.music_cog import VoiceState


@pytest.fixture
def mock_bot():
    """Fixture for a mocked bot."""
    bot = Mock()
    bot.loop = asyncio.get_event_loop()
    return bot


@pytest.fixture
def mock_ctx():
    """Fixture for a mocked context."""
    ctx = Mock()
    ctx.voice_client = None
    return ctx


@pytest.fixture
def mock_voice_client() -> AsyncMock:
    voice_client = AsyncMock()
    voice_client.disconnect = AsyncMock()
    return voice_client


@pytest.fixture
def voice_state(mock_bot, mock_ctx):
    """Fixture for the VoiceState instance."""
    with patch("asyncio.create_task", return_value=AsyncMock()):
        return VoiceState(mock_bot, mock_ctx)


# TODO(ThomasHepworth): Fix test when I get a moment
# @pytest.mark.asyncio
# async def test_audio_player_task_timeout(voice_state: VoiceState):
#     """Test that audio_player_task times out and stops the bot."""
#     with patch("asyncio.sleep", new=AsyncMock()):  # Avoid real delays
#         voice_state.songs.get = AsyncMock(side_effect=asyncio.TimeoutError)

#         stop_mock = AsyncMock()
#         voice_state.stop = stop_mock

#         await voice_state.audio_player_task()

#         stop_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_play_next_song(voice_state: VoiceState):
    """Test the play_next_song method."""
    voice_state.voice = Mock()
    voice_state.next.set = Mock()

    voice_state.play_next_song()

    voice_state.next.set.assert_called_once()


@pytest.mark.asyncio
async def test_skip(voice_state: VoiceState):
    """Test the skip method."""
    voice_state.voice = Mock()
    voice_state.current = "Some Song"

    voice_state.skip()

    voice_state.voice.stop.assert_called_once()


@pytest.mark.asyncio
async def test_stop(voice_state: VoiceState):
    """Test the stop method."""
    voice_state.songs = Mock()

    voice_mock = AsyncMock()
    voice_mock.disconnect = AsyncMock()
    voice_state.voice = voice_mock

    await voice_state.stop()

    voice_state.songs.clear.assert_called_once()
    voice_mock.disconnect.assert_awaited_once()
    assert voice_state.voice is None


@pytest.mark.asyncio
async def test_volume_setter(voice_state: VoiceState):
    """Test the volume setter with valid and invalid values."""
    voice_state.volume = 0.7
    assert voice_state.volume == 0.7

    with pytest.raises(ValueError):
        voice_state.volume = 1.5
