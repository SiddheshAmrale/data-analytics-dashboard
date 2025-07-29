import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import paypalrestsdk

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# PayPal configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "YOUR_PAYPAL_CLIENT_ID",
    "client_secret": "YOUR_PAYPAL_CLIENT_SECRET"
})

# Telegram bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
PRIVATE_GROUP_ID = 'YOUR_PRIVATE_GROUP_ID'

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Pay $30", callback_data='pay')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Click the button below to make a payment of $30.', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'pay':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute",
                "cancel_url": "http://localhost:8000/payment/cancel"
            },
            "transactions": [{
                "amount": {
                    "total": "30.00",
                    "currency": "USD"
                },
                "description": "Payment for access to private Telegram group"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    query.edit_message_text(text=f"Please make the payment by clicking [here]({approval_url}).", parse_mode='Markdown')
        else:
            query.edit_message_text(text="An error occurred while creating the payment. Please try again later.")

def payment_success(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    context.bot.add_chat_members(chat_id=PRIVATE_GROUP_ID, user_ids=[user_id])
    update.message.reply_text("Payment successful! You have been added to the private group.")

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("payment_success", payment_success))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()