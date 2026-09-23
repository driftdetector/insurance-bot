import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render port keep-alive server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running Perfectly!")

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"HTTP Server listening on port {port}")
    server.serve_forever()

# Telegram Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Ageas Federal BI Bot active hai. Data bhej kar quotation le sakte hain.")

def main():
    # Start web server in background thread for Render
    threading.Thread(target=run_http_server, daemon=True).start()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable nahi mila!")
        return

    print("Telegram Bot start ho raha hai...")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    
    # Run bot polling
    app.run_polling()

if __name__ == "__main__":
    main()

