from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_url = 'https://discord.com/api/webhooks/1090625465422708777/xhihjuFS9ACpgB0UCksklpL6Idz6vyAG9yY8F1kzKoe75IFaWfuGW_8pHaoVSBY5cHzr'


def Webhook_basic(description) :
    webhook = DiscordWebhook(url = webhook_url, content = description)
    response = webhook.execute()
    return response


def Webhook_embed(title, description, thumbnail_image, set_url) :
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title=title, description=description, color='03b2f8')
    embed.set_thumbnail(thumbnail_image)
    embed.set_url(set_url)
    webhook.add_embed(embed=embed)

    response = webhook.execute()
    return response