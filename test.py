TOKEN_FILE_PATH = "token.txt"


def read_config(file_path):
    config = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            # 공백 제거
            line = line.strip()
            # '변수 = "값"' 또는 '변수 = 값' 형식의 줄을 분리하여 처리
            if line:
                key, value = line.split(" = ", 1)
                # 따옴표 제거
                value = value.strip('"')
                config[key] = value
    return config


config = read_config(TOKEN_FILE_PATH)

TOKEN = config.get("TOKEN")
CHANNEL_ID = int(config.get("CHANNEL_ID"))
GUILD_ID = int(config.get("GUILD_ID"))
USER_ID = config.get("user_id")


print(TOKEN)
print(USER_ID)
