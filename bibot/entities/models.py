from enum import Enum
import pandas as pd


class DayModel:
    def __init__(self, rooms, date):
        self.rooms = rooms
        self.date = date
        self.application_model = None
        self.setDayInRooms()
# TODO functions typisieren
class ScanModel:
    dataframe = pd.DataFrame()

    def setDayInRooms(self):
        for x in self.rooms:
            x.setDay(self)
    # PERF: Could be faster if multiple rows are generated, then concatenated
    def addSeat(self, date, room_name, timeslot_name, seat_model):
        self.dataframe = self.dataframe.append(
            pd.DataFrame([seat_model], index=[[date], [room_name], [timeslot_name]])
        )

    def getFreePlaces(self):
        free_places = []
        for x in self.rooms:
            free_places = free_places + x.getFreePlaces()
        return free_places
    def createFromDataframe__(self, dataframe):
        scan_model = ScanModel()
        scan_model.dataframe = dataframe
        return scan_model

    def getReservedPlaces(self):
        reserved_places = []
        for x in self.rooms:
            reserved_places = reserved_places + x.getReservedPlaces()
        return reserved_places
    def getAvailableDays(self):
        """
        Get list of date objects with all days in
        scan modell
        """
        return list(self.dataframe.index.unique(level=0))

    def getAvailableRooms(self):
        """
        Get list of strings with all rooms in
        scan modell
        """
        return list(self.dataframe.index.unique(level=1))

class RoomModel:
    def __init__(self, url, roomName):
        self.url = url
        self.roomName = roomName
        self.day_model = None
        # self.time_slots
    def getAvailableTimeslots(self):
        """
        Get list of strings with all timesots in
        scan modell
        """
        return list(self.dataframe.index.unique(level=2))

    def setTimeSlots(self, time_slots):
        self.time_slots = time_slots
        self.setRoomInTimeSlots()
    def getAvailableDays(self):
    def getFromDays(self, days):
        """Slice scan with days of interest.

        :days: list of datetime.date objects
        :returns: New ScanModel sliced with days

        """

    def setRoomInTimeSlots(self):
        for x in self.time_slots:
            x.setRoom(self)
        dataframe = self.dataframe.loc[(days), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def setDay(self, day):
        self.day_model = day
    def getFromRooms(self, rooms):
        """Slice scan with rooms of interest.

    def getFreePlaces(self):
        free_places = []
        for x in self.time_slots:
            free_places = free_places + x.getFreePlaces()
        return free_places
        :rooms: list of room Names as strings
        :returns: New ScanModel sliced with room Names

    def getReservedPlaces(self):
        reserved_places = []
        for x in self.time_slots:
            reserved_places= reserved_places + x.getReservedPlaces()
        return reserved_places
        """

        dataframe = self.dataframe.loc[(slice(None), rooms), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def getFromTimeslots(self, timeslots):
        """Slice scan with timeslots of interest.

class TimeslotModel:
    def __init__(self, seats, slotName):
        self.seats = seats
        self.slotName = slotName
        self.room_model = None
        :timeslots: list of timeslot Names as strings
        :returns: New ScanModel sliced with timeslot Names

    def setTimeSlotInPlaces(self):
        for x in self.seats:
            x.setTimeSlot(self)
        """

    def setRoom(self, room):
        self.room_model = room
        dataframe = self.dataframe.loc[(slice(None), slice(None), timeslots), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def getFreePlaces(self):
        """ Get free places from given Scan Model
        :returns: List SeatModels 

        """
        # HACK: position 0 index is a hack. 
        # Would be better if it was not necessary
        free_places = []
        for x in self.seats:
            if x.state == State.FREE:
                free_places = free_places + [x]
        for _, row in self.dataframe.iterrows():
            seat = row[0]
            if seat.state == State.FREE:
                free_places.append(seat)

        return free_places

    def getReservedPlaces(self):
        """ Get reserved places from given Scan Model
        :returns: List SeatModels 

        """
        # HACK: position 0 index is a hack. 
        # Would be better if it was not necessary
        reserved_places = []
        for x in self.seats:
            if x.state == State.RESERVED:
                reserved_places = reserved_places + [x]
        for _, row in self.dataframe.iterrows():
            seat = row[0]
            if seat.state == State.RESERVED:
                reserved_places.append(seat)

        return reserved_places


class SeatModel:
    def __init__(self, url, number, field_text, handler):
        self.url = url
        self.number = number
        self.field_text = field_text
        self.checkState()
        self.handler = handlerInterface()
        self.handler = handler
        self.timeslotModel = None

    def setHandler(self, handler):
        self.handler = handler

    def setTimeslot(self, timeslot):
        self.timeSlotModel = timeslot

    def reserve(self):
        self.handler.reserveSeat(self)

    def cancel(self):
        self.handler.cancelSeat(self)

    def checkState(self):
        text = self.field_text
        if text == "[X]":
            self.state = State.OCCUPIED
        elif text == "":
            self.state = State.FREE
        else:
            self.state = State.RESERVED


class State(Enum):
    FREE = 1
    OCCUPIED = 2
    RESERVED = 3


class handlerInterface:
    def reserveSeat(self, seat):
        pass

    def cancelSeat(self, seat):
        pass
