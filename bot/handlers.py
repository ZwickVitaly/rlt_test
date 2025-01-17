from copy import deepcopy
from datetime import datetime, timedelta
from json import dumps, loads
from json.decoder import JSONDecodeError

from aiogram.types import Message
from mongo_connection import MONGO_PIPE, collection
from settings import LOOKUP_DATE_UNITS, logger


async def handle_message_request(message: Message):
    logger.info(f"User: {message.from_user.id} requested data: {message.text}")
    try:
        request = loads(message.text)
        if not isinstance(request, dict):
            raise ValueError("Invalid data")
    except (JSONDecodeError, ValueError) as e:
        logger.debug(f"Invalid data fmt: {e.args[0]}")
        await message.answer('{"error": "Невалидный формат данных"}')
        return
    try:
        logger.debug("Extracting dates")
        start = datetime.fromisoformat(request.get("dt_from"))
        end = datetime.fromisoformat(request.get("dt_upto"))
    except (TypeError, ValueError):
        logger.debug("Invalid date format")
        await message.answer('{"error": "Невалидный формат даты"}')
        return
    group_type = request.get("group_type")
    if group_type not in LOOKUP_DATE_UNITS:
        logger.debug("Invalid grouper")
        await message.answer('{"error": "Невалидный формат группировки"}')
        return
    start_exists = collection.find_one({}, {"dt": start})
    if not start_exists.get("value"):
        collection.insert_one({"dt": start, "value": 0})
    end_exists = collection.find_one({}, {"dt": end})
    if not end_exists.get("value"):
        collection.insert_one({"dt": start, "value": 0})
    pipe = deepcopy(MONGO_PIPE)
    pipe[0]["$match"]["dt"] = {"$gte": start, "$lte": end}
    pipe[1]["$group"]["_id"]["$dateTrunc"]["unit"] = group_type
    pipe[3]["$densify"]["range"]["unit"] = group_type
    pipe[3]["$densify"]["range"]["bounds"] = [start, end + timedelta(milliseconds=1)]
    data = collection.aggregate(pipe).next()
    logger.info(f"Returning data: {data}")
    if not data:
        await message.answer('{"error": "Ничего не найдено"}')
        return
    await message.answer(dumps(data))
