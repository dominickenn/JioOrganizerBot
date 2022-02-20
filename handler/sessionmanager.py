class SessionManager:
    '''
    Dictionary
    Key: chat_id
    Value: [event_index, inlinekeyboard_message_id]
    '''
    def __init__(self) -> None:
        self.sessions = {}

    def addSession(self, chat_id: str) -> None:
        if chat_id not in self.sessions.keys():
            self.sessions[chat_id] = [-1, -1]
    
    def getSessionEventID(self, chat_id: str) -> int:
        return self.sessions[chat_id][0]

    def setSessionEventID(self, chat_id: str, event_id: int) -> None:
        self.sessions[chat_id][0] = event_id

    def resetSessionEventID(self, chat_id: str) -> None:
        self.sessions[chat_id][0] = -1

    def getInlineKeyboardMessageID(self, chat_id: str) -> str:
        return self.sessions[chat_id][1]

    def setInlineKeyboardMessageID(self, chat_id: str, message_id: str) -> None:
        self.sessions[chat_id][1] = message_id

    def resetInlineKeyboardMessageID(self, chat_id: str) -> None:
        self.sessions[chat_id][1] = -1