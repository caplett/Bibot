from dataclasses import dataclass
from typing import List
from datetime import date

@dataclass
class Config:
    username: str
    password: str

    rooms: List[str] = []
    timeslots: List[str] = []
    days: List[date] = [date.today()]


