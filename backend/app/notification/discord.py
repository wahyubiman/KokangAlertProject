from discord_webhook import DiscordWebhook, DiscordEmbed
from sentry_sdk import capture_exception

# if rate_limit_retry is True then in the event that you are being rate
# limited by Discord your webhook will automatically be sent once the
# rate limit has been lifted


def discord_webhook_init(url: str) -> DiscordWebhook:
    """
    init discord webhook

    Args:
        url (str): url webhook

    Returns:
        DiscordWebhook: DiscordWebhook class
    """
    return DiscordWebhook(url=url, rate_limit_retry=True)


def send_discord_msb_msg(url: str, title: str, messages: dict):
    """
    send notification via discord webhook when msb break happen

    Args:
        url (str): webhook url
        title (str): title for message
        messages (dict): dict with high & low key
    """
    try:
        webhook = discord_webhook_init(url)
        embed = DiscordEmbed(
            title=title,
            description="@everyone\n\n",
            color="03b2f8",
        )
        msb_high_text = ""
        msb_low_text = ""
        if len(messages["high"]) != 0:
            for msg_high in messages["high"]:
                msb_high_text += "- " + msg_high + "\n"
            embed.add_embed_field(name="High Break", value=msb_high_text)
        if len(messages["low"]) != 0:
            for msg_low in messages["low"]:
                msb_low_text += "- " + msg_low + "\n"
            embed.add_embed_field(name="Low Break", value=msb_low_text)

        embed.set_footer(text="Created by: Kokang")
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        capture_exception(e)


def send_discord_macd_cross_msg(url: str, title: str, messages: dict):
    """
    send notification via discord webhook when macd cross happen

    Args:
        url (str): webhook url
        title (str): title for message
        messages (dict): dict with high & low key
    """
    try:
        webhook = discord_webhook_init(url)
        embed = DiscordEmbed(
            title=title,
            description="@everyone\n\n",
            color="03b2f8",
        )
        macd_cross_high_text = ""
        macd_cross_low_text = ""
        if len(messages["high"]) != 0:
            for msg_high in messages["high"]:
                macd_cross_high_text += "- " + msg_high + "\n"
            embed.add_embed_field(name="MACD Cross Down", value=macd_cross_high_text)
        if len(messages["low"]) != 0:
            for msg_low in messages["low"]:
                macd_cross_low_text += "- " + msg_low + "\n"
            embed.add_embed_field(name="MACD Cross High", value=macd_cross_low_text)

        embed.set_footer(text="Created by: Kokang")
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        capture_exception(e)
