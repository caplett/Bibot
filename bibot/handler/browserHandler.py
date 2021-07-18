# Generated by Selenium IDE
import logging
from datetime import date, timedelta
from bibot.entities.models import (
    DayModel,
    RoomModel,
    TimeslotModel,
    SeatModel,
)
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumSession:
    def setup(self):
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year=2021&month=07&day=11&area=20&room=140"
        )
        self.driver.find_element(By.LINK_TEXT, "gehe zum heutigen Tag").click()

    def teardown(self):
        self.driver.quit()

    def authenticate(self, user, password) -> bool:
        self.driver.find_element(
            By.CSS_SELECTOR, "form:nth-child(2) input:nth-child(3)"
        ).click()
        self.driver.find_element(By.ID, "NewUserName").send_keys(user)
        self.driver.find_element(By.ID, "NewUserPassword").send_keys(password)
        self.driver.find_element(By.ID, "EULA_INPUT").click()
        self.driver.find_element(By.CSS_SELECTOR, ".submit").click()

        try:
            self.driver.find_element_by_link_text("Unbekannter Benutzer")
            logging.error("Login did not work with given credentials")
            return False
        except NoSuchElementException:
            logging.info("Login worked")
            return True

    def isAuthenticated(self) -> bool:
        self.goTodayPage()
        try:
            self.driver.find_element_by_link_text("Unbekannter Benutzer")
            logging.info("Not logged in")
            return False
        except NoSuchElementException:
            logging.info("Still logged in")
            return True

    def goTodayPage(self):
        logging.debug("Go to Today page")
        self.goToDate(date.today())

    def goToDate(self, date):
        self.driver.get(
            f"https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year={date.year}&month={date.month}&day={date.day}&area=20&room=140"
        )

    def getDay(self, date):
        self.goToDate(date)
        rooms = self.handleRooms()
        return rooms

    def getDays(self, fromDate, toDate):
        range = self.getDateRange(fromDate, toDate)
        days = [self.getDay(x) for x in range]
        return days

    def getAvailableRooms(self):
        logging.debug("Getting Available Rooms from website")
        self.driver.find_element(By.LINK_TEXT, "gehe zum heutigen Tag").click()
        elements = self.driver.find_elements_by_xpath("//div[@id='dwm_areas']/ul/li")
        rooms = [
            Room(x.find_element_by_xpath("a").get_attribute("href"), x.text)
            for x in elements
        ]

        logging.debug("Found the following available Rooms:")
        for x in rooms:
            logging.debug(x.roomName)
        return rooms

    def getAvailableTimeSlots(self, room):
        self.driver.get(room.url)
        time_slots = self.driver.find_elements_by_xpath(
            "//table[@id='day_main']/tbody/tr"
        )
        return time_slots

    def getAvailableSeats(self, timeslot):
        seats = [x for x in timeslot.find_elements_by_xpath("td")]
        return seats

    def handleRooms(self):
        available_rooms = self.getAvailableRooms()
        rooms = [self.handleRoom(x) for x in available_rooms]

        return rooms

    def handleRoom(self, availableRoom):
        available_timeslots = self.getAvailableTimeSlots(availableRoom)
        time_slots = [self.handleTimeSlot(x) for x in available_timeslots]

        availableRoom.time_slots = time_slots
        return availableRoom

    def handleTimeSlot(self, timeslot):
        row_names = self.driver.find_elements_by_xpath(
            "//table[@id='day_main']/thead[1]/tr/th"
        )
        available_seats = self.getAvailableSeats(timeslot)
        assert len(row_names) == len(available_seats)

        seats = []
        for i in range(1, len(available_seats)):
            # Catch except block to catch the different
            # setup on the website if a seat
            # is reseverd. This leads to a second "div" block
            try:
                url = (
                    available_seats[i]
                    .find_element_by_xpath("div")
                    .find_element_by_xpath("a")
                    .get_attribute("href")
                )
            except NoSuchElementException:
                url = (
                    available_seats[i]
                    .find_element_by_xpath("div")
                    .find_element_by_xpath("div")
                    .find_element_by_xpath("a")
                    .get_attribute("href")
                )

            seats.append(
                Seat(
                    url,
                    row_names[i].text,
                    available_seats[i].text,
                )
            )

        slot_name = available_seats[0].text
        time_slot = Timeslot(seats, slot_name)

        return time_slot

    def reserveSeat(self, seat):
        self.driver.get(seat.url)
        self.driver.find_element(By.NAME, "save_button").click()
        self.goTodayPage()

    def cancelSeat(self, seat):
        self.driver.get(seat.url)
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/a").click()
        assert (
            self.driver.switch_to.alert.text
            == "Sind Sie sicher,\ndass Sie diesen Eintrag\nlöschen wollen?\n\n"
        )
        self.driver.switch_to.alert.accept()
        self.goTodayPage()

    def getDateRange(self, fromDate, toDate):
        # Inclusive Start inclusive to
        logging.debug(f"Creating Dates Range from{fromDate} to {toDate}")
        dates = []
        itter = fromDate

        logging.debug(f"Apptoing {fromDate} to Range")
        dates.append(fromDate)

        while itter != toDate:
            itter = itter + timedelta(days=1)
            logging.debug(f"Appending {itter} to Range")
            dates.append(itter)

        return dates


if __name__ == "__main__":
    now = date.today()
    session = SeleniumSession()
    session.setup()
    session.authenticate("BIBUsername", "BibPassword")
    day = session.getDay(now)
    session.teardown()
