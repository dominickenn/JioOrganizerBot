from logger import Logger
from handler.handlerstates import States as states
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

class Dispatcher:

    def sendEntryPointInlineKeyboard(self, update: Update, context: CallbackContext, chat_id: str) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Create Event", callback_data=states.CREATE_EVENT),
                InlineKeyboardButton("Edit Event", callback_data=states.EDIT_EVENT_LIST),
            ],
            [
                InlineKeyboardButton("Setup Poll", callback_data=states.SETUP_EVENT_POLL),
                InlineKeyboardButton("Delete Event", callback_data=states.DELETE_EVENT_LIST),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=chat_id,
            text='Hi! I am your local jio bot! \nPress any button below to start!', 
            reply_markup=reply_markup
        )
        Logger.logMessageDispatch("Entry-point inline keyboard", chat_id)

    def sendEventNameRequest(self, update: Update, context: CallbackContext, chat_id: str, message_id: str) -> None:
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Send me your event name in the following format: /eventname \'eventname\'\ne.g. /eventname Dinner on the 15th")
        Logger.logMessageDispatch("Event name request for create event", chat_id)

    def sendEditEventInlineKeyboard(self, update: Update, context: CallbackContext, chat_id: str, message_id: str, event: str) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Done", callback_data=-1),
                InlineKeyboardButton("Create Poll", callback_data=-1),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{event}\n\n<b>To edit the event, use the follow commands:</b>\n    - /adddate \'date\'\n    - /addlocation \'location\'\n    - /deletedate \'date_index\'\n    - /deletelocation \'location_index\'", 
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        Logger.logMessageDispatch("Edit-event inline keyboard", chat_id)

    def deleteLatestUserMessage(self, update: Update, context: CallbackContext, chat_id: str, message_id: str):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        Logger.logMessageDeletion(update.message.text, chat_id)

    def sendInputNotRecognized(self, update: Update, context: CallbackContext, chat_id: str) -> None:
        context.bot.send_message(chat_id=chat_id, text="Input not recognized, please /jio to start again!")