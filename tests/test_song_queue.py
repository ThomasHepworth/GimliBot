import asyncio

import pytest

from src.cogs.music_bot.song_queue import SongQueue


@pytest.fixture(scope="function")
def song_queue():
    return SongQueue()


@pytest.mark.asyncio
async def test_basic_queue_operations(song_queue: SongQueue):
    await song_queue.put("Song 1")
    await song_queue.put("Song 2")

    assert len(song_queue) == 2
    assert song_queue.peek() == "Song 1"
    assert await song_queue.get() == "Song 1"
    assert len(song_queue) == 1
    assert await song_queue.get() == "Song 2"
    assert song_queue.empty()


@pytest.mark.asyncio
async def test_slicing_and_indexing(song_queue: SongQueue):
    # song_queue = SongQueue()
    songs = ["Song 1", "Song 2", "Song 3"]
    for song in songs:
        await song_queue.put(song)

    assert song_queue[0] == "Song 1"
    assert song_queue[1:3] == ["Song 2", "Song 3"]


@pytest.mark.asyncio
async def test_peek(song_queue: SongQueue):
    """Test the peek functionality."""
    await song_queue.put("Song 1")
    assert song_queue.peek() == "Song 1"
    assert len(song_queue) == 1  # Peek should not remove the song


@pytest.mark.asyncio
async def test_shuffle(song_queue: SongQueue):
    """Test the shuffle functionality."""
    songs = ["Song 1", "Song 2", "Song 3", "Song 4"]
    for song in songs:
        await song_queue.put(song)

    original_list = song_queue.as_list()
    song_queue.shuffle()
    shuffled_list = song_queue.as_list()

    assert set(original_list) == set(shuffled_list)
    assert original_list != shuffled_list


@pytest.mark.asyncio
async def test_remove(song_queue: SongQueue):
    """Test removing a song by index."""
    songs = ["Song 1", "Song 2", "Song 3"]
    for song in songs:
        await song_queue.put(song)

    song_queue.remove(1)  # Remove "Song 2"
    assert song_queue.as_list() == ["Song 1", "Song 3"]


@pytest.mark.asyncio
async def test_clear(song_queue: SongQueue):
    """Test clearing the queue."""
    await song_queue.put("Song 1")
    await song_queue.put("Song 2")
    assert not song_queue.empty()

    song_queue.clear()
    assert song_queue.empty()


@pytest.mark.asyncio
async def test_as_list(song_queue: SongQueue):
    """Test converting the queue to a list."""
    songs = ["Song 1", "Song 2", "Song 3"]
    for song in songs:
        await song_queue.put(song)

    assert song_queue.as_list() == songs


@pytest.mark.asyncio
async def test_remove_out_of_range(song_queue: SongQueue):
    """Test removing a song with an invalid index."""
    await song_queue.put("Song 1")

    with pytest.raises(IndexError):
        song_queue.remove(5)  # Index out of range


@pytest.mark.asyncio
async def test_peek_empty_queue(song_queue: SongQueue):
    """Test peek on an empty queue."""
    with pytest.raises(asyncio.QueueEmpty):
        song_queue.peek()


@pytest.mark.asyncio
async def test_index_out_of_range(song_queue: SongQueue):
    """Test indexing out of range."""
    await song_queue.put("Song 1")

    with pytest.raises(IndexError):
        _ = song_queue[5]


@pytest.mark.asyncio
async def test_slicing_empty_queue(song_queue: SongQueue):
    """Test slicing an empty queue."""
    assert song_queue[:] == []
