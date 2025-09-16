from flask import Flask, request, send_file
from pyrogram import Client
import os, io, time

app = Flask(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

tg = Client("tg_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
tg.start()

@app.route("/stream")
def stream():
    chat_id = request.args.get("chat_id")
    msg_id = request.args.get("msg_id")
    exp = request.args.get("exp")

    if not chat_id or not msg_id or not exp:
        return "Missing parameters", 400

    msg_id = int(msg_id)
    exp = int(exp)

    if time.time() > exp:  # time in seconds
        return "⏰ Link expired", 403

    msg = tg.get_messages(chat_id, msg_id)
    file = msg.document or msg.video or msg.audio
    if not file:
        return "❌ No file", 404

    buf = io.BytesIO()
    tg.download_media(file, file_name=buf)
    buf.seek(0)

    return send_file(
        buf,
        as_attachment=False,
        download_name=file.file_name or "file"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
