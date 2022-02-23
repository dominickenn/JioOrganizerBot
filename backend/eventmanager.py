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

    def getEventList(self, chat_id: str) -> list:
        eventlist = self.events[chat_id]
        eventnames = [event.getEventName() for event in eventlist]
        return eventnames

    def getEventName(self, chat_id: str, event_index: int) -> str:
        return self.events[chat_id][event_index].getEventName()

    def deleteEvent(self, chat_id: str, event_index: int) -> None:
        del self.events[chat_id][event_index]
        Logger.logSuccessfulOperation(f"deleted event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def addDateToEvent(self, chat_id: str, event_index: int, date: str) -> None:
        self.events[chat_id][event_index].addDate(date)
        Logger.logSuccessfulOperation(f"added date \'{date}\' to event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def addLocationToEvent(self, chat_id: str, event_index: int, location: str) -> None:
        self.events[chat_id][event_index].addLocation(location)
        Logger.logSuccessfulOperation(f"added location \'{location}\' to event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def deleteDateFromEvent(self, chat_id: str, event_index: int, index: int) -> None:
        self.events[chat_id][event_index].deleteDate(int(index) - 1)
        Logger.logSuccessfulOperation(f"deleted date index \'{index}\' from event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def deleteLocationFromEvent(self, chat_id: str, event_index: int, index: int) -> None:
        self.events[chat_id][event_index].deleteLocation(int(index) - 1)
        Logger.logSuccessfulOperation(f"deleted location index \'{index}\' from event \'{self.getEventName(chat_id, event_index)}\' for \'{chat_id}\'")

    def getLatestEventIndex(self, chat_id: str) -> int:
        return len(self.events[chat_id]) - 1

    def getEventString(self, chat_id: str, event_index: int) -> str:
        return self.events[chat_id][event_index].stringify()

    def getEventInfo(self, chat_id: str, event_index: int) -> tuple:
        return self.events[chat_id][event_index].getEventInfo()