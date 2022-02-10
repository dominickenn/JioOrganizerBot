from distutils.cmd import Command
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler
import logging

'''
Reference for converstaionhandler: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
Design: https://lucid.app/lucidchart/6330a386-4d09-4764-83df-8f9ae152d38d/edit?invitationId=inv_fe30ac88-b3b8-4bda-b97c-3e2416cac9f5
'''

TOKEN = '5100503329:AAEd2hcnal5qbvYL0BvnzCEEL-yTJebJfY0'
botusername = 'JioOrganizerBot'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
JIO, CREATE_EVENT, EDIT_EVENT, ADD_DATES, ADD_LOCATIONS, DELETE_DATES, DELETE_LOCATIONS, EDIT_EVENT_LIST, SETUP_EVENT_POLL, DELETE_EVENT = ['J', 'CE', 'EE', 'AD' ,'AL', 'DD', 'DL', 'EEL', 'SEP', 'DE']

def jio(update: Update, context: CallbackContext):
    '''
    Update: /jio command
    Dispatch: Send buttons for JioOrganizerBot main actions
    '''
    logging.info(f"received message: {update.message.text}")
    keyboard = [
        [
            InlineKeyboardButton("Create Event", callback_data=CREATE_EVENT),
            InlineKeyboardButton("Edit Event", callback_data=EDIT_EVENT_LIST),
        ],
        [
            InlineKeyboardButton("Setup Poll", callback_data=SETUP_EVENT_POLL),
            InlineKeyboardButton("Delete Event", callback_data=DELETE_EVENT),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am your local jio bot! \nPress any button below to start!', reply_markup=reply_markup)
    logging.info("dispatching JioOrganizerBot main action buttons")
    return JIO

def button(update: Update, context: CallbackContext):
    '''
    Update: Button press
    Dispatch: Send relevant message/buttons; Update interal state
    '''
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query = update.callback_query
    query.answer()
    new_state = query.data
    logging.info(f"received button press: {new_state}")
    
    # Add new case for each button
    match new_state:
        case CREATE_EVENT:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Send me your event name in the following format: /eventname \'eventname\'\ne.g. /eventname Dinner on the 15th")

    logging.info(f"Transitioning state to: {new_state}")
    return query.data

def createEvent(update: Update, context: CallbackContext):
    '''
    Update: /eventname command
    Dispatch: EditEvent buttons
    Backend: Create new empty event 'eventname'
    '''
    eventname = update.message.text.split(" ", 1)[1]
    logging.info(f"message:{eventname}")
    #TODO: CREATE IN BACKEND EVENT
    
    return EDIT_EVENT

def cancel(update: Update, context: CallbackContext):
    '''
    Update: 'cancel' commnand / unrecognized input
    Dispatch: text - "Input not recognized, please /jio to start again!"
    '''
    logging.info(f"received message: {update.message.text}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Input not recognized, please /jio to start again!")

def main():
    '''
    Starts the bot
    -   Create updater with bot's token [Updater receives updates from bot]
    -   Create dispatcher [Dispatcher sends commands to bot]
    -   Create handlers to attach to dispatcher
    '''
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('jio', jio)],
        states={
            JIO: [CallbackQueryHandler(button)],
            CREATE_EVENT: [CommandHandler('eventname', createEvent)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    #starts the bot
    updater.start_polling()
    #run bot until Ctrl + C
    updater.idle()

if __name__ == '__main__':
    main()