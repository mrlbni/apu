from flask import Flask, request, Response
from pyrogram import Client
import os, time

app = Flask(__name__)

# Telegram credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

tg = Client("tg_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
tg.start()

CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk, safe for Koyeb memory

@app.route("/stream")
def stream():
    chat_id = request.args.get("chat_id")
    msg_id = request.args.get("msg_id")
    exp = request.args.get("exp")

    if not chat_id or not msg_id or not exp:
        return "Missing parameters", 400

    msg_id = int(msg_id)
    exp = int(exp)

    if time.time() > exp:
        return "⏰ Link expired", 403

    try:
        msg = tg.get_messages(chat_id, msg_id)
    except Exception as e:
        return f"❌ Error fetching message: {e}", 404

    file = msg.document or msg.video or msg.audio
    if not file:
        return "❌ No file found", 404

    # Generator to stream the file in chunks
    def file_generator():
        offset = 0
        total_size = file.file_size

        while offset < total_size:
            # Download chunk from Telegram
            chunk = tg.download_media(
                file,
                file_name=None,  # Don't save to disk
                in_memory=True,
                progress=lambda d, t: None,
                part_offset=offset,
                part_size=CHUNK_SIZE
            )
            yield chunk
            offset += CHUNK_SIZE

    return Response(
        file_generator(),
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f'inline; filename="{file.file_name}"'}
    )

if __name__ == "__main__":
    # Koyeb uses environment variable PORT
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    
