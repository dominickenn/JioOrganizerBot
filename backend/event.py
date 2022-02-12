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
            logging.info(f"Successfuly added \'{date}\' to \'{eventname}\'")
        except:
            logging.error(f"Failed to add \'{date}\' to \'{eventname}\'")

    def addLocation(self, location) -> None:
        try:
            bisect.insort(self.locations, location)
            logging.info(f"Successfuly added \'{location}\' to \'{eventname}\'")
        except:
            logging.error(f"Failed to add \'{location}\' to \'{eventname}\'")

    def deleteDate(self, index) -> None:
        try:
            del self.dates[index]
            logging.info(f"Successfuly deleted \'{dates[index]}\' from \'{eventname}\'")
        except:
            logging.error(f"Failed to delete \'{dates[index]}\' from \'{eventname}\'")

    def deleteLocation(self, index) -> None:
        try:
            del self.locations[index]
            logging.info(f"Successfuly deleted \'{location[index]}\' from \'{eventname}\'")
        except:
            logging.error(f"Failed to delete \'{location[index]}\' from \'{eventname}\'")