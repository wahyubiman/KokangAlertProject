"""
For background task scheduler
"""
import asyncio
from sentry_sdk import capture_exception
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.indicator_alert.connector import ExchangeConnector
from app.indicator_alert.strategy.msb import MSB
from app.notification.discord import send_discord_msb_msg

scheduler = AsyncIOScheduler()


def scanner_msb_1h():
    """
    run MSB scanner on 1h timeframe
    """
    try:
        webhook_url = os.getenv("DISCORD_WEBHOOK_MSB_1H")
        dfs = ExchangeConnector("binance", "future").data()
        result = MSB().result(dfs)
        if len(result["high"]) != 0 or len(result["low"]) != 0:
            send_discord_msb_msg(webhook_url, "MSB alert | 1h | Binance Future", result)
    except Exception as e:
        capture_exception(e)


def scanner_msb_4h():
    """
    run MSB scanner on 4h timeframe
    """
    try:
        webhook_url = os.getenv("DISCORD_WEBHOOK_MSB_4H")
        dfs = ExchangeConnector("binance", "future").data("4h")
        result = MSB().result(dfs)
        if len(result["high"]) != 0 or len(result["low"]) != 0:
            send_discord_msb_msg(webhook_url, "MSB alert | 4h | Binance Future", result)
    except Exception as e:
        capture_exception(e)


def background_task():
    """
    start a background task
    """
    try:
        scheduler.add_job(scanner_msb_1h, "cron", hour="0-23")  # run every hour
        scheduler.add_job(scanner_msb_4h, "cron", hour="*/4")  # run every 4 hour
        scheduler.start()  # start the scheduler
        # asyncio.get_event_loop().run_forever()
    except Exception as e:
        capture_exception(e)
