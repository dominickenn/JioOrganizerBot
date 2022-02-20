from logger import Logger
from handler.handlerstates import States as states
from frontend.dispatcher import Dispatcher
from backend.eventmanager import EventManager
from handler.sessionmanager import SessionManager
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler

class Handler:
    def __init__(self) -> None:
        self.handler = ConversationHandler(
            entry_points=[CommandHandler('jio', self.entryPointHandling)],
            states={
                states.ENTRY_POINT: [CallbackQueryHandler(self.buttonHandling)],
                states.CREATE_EVENT: [CommandHandler('eventname', self.createEventHandling)],
                states.EDIT_EVENT: [CallbackQueryHandler(self.buttonHandling)],
            },
            fallbacks=[CommandHandler('cancel', self.cancelCommandHandling)],
        )
        self.dispatcher = Dispatcher();
        self.eventManager = EventManager();
        self.sessionManager = SessionManager();

    def getHandler(self) -> ConversationHandler:
        return self.handler

    def entryPointHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: /jio command
        Dispatch: Entry point inline keyboard
        Session: Add chat_id/reset session
        '''
        chat_id = update.effective_chat.id
        Logger.logMessageReceived(f"{update.message.text}", chat_id)
        self.dispatcher.sendEntryPointInlineKeyboard(update, context, chat_id)
        self.sessionManager.addSession(chat_id)
        return states.ENTRY_POINT

    def buttonHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: Button press
        Dispatch: Handled according to button press
        State-Update: According to button press
        '''
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query = update.callback_query
        query.answer()
        new_state = query.data
        chat_id = update.effective_chat.id
        message_id = update.callback_query.message.message_id
        Logger.buttonPressReceived(new_state, chat_id)
        self.sessionManager.setInlineKeyboardMessageID(chat_id, message_id)

        # Handling of button presses based on transition to new state
        match new_state:
            case states.CREATE_EVENT:
                self.dispatcher.sendEventNameRequest(update, context, chat_id, message_id)
                #TODO add edit_event button handling (ADD DATE, ADD LOCATION, DELETE DATE, DELETE LOCATION, DONE, CREATE POLL
                #https://stackoverflow.com/questions/55201953/telegram-bot-api-edit-inlinekeyboard-with-python-telegram-bot-not-working
            case states.ADD_DATES:
                pass
                

        return new_state

    def createEventHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: /eventname "eventname"
        Dispatch: EditEvent buttons
        Backend: Create new empty event 'eventname'
        Session: Edit chat_id session to latest event index
        '''
        eventname = update.message.text.split(" ", 1)[1]
        chat_id = update.effective_chat.id
        message_id = update.callback_query.message.message_id
        Logger.logMessageReceived(f"Received event name {eventname}", chat_id)
        self.eventManager.createEvent(chat_id, eventname)
        self.dispatcher.sendEditEventInlineKeyboard(update, context, chat_id, message_id, eventname)
        self.sessionManager.setSessionEventID(self.eventManager.getLatestEventIndex(chat_id))
        return states.EDIT_EVENT


    def cancelCommandHandling(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat.id
        Logger.logMessageReceived(f"{update.messsage.text}", chat_id)
        self.dispatcher.sendInputNotRecognized(update, context, chat_id)