## Random Poster Bot

This as a Telegram Bot for random posting on your Telegram Channel.

Before main installation you have to install Git version "^2.40.1",
Docker "^24.0.2" and Docker Compose "^2.7.0", also you need existing Telegram Bot and channel.

1. Firstly you need to clone repository
```
$: git clone https://github.com/averagepythonfan/random_poster.git
```

2. So let's install the project
```
$: docker compose up -d --build
```

3. Run the migrations
```
$: docker exec bot_cont alembic upgrade head
```


4. Edit .env-example file and enter your own environments like TG bot TOKEN, your channel ID, etc.
5. Add bot to your channel
6. Send some memes to your TG Bot
7. Restart your project
```
$: docker compose restart
```