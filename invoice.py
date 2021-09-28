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


def almost_equal(float1: float, float2: float, precision: float = 0.001) -> bool:
    """
    Returns if the difference between two floats is within a certain precision.

    Main purpose is to make sure monetary values are close enough after multiplication.
    """
    return abs(float1 - float2) < precision


def main():
    """Run tests for almost_equal, the Invoice class, and the Reporter class"""
    # test almost_equal
    assert almost_equal(10.0, 10.0005)
    assert not almost_equal(10.0, 10.1)
    assert almost_equal(10.0, 10.01, precision=0.1)

    # test the invoice dataclass
    invoice = Invoice(0, 10.0)
    assert not invoice.paid
    invoice.pay()
    assert invoice.paid

    invoice = Invoice(1, 10.0, 10.0)
    assert almost_equal(invoice.discount_value, 1.0)
    assert almost_equal(invoice.net_price, 9.0)

    # test the reporter dataclass
    reporter = Reporter(0)
    reporter.create_invoice(Invoice(0, 10.0))
    reporter.create_invoice(Invoice(1, 20.0))
    assert almost_equal(reporter.funds_owed, 30.0)
    assert almost_equal(reporter.funds_paid, 0.0)
    reporter.pay_invoice(0)
    assert almost_equal(reporter.funds_owed, 20.0)
    assert almost_equal(reporter.funds_paid, 10.0)
    reporter.create_invoice(Invoice(2, 100.0, 10.0))
    assert almost_equal(reporter.funds_owed, 110.0)
    assert almost_equal(reporter.funds_paid, 10.0)


if __name__ == "__main__":
    main()
