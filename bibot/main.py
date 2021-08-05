from bibot.entities.config import Config
from bibot.handler.browserHandler import SeleniumSession
from datetime import date 

# TODO: Logging
if __name__ == "__main__":
    config = Config("Username", "Password")

    session = SeleniumSession()

    now = date.today()
    session.setup()
    session.authenticate(config.username, config.password)
    scan = session.getDay(config.days[0])

    available_days = scan.getAvailableDays() # e.g [date.today()]
    available_timeslotw = scan.getAvailableTimeslots() # e.g ["vormittags", "nachmittags", ...]
    available_rooms = scan.getAvailableRooms() # e.g ["1.OG KIT-BIB (LSW)", "2.OG KIT-BIB (LST)", "3.OG KIT-BIB (LSG)"]

    # Order can be changed
    sliced_scan = scan.getFromDays([date.today()]).getFromTimeslots(["vormittags", "nachmittags"]).getFromRooms(["3.OG KIT-BIB (LSG)"])

    free_places = sliced_scan.getFreePlaces()
    free_places[0].reserve()

    session.teardown()

