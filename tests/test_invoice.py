"""Test cases for the Invoice class"""

from .utils import almost_equal

from invoices.reporter import Invoice


def test_invoice():
    """Test cases for the invoice class"""
    invoice = Invoice(0, 10.0)
    assert not invoice.paid
    invoice.pay()
    assert invoice.paid
    invoice_dict = {
        "invoice_id": 0,
        "price": 10.0,
        "discount": 0.0,
        "paid": True,
        "discount_value": 0.0,
        "net_price": 10.0,
    }
    assert invoice.to_dict() == invoice_dict


def test_invoice_discounts():
    invoice = Invoice(0, 10.0, 10.0)
    assert almost_equal(invoice.discount_value, 1.0)
    assert almost_equal(invoice.net_price, 9.0)
