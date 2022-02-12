import bisect
#bisect is the optimal method for inserting into sorted list

class Event:
    def __init__(self, eventname) -> None:
        self.eventname = eventname
        self.dates = []
        self.locations = []

    def addDate(self, date) -> None:
        bisect.insort(self.dates, date)

    def addLocation(self, location) -> None:
        bisect.insort(self.locations, location)

    def deleteDate(self, index) -> None:
        del self.dates[index]

    def deleteLocation(self, index) -> None:
        del self.locations[index]