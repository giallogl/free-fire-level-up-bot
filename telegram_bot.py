import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Get configuration from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_UID = os.getenv("BOT_UID")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file!")

# Import the Free Fire client
from app import FF_CLIENT

class TelegramFFBot:
    def __init__(self):
        self.ff_client = None
        self.user_id = BOT_UID
        self.user_password = BOT_PASSWORD
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        message = f"""
🎮 **مرحباً {user.first_name}!**

أنا بوت Free Fire للرفع السريع! 🚀

**الأوامر المتاحة:**
/help - اعرض جميع الأوامر
/status - حالة البوت
/connect - اتصل بحسابك
/disconnect - قطع الاتصال
        """
        await update.message.reply_text(message, parse_mode="Markdown")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = """
**📋 قائمة الأوامر:**

/start - ابدأ البوت
/help - اعرض المساعدة
/status - حالة الاتصال
/connect - اتصل بـ Free Fire
/disconnect - قطع الاتصال
/info - معلومات حسابك

**💬 أرسل أي رسالة لتفاعل البوت معك!**
        """
        await update.message.reply_text(message, parse_mode="Markdown")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        status = "✅ البوت يعمل بنجاح!" if self.ff_client else "❌ البوت غير متصل"
        await update.message.reply_text(f"**حالة البوت:** {status}", parse_mode="Markdown")
    
    async def connect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /connect command"""
        await update.message.reply_text("🔄 جاري الاتصال بـ Free Fire...")
        
        try:
            # Here you would connect to Free Fire
            await update.message.reply_text("✅ تم الاتصال بنجاح!")
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ في الاتصال: {str(e)}")
    
    async def disconnect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /disconnect command"""
        await update.message.reply_text("🔌 تم قطع الاتصال")
    
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        info_message = f"""
**ℹ️ معلومات حسابك:**

🆔 UID: `{self.user_id}`
👤 اسم المستخدم: `AURA.lfassi`
🎮 اللعبة: Free Fire

**الحالة:** ✅ جاهز
        """
        await update.message.reply_text(info_message, parse_mode="Markdown")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        text = update.message.text
        
        if "مرحبا" in text.lower() or "hi" in text.lower():
            await update.message.reply_text("👋 مرحباً! كيفك أنت؟")
        
        elif "شنو" in text.lower() or "what" in text.lower():
            await update.message.reply_text("📱 أنا بوت Free Fire! استعمل /help للأوامر")
        
        else:
            await update.message.reply_text("✅ استقبلت رسالتك! اكتب /help للمساعدة")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"Update {update} caused error {context.error}")

async def main():
    """Start the bot"""
    print("🚀 بدء البوت...")
    
    # Create bot instance
    bot = TelegramFFBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("status", bot.status))
    application.add_handler(CommandHandler("connect", bot.connect))
    application.add_handler(CommandHandler("disconnect", bot.disconnect))
    application.add_handler(CommandHandler("info", bot.info))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    print("✅ البوت جاهز! استقبال الرسائل...")
    
    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
