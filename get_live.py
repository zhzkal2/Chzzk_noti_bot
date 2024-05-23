import requests


async def get_live(user_id):
    url = f"https://api.chzzk.naver.com/service/v2/channels/{user_id}/live-detail"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 일으킵니다.
        data = response.json()  # JSON 응답을 파이썬 사전으로 변환합니다.
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return None
