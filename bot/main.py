import asyncio

from constructor import dp, bot, start_polling


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(start_polling(dp, bot))
