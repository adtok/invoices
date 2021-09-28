"""A simple invoice reporting system"""

from dataclasses import dataclass, field, asdict
from typing import Union


@dataclass
class Invoice:
    """A dataclass to hold invoices"""

    invoice_id: int
    price: float
    discount: float = 0.0  # 7.0 = 7%
    paid: bool = False
    discount_value: float = field(init=False)
    net_price: float = field(init=False)

    def __post_init__(self):
        """Set the discount value and net price"""
        discount_value = round(self.price * (self.discount / 100), 2)
        self.discount_value = discount_value
        self.net_price = self.price - discount_value

    def pay(self) -> None:
        """Marks the invoice as paid"""
        self.paid = True

    def to_dict(self) -> dict[str, Union[int, float, bool]]:
        """Returns the object as a dictionary"""
        return asdict(self)


@dataclass
class Reporter:
    """A class that provides a report of all invoices."""

    reporter_id: int
    invoices: dict[int, Invoice] = field(default_factory=dict)

    def create_invoice(self, invoice: Invoice) -> None:
        """Adds an invoice to to the reporter"""
        if invoice.invoice_id in self.invoices:
            raise ValueError(f"An invoice with id {invoice.invoice_id} already exists.")
        self.invoices[invoice.invoice_id] = invoice

    def pay_invoice(self, invoice_id) -> None:
        """Pays the invoice for the given id"""
        self.invoices[invoice_id].pay()

    @property
    def funds_paid(self) -> float:
        """Gives the total money paid across all invoices"""
        return sum(
            invoice.net_price for invoice in self.invoices.values() if invoice.paid
        )

    @property
    def funds_owed(self) -> float:
        """Gives the total money owed for all invoices"""
        return sum(
            invoice.net_price for invoice in self.invoices.values() if not invoice.paid
        )

    def to_dict(self) -> dict[str, Union[int, dict[int, Invoice]]]:
        """Returns a dictionary representation of the reporter object"""
        return asdict(self)
