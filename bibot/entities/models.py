from enum import Enum


class DayModel:
    def __init__(self, rooms, date):
        self.rooms = rooms
        self.date = date
        self.application_model = None
        self.setDayInRooms()

    def setDayInRooms(self):
        for x in self.rooms:
            x.setDay(self)

    def getFreePlaces(self):
        free_places = []
        for x in self.rooms:
            free_places = free_places + x.getFreePlaces()
        return free_places

    def getReservedPlaces(self):
        reserved_places = []
        for x in self.rooms:
            reserved_places = reserved_places + x.getReservedPlaces()
        return reserved_places


class RoomModel:
    def __init__(self, url, roomName):
        self.url = url
        self.roomName = roomName
        self.day_model = None
        # self.time_slots

    def setTimeSlots(self, time_slots):
        self.time_slots = time_slots
        self.setRoomInTimeSlots()

    def setRoomInTimeSlots(self):
        for x in self.time_slots:
            x.setRoom(self)

    def setDay(self, day):
        self.day_model = day

    def getFreePlaces(self):
        free_places = []
        for x in self.time_slots:
            free_places = free_places + x.getFreePlaces()
        return free_places

    def getReservedPlaces(self):
        reserved_places = []
        for x in self.time_slots:
            reserved_places= reserved_places + x.getReservedPlaces()
        return reserved_places



class TimeslotModel:
    def __init__(self, seats, slotName):
        self.seats = seats
        self.slotName = slotName
        self.room_model = None

    def setTimeSlotInPlaces(self):
        for x in self.seats:
            x.setTimeSlot(self)

    def setRoom(self, room):
        self.room_model = room

    def getFreePlaces(self):
        free_places = []
        for x in self.seats:
            if x.state == State.FREE:
                free_places = free_places + [x]
        return free_places

    def getReservedPlaces(self):
        reserved_places = []
        for x in self.seats:
            if x.state == State.RESERVED:
                reserved_places = reserved_places + [x]
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
