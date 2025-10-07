import os
import datetime
import asyncio
import aiohttp
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from livekit.api import AccessToken, VideoGrants
from livekit import api

load_dotenv(".env")
app = Flask(__name__)
 
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_SECRET = os.getenv("LIVEKIT_API_SECRET")
HTTP_URL = LIVEKIT_URL.replace("wss://", "https://")

@app.route("/")
def home():
    return render_template("index.html", lk_url=LIVEKIT_URL)
 
@app.route("/token", methods=["POST"])
def token():
    room = request.json.get("room", "default")
    identity = request.json.get("identity", "user-" + datetime.datetime.utcnow().strftime("%H%M%S"))

    token = AccessToken(api_key=LIVEKIT_KEY, api_secret=LIVEKIT_SECRET)
    
    token = token.with_identity(identity)
    
    video_grants = VideoGrants(
        room_join=True,
        room=room,
        can_publish=True,
        can_subscribe=True
    )
    token = token.with_grants(video_grants)

    return jsonify({"token": token.to_jwt()})

async def create_room_async():
    """Async function to create the room using LiveKitAPI."""
    try:
        lkapi = api.LiveKitAPI(
            url=HTTP_URL,
            api_key=LIVEKIT_KEY,
            api_secret=LIVEKIT_SECRET
        )
        
        room = await lkapi.room.create_room(
            api.CreateRoomRequest(name="default")
        )
        print(f"Room '{room.name}' created successfully.")
        await lkapi.aclose()
        return room
    except Exception as e:
        print(f"Room creation note: {e}")
        return None

try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_room_async())
    loop.close()
except Exception as e:
    print(f"Startup room creation failed: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)