from logger import Logger
from handler.handlerstates import States as states
from frontend.dispatcher import Dispatcher
from backend.eventmanager import EventManager
from handler.sessionmanager import SessionManager
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, PollAnswerHandler

class Handler:
    def __init__(self) -> None:
        self.handler = ConversationHandler(
            entry_points=[CommandHandler('jio', self.entryPointHandling)],
            states={
                states.ENTRY_POINT: [CallbackQueryHandler(self. entryPointButtonHandling)],
                states.CREATE_EVENT: [CommandHandler('eventname', self.createEventHandling)],
                states.EDIT_EVENT_LIST:[CallbackQueryHandler(self. editEventListButtonHandling)],
                states.POLLING:[CallbackQueryHandler(self. pollingButtonHandling)],
                states.EDIT_EVENT: [
                    CallbackQueryHandler(self.editEventButtonHandling),
                    CommandHandler('adddate', self.editEventHandling),
                    CommandHandler('addlocation', self.editEventHandling),
                    CommandHandler('deletedate', self.editEventHandling),
                    CommandHandler('deletelocation', self.editEventHandling)],
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
        self.dispatcher.deleteLatestUserMessage(update, context, chat_id)
        self.dispatcher.sendEntryPointInlineKeyboard(update, context, chat_id)
        self.sessionManager.addSession(chat_id)
        return states.ENTRY_POINT

    def entryPointButtonHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: Entry-point button press
        Dispatch: Handled according to button press
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
            case states.EDIT_EVENT_LIST:
                self.dispatcher.sendEventList(update, context, chat_id, message_id, self.eventManager.getFiveLatestEventList(chat_id))
            case states.POLLING:
                self.dispatcher.sendEventList(update, context, chat_id, message_id, self.eventManager.getFiveLatestEventList(chat_id))
            case states.DONE:
                self.dispatcher.deleteLatestBotMessage(update, context, chat_id, message_id)
                self.sessionManager.resetSession(chat_id)
                return ConversationHandler.END
        return new_state

    def createEventHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: /eventname "eventname"
        Dispatch: EditEvent buttons
        Backend: Create new empty event 'eventname'
        Session: Edit chat_id session to latest event index
        '''        
        eventname_array = update.message.text.split(" ", 1)
        chat_id = update.effective_chat.id
        message_id = self.sessionManager.getInlineKeyboardMessageID(chat_id)
        if len(eventname_array) < 2:
            self.dispatcher.deleteLatestUserMessage(update, context, chat_id)
            return states.CREATE_EVENT
        eventname = eventname_array[1]
        Logger.logMessageReceived(update.message.text, chat_id)
        self.eventManager.createEvent(chat_id, eventname)
        self.dispatcher.deleteLatestUserMessage(update, context, chat_id)
        event_id = self.eventManager.getLatestEventIndex(chat_id)
        self.dispatcher.sendEditEventInlineKeyboard(update, context, chat_id, message_id, self.eventManager.getEventString(chat_id, event_id))
        self.sessionManager.setSessionEventID(chat_id, event_id)
        return states.EDIT_EVENT

    def editEventListButtonHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: Event button press
        Dispatch: Handled according to button press
        '''
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query = update.callback_query
        query.answer()
        selected_event = int(query.data)
        chat_id = update.effective_chat.id
        message_id = update.callback_query.message.message_id
        Logger.buttonPressReceived(selected_event, chat_id)
        self.sessionManager.setInlineKeyboardMessageID(chat_id, message_id)
        self.sessionManager.setSessionEventID(chat_id, selected_event)
        self.dispatcher.sendEditEventInlineKeyboard(update, context, chat_id, message_id, self.eventManager.getEventString(chat_id, selected_event))
        return states.EDIT_EVENT

    def pollingButtonHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: Event button press
        Dispatch: Handled according to button press
        '''
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query = update.callback_query
        query.answer()
        selected_event = int(query.data)
        chat_id = update.effective_chat.id
        message_id = update.callback_query.message.message_id
        Logger.buttonPressReceived(selected_event, chat_id)
        self.dispatcher.deleteLatestBotMessage(update, context, chat_id, message_id)
        self.dispatcher.sendEventPoll(update, context, chat_id, *self.eventManager.getEventInfo(chat_id, self.sessionManager.getSessionEventID(chat_id)))
        self.sessionManager.resetSession(chat_id)
        return ConversationHandler.END

    def editEventHandling(self, update: Update, context: CallbackContext) -> str:
        '''
        Update: /adddate "date" OR /addlocation "location" OR /deletedate OR /deletelocation
        Dispatch: EditEvent buttons and New Event Updates
        Backend: AddDate/AddLocation/DeleteDate/DeleteLocation
        '''
        message_array = update.message.text.split(" ", 1)
        chat_id = update.effective_chat.id
        message_id = self.sessionManager.getInlineKeyboardMessageID(chat_id)
        if len(message_array) < 2:
            self.dispatcher.deleteLatestUserMessage(update, context, chat_id)
            return states.EDIT_EVENT
        command = message_array[0]
        message = message_array[1]
        event_id = self.sessionManager.getSessionEventID(chat_id)
        Logger.logMessageReceived(update.message.text, chat_id)
        match command:
            case "/adddate":
                self.eventManager.addDateToEvent(chat_id, event_id, message)
            case "/addlocation":
                self.eventManager.addLocationToEvent(chat_id, event_id, message)
            case "/deletedate":
                self.eventManager.deleteDateFromEvent(chat_id, event_id, message)
            case "/deletelocation":
                self.eventManager.deleteLocationFromEvent(chat_id, event_id, message)
        self.dispatcher.sendEditEventInlineKeyboard(update, context, chat_id, message_id, self.eventManager.getEventString(chat_id, event_id))
        self.dispatcher.deleteLatestUserMessage(update, context, chat_id)
        return states.EDIT_EVENT

    def editEventButtonHandling(self, update: Update, context: CallbackContext) -> str:
            '''
            Update: Edit event button press
            Dispatch: Handled according to button press
            '''
            # CallbackQueries need to be answered, even if no notification to the user is needed
            # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
            query = update.callback_query
            query.answer()
            new_state = query.data
            chat_id = update.effective_chat.id
            message_id = update.callback_query.message.message_id
            event_index = self.sessionManager.getSessionEventID(chat_id)
            Logger.buttonPressReceived(new_state, chat_id)
            # Handling of button presses based on transition to new state
            if new_state == states.POLLING:
                if self.eventManager.canEventCreatePoll(chat_id, event_index):
                    self.dispatcher.sendEventPoll(update, context, chat_id, *self.eventManager.getEventInfo(chat_id, event_index))
                else:
                    self.dispatcher.sendEditEventInlineKeyboard(update, context, chat_id, message_id, self.eventManager.getEventString(chat_id, event_index), error=True)
                    return states.EDIT_EVENT
            self.dispatcher.deleteLatestBotMessage(update, context, chat_id, message_id)           
            self.sessionManager.resetSession(chat_id)
            return ConversationHandler.END
    
    def cancelCommandHandling(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat.id
        Logger.logMessageReceived(f"{update.messsage.text}", chat_id)
        self.dispatcher.sendInputNotRecognized(update, context, chat_id)