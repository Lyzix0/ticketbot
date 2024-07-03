import logging

BOT_TOKEN = "your token"

logger = logging.getLogger("nextcord")
logging.basicConfig(filename="logs/logs.log")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename="logs/nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
