from backend.event import Event
from logger import Logger

class EventManager:
    
    def __init__(self) -> None:
        '''
        Dictionary
        Key: update.message.chat_id
        Value: list of events
        '''
        self.events = {}

    def createEvent(self, chat_id: str, eventname: str) -> None:
        if chat_id not in self.events.keys():
            self.events[chat_id] = []
        self.events[chat_id].append(Event(eventname))
        Logger.logSuccessfulOperation(f"created event \'{eventname}\' for \'{chat_id}\'")

    def getFiveLatestEventList(self, chat_id: str) -> list:
        if chat_id not in self.events.keys():
            return []
        eventlist = self.events[chat_id]
        n_events = len(eventlist)
        eventnames = [(eventlist[i].getEventName(), i) for i in range(n_events - 5, n_events)]
        return eventnames

    def getEventName(self, chat_id: str, event_index: int) -> str:
        return self.events[chat_id][event_index].getEventName()

    def addDateToEvent(self, chat_id: str, event_index: int, date: str) -> None:
        self.events[chat_id][event_index].addDate(date)
        Logger.logSuccessfulOperation(f"added date \'{date}\' to event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def addLocationToEvent(self, chat_id: str, event_index: int, location: str) -> None:
        self.events[chat_id][event_index].addLocation(location)
        Logger.logSuccessfulOperation(f"added location \'{location}\' to event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def deleteDateFromEvent(self, chat_id: str, event_index: int, index: int) -> None:
        index = int(index) - 1
        if isinstance(index, int):
            self.events[chat_id][event_index].deleteDate(index)
            Logger.logSuccessfulOperation(f"deleted date index \'{index}\' from event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def deleteLocationFromEvent(self, chat_id: str, event_index: int, index: int) -> None:
        index = int(index) - 1
        if isinstance(index, int):
            self.events[chat_id][event_index].deleteLocation(index)
            Logger.logSuccessfulOperation(f"deleted location index \'{index}\' from event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def getLatestEventIndex(self, chat_id: str) -> int:
        return len(self.events[chat_id]) - 1

    def getEventString(self, chat_id: str, event_index: int) -> str:
        return self.events[chat_id][event_index].stringify()

    def getEventInfo(self, chat_id: str, event_index: int) -> tuple:
        return self.events[chat_id][event_index].getEventInfo()

    def canEventCreatePoll(self, chat_id: str, event_index: int) -> bool:
        return self.events[chat_id][event_index].canCreatePoll()