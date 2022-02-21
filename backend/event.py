import bisect
#bisect is the optimal method for inserting into sorted list

class Event:

    def __init__(self, eventname: str) -> None:
        self.eventname = eventname
        self.dates = []
        self.locations = []

    def getEventName(self) -> str:
        return self.eventname

    def getDates(self) -> list:
        return self.dates

    def getLocations(self) -> list:
        return self.locations

    def addDate(self, date: str) -> None:
        bisect.insort(self.dates, date)

    def addLocation(self, location: str) -> None:
        bisect.insort(self.locations, location)

    def deleteDate(self, index: int) -> None:
        del self.dates[index]

    def deleteLocation(self, index: int) -> None:
        del self.locations[index]
    
    def stringify(self) -> str:
        result = f"<b>Event:</b>{self.eventname}"
        result += "\n<b>Dates:</b>"
        for date in self.dates:
            result += f"       {date}\n"
        result += "<b>Locations:</b>" 
        for location in self.locations:
            result += f"           {location}\n"
        return result