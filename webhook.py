from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_url =


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