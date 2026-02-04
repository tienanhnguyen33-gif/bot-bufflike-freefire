import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN_BOT = "8376882243:AAESOF0XBQpzqNjcALU2P5sisxK_xCMmp9k"
API_TTC = "hjbkclczkuz758dvkx1uu3d7c02mreh6w"
ADMIN_ID = "7280120249"

valid_keys = [] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot online trên Render! Không bị chặn.")

async def addkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID: return
    if context.args:
        key = context.args[0].strip()
        valid_keys.append(key)
        await update.message.reply_text(f"✅ Đã nạp Key: {key}")

async def buff_like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Cú pháp: /like UID Key")
        return
    uid, key_nhap = context.args[0].strip(), context.args[1].strip()
    if key_nhap not in valid_keys:
        await update.message.reply_text("❌ Key sai!")
        return
    await update.message.reply_text(f"⏳ Đang xử lý UID: {uid}...")
    url = f"https://api.tuongtaccheo.com/api/freefire/?access_token={API_TTC}&id={uid}"
    try:
        response = requests.get(url, timeout=30)
        res = response.json()
        if "mess" in res:
            await update.message.reply_text(f"📩 TTC báo: {res['mess']}")
            if "thành công" in res['mess'].lower(): valid_keys.remove(key_nhap)
    except:
        await update.message.reply_text("❌ Lỗi kết nối server.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addkey", addkey))
    app.add_handler(CommandHandler("like", buff_like))
    app.run_polling()
