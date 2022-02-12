import bisect
import logging
#bisect is the optimal method for inserting into sorted list

class Event:

    def __init__(self, eventname) -> None:
        self.eventname = eventname
        self.dates = []
        self.locations = []

    def addDate(self, date) -> None:
        try:
            bisect.insort(self.dates, date)
            logging.info(f"Successfuly added \'{date}\' to \'{self.eventname}\'")
        except:
            logging.error(f"Failed to add \'{date}\' to \'{self.eventname}\'")

    def addLocation(self, location) -> None:
        try:
            bisect.insort(self.locations, location)
            logging.info(f"Successfuly added \'{location}\' to \'{self.eventname}\'")
        except:
            logging.error(f"Failed to add \'{location}\' to \'{self.eventname}\'")

    def deleteDate(self, index) -> None:
        try:
            del self.dates[index]
            logging.info(f"Successfuly deleted \'{self.dates[index]}\' from \'{self.eventname}\'")
        except:
            logging.error(f"Failed to delete \'{self.dates[index]}\' from \'{self.eventname}\'")

    def deleteLocation(self, index) -> None:
        try:
            del self.locations[index]
            logging.info(f"Successfuly deleted \'{self.location[index]}\' from \'{self.eventname}\'")
        except:
            logging.error(f"Failed to delete \'{self.location[index]}\' from \'{self.eventname}\'")