#import bisect
#bisect is the optimal method for inserting into sorted list

class Event:

    def __init__(self, eventname: str) -> None:
        self.eventname = eventname
        self.dates = []
        self.locations = []

    def getEventName(self) -> str:
        return self.eventname

    def getEventInfo(self) -> tuple:
        return self.eventname, self.dates, self.locations

    def addDate(self, date: str) -> None:
        #bisect.insort(self.dates, date)
        self.dates.append(date)

    def addLocation(self, location: str) -> None:
        #bisect.insort(self.locations, location)
        self.locations.append(location)

    def deleteDate(self, index: int) -> None:
        del self.dates[index]

    def deleteLocation(self, index: int) -> None:
        del self.locations[index]
    
    def stringify(self) -> str:
        result = f"<u>Event:</u>\n{self.eventname}\n"
        result += "\n<u>Dates:</u>"
        for date in self.dates:
            result += f"\n{date}"
        result += "\n\n<u>Locations:</u>"
        for location in self.locations:
            result += f"\n{location}"
        return result

    def canCreatePoll(self) -> bool:
        return len(self.dates) > 0 and len(self.locations) > 0