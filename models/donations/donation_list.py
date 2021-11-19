from __future__ import annotations

from models.model_list import ModelList
from models.donations.donation import Donation


class DonationList(ModelList):
    def __init__(self):
        super().__init__()
        self.items: list[Donation] = []

    @property
    def item(self) -> Donation:
        return Donation()
