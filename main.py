import discord
from discord import ui, ButtonStyle, Interaction, Embed
from discord.ext import commands, tasks
from get_live import get_live

TOKEN = "MTIzOTk4MjkyMTM2MDg2NzM1OA.GjfNAM.qmwHAzLydca2WxsctrLn30hu2G2oDZEF_JTpJ4"
CHANNEL_ID = 1242727245852966973
GUILD_ID = 1239992071574519859
# https://discord.com/oauth2/authorize?client_id=1239982921360867358&permissions=8&scope=bot
# user_id = "4f7288eb344e2e22488f4f115dacf490"
previous_status = {}

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


class DataStorage:
    def __init__(self):
        self.data = {}

    def save_data(self, user_id, name, answer):
        self.data[user_id] = {"name": name, "id": answer}

    def get_data(self, user_id):
        return self.data.get(user_id, None)


data_storage = DataStorage()


async def check_live_status():
    user_id = list(data_storage.data.keys())[0]
    user_data = data_storage.get_data(user_id)
    chzzk_user_id = user_data["id"]
    print(chzzk_user_id)

    live_status = await get_live(chzzk_user_id)

    # print(chzzk_data["id"])

    if live_status is not None:
        current_status = live_status["content"]["status"]
        print(live_status["content"]["status"])
        # 처음 처리되는 사용자라면 이전 상태를 현재 상태로 초기화합니다.
        if user_id not in previous_status:
            previous_status[user_id] = current_status

        if previous_status[user_id] == "CLOSE" and current_status == "OPEN":
            # if live_status["content"]["status"] == "CLOSE":
            chat_channel = client.get_channel(CHANNEL_ID)
            embed = discord.Embed(
                title=live_status["content"]["liveTitle"], colour=discord.Colour.green()
            )
            embed.set_author(
                name=live_status["content"]["channel"]["channelName"],
                icon_url=live_status["content"]["channel"]["channelImageUrl"],
            )
            preview_url = live_status["content"]["liveImageUrl"].replace(
                "_{type}", "_1080"
            )
            embed.set_image(url=preview_url)

            embed.url = f"https://chzzk.naver.com/live/{chzzk_user_id}"
            embed.description = f"**{live_status['content']['channel']['channelName']}** 님이 방송을 시작했습니다!"

            embed.set_footer(
                text=f"{client.user.name} 방송 알림",
                icon_url=client.user.display_avatar.url,
            )

            await chat_channel.send(embed=embed)
        previous_status[user_id] = current_status


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    check_status_task.start()


@tasks.loop(minutes=1)
async def check_status_task():
    try:
        print("Running scheduled task...")
        await check_live_status()
    except Exception as e:
        print(f"Error occurred: {e}")


class Questionnaire(ui.Modal, title="이름과 ID를 입력해주세요."):
    name = ui.TextInput(label="스트리머 이름 입력")
    answer = ui.TextInput(
        label="스트리머 채널 ID 입력", style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        data_storage.save_data(user_id, self.name.value, self.answer.value)
        await interaction.response.send_message(
            f"Thanks for your response, {self.name}!", ephemeral=True
        )
        await check_live_status()


@client.command()
async def 등록(ctx):
    """Sends a button that triggers the modal."""
    button = ui.Button(label="클릭", style=ButtonStyle.green)

    async def button_callback(interaction: Interaction):
        await interaction.response.send_modal(Questionnaire())

    button.callback = button_callback
    view = ui.View()
    view.add_item(button)
    await ctx.send("버튼을 클릭해주세요.", view=view)


client.run(TOKEN)
