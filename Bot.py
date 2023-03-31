import discord
import asyncio

from Database.database import Connect


TOKEN = 'MTA5MDEwMzE5NjI4ODAzNjg2NA.GfG_He.G2QR6Mi_RqUF-6UEcyUDT8U1HXuOkkTUEGGBAI'
CHANNEL_ID = 1090105806109823022


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        await self.change_presence(status=discord.Status.online, activity=None)

    async def on_message(self, message):
        conn = Connect()
        cur = conn.cursor()

        if message.author == self.user:
            return

        if message.content == 'log':
            Query = """
                SELECT CONTENT, RECIPIENT, SENDER, PRODUCT_ID, PRODUCT_NAME, DATE_FORMAT(CREATED, "%Y-%m-%d") AS CREATED FROM LOG WHERE SENDER = "Discord"
            """
            cur.execute(Query)
            result = cur.fetchall()
            print(result)

            for i in range(len(result)):
                msg = f"[{result[i][5]}]  -  {result[i][1]}님  -  {result[i][0]}"
                await message.channel.send(msg)

        elif message.content[0] == '!':
            if message.content[1:] == 'ping':
                await message.channel.send(f'pong {message.author.mention}')  # message.author.mention -> 호출한 사람

            elif message.content[1:3] == ("청소"):
                purge_number = message.content.replace("!청소 ", "")
                print(purge_number)
                check_purge_number = purge_number.isdigit()

                if check_purge_number == True:
                    await message.channel.purge(limit=int(purge_number) + 1)
                    msg = await message.channel.send(f"**{purge_number}개**의 메시지를 삭제했습니다.")
                    await asyncio.sleep(3)
                    await msg.delete()

        else:
            await message.channel.send("올바른 값을 입력해주세요.")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)