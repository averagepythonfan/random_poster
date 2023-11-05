from aiogram import types


bot_commands = (
    ('stats', 'stats by posts'),
    ("random", "random post"),
    ('status', 'user status'),
)


commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(
        types.BotCommand(command=cmd[0], description=cmd[1])
    )