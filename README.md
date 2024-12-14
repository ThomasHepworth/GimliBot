# GimliBot 🎵

GimliBot is a simple yet powerful **Discord music bot** that brings high-quality music playback to your server. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download and play music directly from YouTube.

---

## 📜 Features

- 🎶 **Play music** from YouTube.
- ⏯️ **Pause/Resume** music playback.
- ⏭️ **Skip** the current song.
- 🔄 **Loop** songs or shuffle the queue.
- 🎚️ **Volume control** to adjust playback volume.
- 📋 **View the queue** with pagination support.
- 📀 **Display the currently playing song.**
- 🧹 **Clear the queue** or remove specific songs.

---

## 🛠️ Commands

| Command                      | Description                                              |
|------------------------------|----------------------------------------------------------|
| `!play <song>`               | Plays a song. Searches YouTube if no URL is provided.    |
| `!join`                      | Makes the bot join your voice channel.                   |
| `!leave`                     | Clears the queue and disconnects from the voice channel. |
| `!pause`                     | Pauses the currently playing song.                       |
| `!resume`                    | Resumes the paused song.                                 |
| `!stop`                      | Stops the music and clears the queue.                    |
| `!skip`                      | Vote to skip the current song (3 votes required).        |
| `!queue` or `!q`             | Displays the current queue (paginated).                  |
| `!shuffle`                   | Shuffles the music queue.                                |
| `!remove <index>`            | Removes a song from the queue at a given index.          |
| `!loop`                      | Toggles looping of the currently playing song.           |
| `!volume <0-100>`            | Adjusts the playback volume.                             |
| `!now`                       | Displays information about the current song.             |

---

## 🚀 Getting Started

### Prerequisites

Before running `GimliBot`, ensure you have:

- **Python 3.11+** installed.
- **Docker** installed.
- **Discord bot token** from the [Discord Developer Portal](https://discord.com/developers/applications).

<details>
<summary><strong>🧩 Installation and setup</strong></summary>

1. **Clone the repository**:

```sh
git clone <ssh_url>
cd GimliBot
```

2. Install _all_ dependencies using uv:
```sh
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml --all-extras
```

3.	Set up the bot token:
Create an .env file in the project root and add your Discord bot token:
```
TOKEN=DISCORD_BOT_TOKEN
```

</details>

<details>
<summary><strong>🧹 Code Quality and Formatting</strong></summary>

This project uses **Ruff** for code linting and formatting to ensure clean, readable, and consistent code.

- **Check for linting issues**:
   ```bash
   ruff check .

	•	Format the code:

ruff format .

</details>

<hr>

### 🐳 Run the bot with Docker Compose

`GimliBot` is designed to be run in a Docker container. The provided `docker-compose.yml` file sets up the bot and its dependencies in a containerised environment.

1.	Create a .env file in the project root and add your bot token:
```
TOKEN=YOUR_DISCORD_BOT_TOKEN
```

2.	Run the bot using Docker Compose (the compose file can be found at [docker.compose.yml](./docker-compose.yml)):

```
docker-compose up --build -d
```


This will build the Docker image, start the bot, and keep it running in the background.

<hr>


### 🎥 Bot in Action

