from __future__ import annotations

from typing import TYPE_CHECKING, List

from models.model_list import ModelList
from models.purchases.purchase import Purchase

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.owners.owner import Owner


class PurchaseList(ModelList):
    def __init__(self, ir: IR=None, owner: Owner=None):
        super().__init__()
        self.ir: IR = ir
        self.owner: Owner = owner
        self.items: list[Purchase] = []

    @property
    def item(self) -> Purchase:
        return Purchase(ir=self.ir, owner=self.owner)

    def get(self, filters: List[tuple] = None, order_by: List[tuple] = None, limit: int = None) -> PurchaseList:
        filters: list = filters if filters else []

        if self.ir:
            filters.append(('ir.id', '==', self.ir.id))
        if self.owner:
            filters.append(('owner.id', '==', self.owner.id))

        return super().get(filters=filters, order_by=order_by, limit=limit)
