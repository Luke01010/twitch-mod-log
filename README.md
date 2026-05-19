# Twitch & YouTube Chat Moderation Log Bot

A python-based bot system that tracks YouTube and Twitch chat moderation actions (Bans, Timeouts, and Deleted Messages) and reports them to Discord using high-fidelity rich screenshots and plain text webhook logs.

---

## Features
- **Twitch Integration**: Listens to IRC chat events (`CLEARCHAT`, `CLEARMSG`) to track bans, timeouts, and deleted messages.
- **YouTube Integration**: Monitors active streams via the YouTube Data API v3 to log chat deletions and user bans.
- **Rich Visuals**: Generates beautiful dark-themed image snapshots displaying the deleted message context and colored username badges, rendered using the modern **Inter** font.
- **Dual Webhooks**:
  - Main webhook: Posts rich PNG image snapshots of mod actions.
  - Plain webhook (optional): Posts instant plain-text notifications, complete with direct Discord message links to the rich snapshot post.
- **Docker Ready**: Containers configured with font assets pre-packaged.

---

## 1. Setup Environment Variables (`.env`)

Create a `.env` file in the root directory by copying the configuration below and filling in your credentials:

```env
# Twitch Settings
TWITCH_CHANNEL=your_channel_name
TWITCH_USERNAME=your_bot_username
TWITCH_TOKEN=oauth:your_twitch_oauth_token

# YouTube Settings
YT_CHANNEL_ID=your_youtube_channel_id
YT_API_KEY=your_google_youtube_api_key

# Discord Webhooks
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_PLAIN_URL=https://discord.com/api/webhooks/...
```

### How to Get Your Credentials

#### A. Twitch Username & OAuth Token (`TWITCH_TOKEN`)
1. Create or log into the Twitch account you want the bot to use.
2. Visit the [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/).
3. Click **Connect** and authorize the application.
4. Copy the generated password string (it begins with `oauth:`). This is your `TWITCH_TOKEN`.
5. Enter the target channel you want to monitor in `TWITCH_CHANNEL` (e.g., `xqc`).

#### B. YouTube Channel ID (`YT_CHANNEL_ID`)
To track YouTube chat, you need the unique channel ID of the creator:
- **Direct Method**: Go to the YouTube creator's channel page, click **About** (or share button), and click **Copy Channel ID**.
- **Alternative Method**: If it is hidden under a handle (e.g. `@username`), copy the channel page link and paste it into a free tool like [CommentPicker YouTube Channel ID Finder](https://commentpicker.com/youtube-channel-id.php) to retrieve the `UC...` ID.

#### C. Google API Key (`YT_API_KEY`)
The YouTube bot polls live chat using the YouTube Data API v3:
1. Log into the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g. `youtube-mod-log`).
3. Navigate to **API Library** and search for **YouTube Data API v3**. Click **Enable**.
4. Go to the **Credentials** page from the sidebar.
5. Click **Create Credentials** -> **API Key**. Copy your generated key and add it to `YT_API_KEY`.
6. *(Highly Recommended)* Under API restrictions, restrict the key to **only** allow calls to the **YouTube Data API v3**.

#### D. Discord Webhook URLs
1. In Discord, navigate to the text channel where you want mod logs posted.
2. Click **Channel Settings** (gear icon) -> **Integrations** -> **Webhooks** -> **Create Webhook**.
3. Customize the webhook name/avatar, then click **Copy Webhook URL**.
4. Set this as `DISCORD_WEBHOOK_URL` (for image screenshots) and optionally create a second one for `DISCORD_WEBHOOK_PLAIN_URL` (for plain text backup logs).

---

## 2. Option A: Running via Docker (Recommended)

Docker is the easiest way to run the bots because it automatically installs and packages all system dependencies—most notably the **Inter** font family required to render high-fidelity PNG logs.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) on your machine.

### Run with Docker Compose
The included `docker-compose.yml` configures two services: `twitch-mod-log` and `yt-mod-log`.

```bash
# Build and start both bots in the background
docker compose up --build -d

# View live container logs
docker compose logs -f

# Stop the bots
docker compose down
```

---

## 3. Option B: Running Natively (Naked `.py` Files)

Running the scripts directly on your host machine is fully supported but requires a manual step to make sure the **Inter** font files are present.

### Prerequisites
- Python 3.12 or newer installed.
- **Fonts**: The PIL image library draws text using the Inter font. The Python scripts look for Inter at standard Linux system paths:
  ```python
  FONT_BOLD = "/usr/share/fonts/truetype/inter/Inter-Bold.ttf"
  FONT_REGULAR = "/usr/share/fonts/truetype/inter/Inter-Regular.ttf"
  FONT_ITALIC = "/usr/share/fonts/truetype/inter/Inter-Italic.ttf"
  ```
  If you are running on macOS or Windows:
  1. Download the Inter font zip package from [rsms/inter releases](https://github.com/rsms/inter/releases).
  2. Create a local folder called `fonts` in the project root, extract the `.ttf` files into it.
  3. Open `bot.py` and `yt_bot.py` and modify those paths to point to your local assets, e.g.:
     ```python
     FONT_BOLD = "fonts/Inter-Bold.ttf"
     FONT_REGULAR = "fonts/Inter-Regular.ttf"
     FONT_ITALIC = "fonts/Inter-Italic.ttf"
     ```

### Execution Steps

1. **Clone & Enter directory**:
   ```bash
   cd twitch-mod-log
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the bots**:
   To load environment variables from your `.env` file, you can prefix the execution command (on macOS/Linux):
   
   ```bash
   # Run the Twitch chat bot
   env $(cat .env | xargs) python bot.py

   # Run the YouTube live chat bot
   env $(cat .env | xargs) python yt_bot.py
   ```

---

## Troubleshooting

### YouTube API Quota Exhausted
The YouTube bot uses the YouTube Data API v3. To avoid rapid quota consumption, it uses a zero-cost RSS feed parsing method (`CHECK_STREAM_INTERVAL = 300` seconds) to check if the channel is live. Once it detects a stream, it switches to live chat polling. 
If your quota is exceeded, the bot will log an error message and wait. Quotas automatically reset daily at midnight Pacific Time.

### Discord Webhook Failures
Make sure your Discord webhook URL does not contain trailing spaces. Webhooks require an active internet connection, and the main webhook will attempt to upload binary image files.
