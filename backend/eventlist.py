from backend.event import Event
import logging

class EventList:
    
    def __init__(self) -> None:
        self.events = []
        self.eventNames = []

    def createEvent(self, eventname) -> None:
        try:
            self.events.append(Event(eventname))
            self.eventNames.append(eventname)
            logging.info(f"Successfuly created event \'{eventname}\'")
        except:
            logging.error(f"Failed to create event \'{eventname}\'")

    def getEventList(self) -> list:
        try:
            return self.eventNames
        except:
            logging.error(f"Failed to retrieve event list")

    def getEventDates(self, index) -> list:
        return self.events[index].getDates()

    def getEventLocations(self, index) -> list:
        return self.events[index].getLocations()

    def getEventName(self, index) -> str:
        return self.eventNames[index]

    def deleteEvent(self, index) -> None:
        try:
            del self.events[index]
            del self.eventNames[index]
            logging.info(f"Successfuly deleted event \'{self.eventNames[index]}\'")
        except:
            logging.error(f"Failed to delete event {self.eventNames[index]}")

    def addDateToEvent(self, event_index, date) -> None:
        self.events[event_index].addDate(date)

    def addLocationToEvent(self, event_index, location) -> None:
        self.events[event_index].addDate(location)

    def deleteDateFromEvent(self, event_index, date) -> None:
        self.events[event_index].deleteDate(date)

    def deleteLocationFromEvent(self, event_index, location) -> None:
        self.events[event_index].deleteDate(location)