import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
from example_database import db
# from YOUR_DATABASE import db

load_dotenv()

router = Router()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(user, text):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "New feedback(from TG bot)"

    body = f"""
User: {user.full_name}
Username: @{user.username}
ID: {user.id}

Message:
{text}
"""
    
    

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(f"Hello, {message.from_user.first_name}! Use /help to get help with commands.")

@router.message(Command("fb"))
async def feedback_handler(message: Message):
    text = message.text.replace("/feedback", "").strip()
    if not text:
        await message.answer("Please, write a text after /fb")
        return
    await asyncio.to_thread(send_email, message.from_user, text)
    await message.answer("✅ Thanks for your feedback!")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(f"<b>Commands for this Guitar 0 bot:</b>\n\n"
        f"/start - restart bot\n"
        f"/help - show this menu\n"
        f"/fb - give us your feedback",
        parse_mode="HTML")
