from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from example_database import db

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(f"Hello, {message.from_user.first_name}! Use /help to get help with commands.")

@router.message(Command("fb"))
async def cmd_feedback(message: types.Message, command: CommandObject):
    if not command.args:
        return await message.answer("Please, write a feedback text after /fb")
    db.add_feedback(message.from_user.id, message.from_user.full_name, command.args)
    await message.answer("✅ Thanks for your feedback!")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(f"<b>Commands for Guitar 0 bot:</b>\n\n"
        f"/start - restart bot\n"
        f"/help - view this message\n"
        f"/fb - send us your feedback. Example: <code>/fb Bot is great!</code>\n",
        parse_mode="HTML")
