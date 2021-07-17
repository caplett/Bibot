from enum import Enum


class Room:
    def __init__(self, url, roomName):
        self.url = url
        self.roomName = roomName


class Timeslot:
    def __init__(self, seats, slotName):
        self.seats = seats
        self.slotName = slotName


class Seat:
    def __init__(self, url, number, field_text):
        self.url = url
        self.number = number
        self.field_text = field_text
        self.checkState()

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
