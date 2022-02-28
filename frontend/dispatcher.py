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
                InlineKeyboardButton("Setup Poll", callback_data=states.POLLING),
                InlineKeyboardButton("Done", callback_data=states.DONE),
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

    def sendEditEventInlineKeyboard(self, update: Update, context: CallbackContext, chat_id: str, message_id: str, event: str, error: bool=False) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Done", callback_data=states.DONE),
                InlineKeyboardButton("Create Poll", callback_data=states.POLLING),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"{event}\n\n<b>To edit the event, use the follow commands:</b>\n    - /adddate \'date\'\n    - /addlocation \'location\'\n    - /deletedate \'date_index\'\n    - /deletelocation \'location_index\'\n      <i>Indices start from 1.</i>"
        if error:
            text += "\n\n<b>There must be at least 1 date and 1 location for a poll!</b>"
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text, 
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        Logger.logMessageDispatch("Edit-event inline keyboard", chat_id)
    
    def sendEventPoll(self, update: Update, context: CallbackContext, chat_id: str, event_name: str, event_dates: list, event_locations: list) -> None:
        options = []
        for date in event_dates:
            for location in event_locations:
                options.append(f"{location} on {date}")
        question = f"Make your vote for {event_name}!"
        if len(options) == 0:
            context.bot.send_message(
                chat_id=chat_id,
                text="There must be at least 1 date and 1 location for a poll!"
            )
            Logger.logMessageDispatch(f"Insufficient options for poll", chat_id)
        elif len(options) == 1:
            question = f"Make your vote for {event_name}!\n{options[0]}"
            options = ["Yes", "No", "Maybe"]
            context.bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=True
            )
            Logger.logMessageDispatch(f"Poll for {event_name}", chat_id)
        else:
            context.bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=True
            )
            Logger.logMessageDispatch(f"Poll for {event_name}", chat_id)

    def sendEventList(self, update: Update, context: CallbackContext, chat_id: str, message_id: str, event_list: list) -> None:
        keyboard = []
        for i in range(len(event_list)):
            keyboard.append([InlineKeyboardButton(f"{event_list[i]}", callback_data=i)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if len(keyboard) == 0:
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"These are no events!", 
            )
            Logger.logMessageDispatch("No events", chat_id)
        else:
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"These are the latest 5 events!\nChoose an event!", 
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            Logger.logMessageDispatch("Latest 5 event list", chat_id)

    def deleteLatestBotMessage(self, update: Update, context: CallbackContext, chat_id: str, message_id: str) -> None:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        Logger.logBotConversationEnd(chat_id)

    def deleteLatestUserMessage(self, update: Update, context: CallbackContext, chat_id: str) -> None:
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        Logger.logMessageDeletion(update.message.text, chat_id)

    def sendInputNotRecognized(self, update: Update, context: CallbackContext, chat_id: str) -> None:
        context.bot.send_message(chat_id=chat_id, text="Input not recognized, please /jio to start again!")