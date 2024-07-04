from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from settings import BOT_TOKEN, logger
from handlers import handle_message_request


logger.debug("Init bot")
bot = Bot(BOT_TOKEN)
logger.debug("Init dp")
dp = Dispatcher()

logger.debug("Registering handlers")

dp.message.register(handle_message_request)


async def start_polling(dispatcher: Dispatcher, polling_bot: Bot):
    try:
        logger.debug("Skipping updates")
        await polling_bot(DeleteWebhook(drop_pending_updates=True))
        logger.warning("Polling started")
        await dispatcher.start_polling(polling_bot, polling_timeout=10)
    except Exception as e:
        logger.warning(f"Bot stopped polling due to: {e}")
