from dataclasses import dataclass, field
from typing import List
from datetime import date

@dataclass
class Config:
    username: str
    password: str

    rooms: List[str] =  field(default_factory=list)
    timeslots: List[str] = field(default_factory=list)
    days: List[date] = field(default_factory=lambda: [date.today()])


