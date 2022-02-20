class SessionManager:
    def __init__(self) -> None:
        sessions = {}

    def addSession(self, chat_id: str) -> None:
        if chat_id not in self.sessions.keys():
            self.sessions[chat_id] = -1
    
    def getSessionEventID(self, chat_id: str) -> int:
        return self.sessions[chat_id]

    def editSessionEventID(self, chat_id: str, event_id: int) -> None:
        self.sessions[chat_id] = event_id

    def resetSessionEventID(self, chat_id: str) -> None:
        self.sessions[chat_id] = -1