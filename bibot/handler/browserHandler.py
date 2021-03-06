# Generated by Selenium IDE
import logging
import bs4
from typing import List, Tuple
from datetime import date, timedelta
from bs4 import BeautifulSoup
from bibot.entities.models import RoomModel, SeatModel, ScanModel, handlerInterface
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumSession(handlerInterface):
    logger = logging.getLogger(__name__)

    def setup(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(
            "https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year=2021&month=07&day=11&area=20&room=140"
        )
        self.goTodayPage()
        self.logger.info("Selenium Session successfully setup")

    def teardown(self) -> None:
        self.driver.quit()
        self.logger.info("Selenium successfully teardown")

    def authenticate(self, user: str, password: str) -> bool:
        self.driver.find_element(
            By.CSS_SELECTOR, "form:nth-child(2) input:nth-child(3)"
        ).click()
        self.driver.find_element(By.ID, "NewUserName").send_keys(user)
        self.driver.find_element(By.ID, "NewUserPassword").send_keys(password)
        self.driver.find_element(By.ID, "EULA_INPUT").click()
        self.driver.find_element(By.CSS_SELECTOR, ".submit").click()

        try:
            self.driver.find_element_by_link_text("Unbekannter Benutzer")
            self.logger.error("Login did not work with given credentials")
            return False
        except NoSuchElementException:
            self.logger.info("Login worked")
            return True

    def isAuthenticated(self) -> bool:
        self.goTodayPage()
        try:
            self.driver.find_element_by_link_text("Unbekannter Benutzer")
            self.logger.info("Not logged in")
            return False
        except NoSuchElementException:
            self.logger.info("Still logged in")
            return True

    def goTodayPage(self) -> None:
        self.logger.debug("Go to Today page")
        self.goToDate(date.today())

    def goToDate(self, date: date) -> None:
        self.driver.get(
            f"https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year={date.year}&month={date.month}&day={date.day}&area=20&room=140"
        )

    def getDay(self, date: date, scan_model=ScanModel()) -> ScanModel:
        self.goToDate(date)
        self.handleRooms(date, scan_model)

        return scan_model

    def getDays(self, fromDate: date, toDate: date) -> ScanModel:
        range = self.getDateRange(fromDate, toDate)
        scan_model = ScanModel()
        [self.getDay(x, scan_model=scan_model) for x in range]
        return scan_model

    def getAvailableRooms(self) -> List[RoomModel]:
        self.logger.debug("Getting Available Rooms from website")
        self.driver.find_element(By.LINK_TEXT, "gehe zum heutigen Tag").click()
        elements = self.driver.find_elements_by_xpath("//div[@id='dwm_areas']/ul/li")
        rooms = [
            RoomModel(x.find_element_by_xpath("a").get_attribute("href"), x.text)
            for x in elements
        ]

        self.logger.debug("Found the following available Rooms:")
        for x in rooms:
            self.logger.debug(x.roomName)
        return rooms

    def getAvailableTimeSlots(
        self, room: RoomModel
    ) -> Tuple[bs4.element.Tag, bs4.element.Tag]:
        self.driver.get(room.url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        time_slots = soup.find("table", id="day_main").tbody.find_all("tr")
        row_names = (
            soup.find("table", id="day_main").find_all("thead")[1].tr.find_all("th")
        )
        return time_slots, row_names

    def getAvailableSeats(self, timeslot: bs4.element.Tag) -> List[bs4.element.Tag]:
        seats = [x for x in timeslot.find_all("td")]
        return seats

    def handleRooms(self, date: date, scan_model: ScanModel) -> None:
        available_rooms = self.getAvailableRooms()
        [self.handleRoom(x, date, scan_model) for x in available_rooms]

    def handleRoom(
        self, availableRoom: RoomModel, date: date, scan_model: ScanModel
    ) -> None:
        available_timeslots, row_names = self.getAvailableTimeSlots(availableRoom)
        [
            self.handleTimeSlot(x, date, availableRoom, row_names, scan_model)
            for x in available_timeslots
        ]

    def handleTimeSlot(
        self,
        timeslot: bs4.element.Tag,
        date: date,
        availableRoom: RoomModel,
        row_names: bs4.element.ResultSet,
        scan_model: ScanModel,
    ) -> None:
        available_seats = self.getAvailableSeats(timeslot)
        assert len(row_names) == len(available_seats)

        slot_name = available_seats[0].text.strip()
        for i in range(1, len(available_seats)):
            url_part = available_seats[i].div.a.get("href")
            if url_part == None:
                # Catch reserved places. They have one div level more
                url_part = available_seats[i].div.div.a.get("href")

            url = (
                "https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/"
                + url_part
            )

            scan_model.addSeat(
                date,
                availableRoom.roomName,
                slot_name,
                SeatModel(
                    url,
                    row_names[i].text.strip(),
                    available_seats[i].text.strip(),
                    self,
                ),
            )

    def reserveSeat(self, seat: SeatModel) -> None:
        try:
            self.driver.get(seat.url)
            self.driver.find_element(By.NAME, "save_button").click()
            self.goTodayPage()
            self.logger.info("Reseverd Seat")
        except Exception as e:
            self.logger.exception("Seat Reservation did not work")

    def cancelSeat(self, seat: SeatModel) -> None:
        try:
            self.driver.get(seat.url)
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/a").click()
            assert (
                self.driver.switch_to.alert.text
                == "Sind Sie sicher,\ndass Sie diesen Eintrag\nl??schen wollen?\n\n"
            )
            self.driver.switch_to.alert.accept()
            self.goTodayPage()
            self.logger.info("Canceled Seat")
        except Exception as e:
            self.logger.exception("Seat Cancelation did not work")

    def getDateRange(self, fromDate: date, toDate: date) -> List[date]:
        # Inclusive Start inclusive to
        self.logger.debug(f"Creating Dates Range from{fromDate} to {toDate}")
        dates = []
        itter = fromDate

        self.logger.debug(f"Apptoing {fromDate} to Range")
        dates.append(fromDate)

        while itter != toDate:
            itter = itter + timedelta(days=1)
            self.logger.debug(f"Appending {itter} to Range")
            dates.append(itter)

        return dates
