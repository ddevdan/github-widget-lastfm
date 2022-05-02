from decouple import config


LAST_FM_API_KEY = config("LAST_FM_API_KEY")
LAST_FM_BASE_URL = f"https://ws.audioscrobbler.com/2.0/?api_key={LAST_FM_API_KEY}&method=user.getrecenttracks&format=json"
