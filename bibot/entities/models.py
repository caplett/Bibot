from __future__ import annotations
from enum import Enum
from typing import List
from datetime import date
import pandas as pd


class ScanModel:
    dataframe = pd.DataFrame()

    # PERF: Could be faster if multiple rows are generated, then concatenated
    def addSeat(
        self, date: date, room_name: str, timeslot_name: str, seat_model: SeatModel
    ) -> None:
        self.dataframe = self.dataframe.append(
            pd.DataFrame([seat_model], index=[[date], [room_name], [timeslot_name]])
        )

    def createFromDataframe__(self, dataframe: pd.DataFrame) -> ScanModel:
        scan_model = ScanModel()
        scan_model.dataframe = dataframe
        return scan_model

    def getAvailableDays(self) -> List[date]:
        """
        Get list of date objects with all days in
        scan modell
        """
        return list(self.dataframe.index.unique(level=0))

    def getAvailableRooms(self) -> List[str]:
        """
        Get list of strings with all rooms in
        scan modell
        """
        return list(self.dataframe.index.unique(level=1))

    def getAvailableTimeslots(self) -> List[str]:
        """
        Get list of strings with all timesots in
        scan modell
        """
        return list(self.dataframe.index.unique(level=2))

    def getFromDays(self, days: List[date]) -> ScanModel:
        """Slice scan with days of interest.

        :days: list of datetime.date objects
        :returns: New ScanModel sliced with days

        """

        dataframe = self.dataframe.loc[(days), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def getFromRooms(self, rooms: List[str]) -> ScanModel:
        """Slice scan with rooms of interest.

        :rooms: list of room Names as strings
        :returns: New ScanModel sliced with room Names

        """

        dataframe = self.dataframe.loc[(slice(None), rooms), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def getFromTimeslots(self, timeslots: List[str]) -> ScanModel:
        """Slice scan with timeslots of interest.

        :timeslots: list of timeslot Names as strings
        :returns: New ScanModel sliced with timeslot Names

        """

        dataframe = self.dataframe.loc[(slice(None), slice(None), timeslots), :]
        scan_model = self.createFromDataframe__(dataframe)
        return scan_model

    def getFreePlaces(self) -> List[SeatModel]:
        """Get free places from given Scan Model
        :returns: List SeatModels

        """
        # HACK: position 0 index is a hack.
        # Would be better if it was not necessary
        free_places = []
        for _, row in self.dataframe.iterrows():
            seat = row[0]
            if seat.state == State.FREE:
                free_places.append(seat)

        return free_places

    def getReservedPlaces(self) -> List[SeatModel]:
        """Get reserved places from given Scan Model
        :returns: List SeatModels

        """
        # HACK: position 0 index is a hack.
        # Would be better if it was not necessary
        reserved_places = []
        for _, row in self.dataframe.iterrows():
            seat = row[0]
            if seat.state == State.RESERVED:
                reserved_places.append(seat)

        return reserved_places


class RoomModel:
    def __init__(self, url, roomName):
        self.url = url
        self.roomName = roomName
        self.day_model = None


class SeatModel:
    def __init__(self, url, number, field_text, handler):
        self.url = url
        self.number = number
        self.field_text = field_text
        self.checkState()
        self.handler = handlerInterface()
        self.handler = handler
        self.timeslotModel = None

    def setHandler(self, handler: handlerInterface) -> None:
        self.handler = handler

    def reserve(self) -> None:
        self.handler.reserveSeat(self)

    def cancel(self) -> None:
        self.handler.cancelSeat(self)

    def checkState(self) -> None:
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
    def reserveSeat(self, seat: SeatModel):  # noqa
        pass

    def cancelSeat(self, seat: SeatModel):
        pass
