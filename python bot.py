import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN_BOT = "8376882243:AAESOF0XBQpzqNjcALU2P5sisxK_xCMmp9k"
API_TTC = "hjbkclczkuz758dvkx1uu3d7c02mreh6w"
ADMIN_ID = "7280120249"

valid_keys = [] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot online trên Render! Hãy nạp key rồi buff like nhé.")

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
        await update.message.reply_text("❌ Key sai hoặc không tồn tại!")
        return

    await update.message.reply_text(f"⏳ Đang gửi yêu cầu cho UID: {uid}...")

    # Cấu hình lại link chuẩn nhất của TTC và thêm Headers để tránh bị chặn
    url = f"https://tuongtaccheo.com/api/freefire/index.php?access_token={API_TTC}&id={uid}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        # Kiểm tra nếu web phản hồi lỗi
        if response.status_code != 200:
            await update.message.reply_text(f"❌ Web TTC từ chối kết nối (Lỗi {response.status_code})")
            return

        res = response.json()
        if "mess" in res:
            await update.message.reply_text(f"📩 Kết quả: {res['mess']}")
            if "thành công" in res['mess'].lower():
                valid_keys.remove(key_nhap)
        else:
            await update.message.reply_text("❓ Không nhận được phản hồi hợp lệ từ TTC.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addkey", addkey))
    app.add_handler(CommandHandler("like", buff_like))
    app.run_polling()

