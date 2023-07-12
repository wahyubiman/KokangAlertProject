import requests
import os
from sentry_sdk import capture_exception
from typing import List

url = os.getenv("NTFY_URL")


def send_notif(title: str, results: List, username: str, password: str):
    """
    send notif

    Args:
        title (str): tile text
        results (List): list contain result
        username (str): usernmae for subscribe to ntfy topic
        password (str): password for subscribe to ntfy topic
    """
    data = ""
    result_up = "\n⬆️ MACD Cross Up\n"
    result_down = "\n⬇️ MACD Cross Down\n"
    try:
        if len(results["high"]) != 0:
            for msg_high in results["high"]:
                result_up += "- " + msg_high + "\n"
            data += result_up
        if len(results["low"]) != 0:
            for msg_low in results["low"]:
                result_down += "- " + msg_low + "\n"
            data += result_down
        requests.post(
            url,
            data=data,
            header={"Title": title, "Tags": "rotating_light"},
            auth=(username, password),
        )
    except Exception as e:
        capture_exception(e)
