import enum
import json
from typing import List

from pydantic import BaseModel


class Currency(str, enum.Enum):
    eur = 'EUR'
    kzt = 'KZT'


class Status(str, enum.Enum):
    pending = 'PENDING'
    completed = 'COMPLETED'


class CurrenciesRate(BaseModel):
    currency: str
    rate: float


class Dep(BaseModel):
    at: str = None
    airport: str = None


class Segment(BaseModel):
    operating_airline: str = None
    marketing_airline: str = None
    flight_number: str = None
    equipment: str = None
    dep: Dep
    arr: Dep
    baggage: str = None


class Pricing(BaseModel):
    total: str = None
    base: str = None
    taxes: str = None
    currency: Currency


class Flight(BaseModel):
    duration: int = None
    segments: List[Segment]


class Flights(BaseModel):
    flights: List[Flight]
    refundable: bool = False
    validating_airline: str = None
    pricing: Pricing


class SearchRes(BaseModel):
    search_id: str


class Results(BaseModel):
    search_id: str
    status: Status = Status.pending
    items: List[Flights] = []

    def sorted_by_price(self, reverse: bool) -> 'Results':
        """Sort items from Results by total price."""

        self.items = sorted(self.items, key=lambda f: float(f.pricing.total), reverse=reverse)
        return self

    def prepare_to_redis(self, value: str, res: dict) -> 'Results':
        """Preparing data for saving to Radis (updating/creating items by key: search_id)."""

        if value:
            return self.parse_obj({'search_id': self.search_id, 'items': json.loads(value)['items'] + res})
        else:
            return self.parse_obj({'search_id': self.search_id, 'items': res})

    def set_status(self, value: str, status: Status) -> 'Results':
        """Preparing data for setting the status of an entry in a radis (updating field status)."""

        return self.parse_obj({'search_id': self.search_id, 'status': status, 'items': json.loads(value)['items']})
