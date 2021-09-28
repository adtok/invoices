"""Testing for the Reporter class"""
from .utils import almost_equal

from invoices.reporter import Invoice, Reporter

import pytest


def test_reporter():
    """Basic tests for the Reporter class"""
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


def test_no_duplicate_invoices():
    """Test no duplicate invoice_id in invoices"""
    reporter = Reporter(0)
    reporter.create_invoice(Invoice(0, 10.0))
    with pytest.raises(ValueError):
        reporter.create_invoice(Invoice(0, 0.0))


def test_to_dict():
    """Tests Reporter.to_dict()"""
    reporter = Reporter(0)
    reporter.create_invoice(Invoice(0, 10.0))
    reporter.pay_invoice(0)
    reporter_dict = {
        "reporter_id": 0,
        "invoices": {
            0: {
                "invoice_id": 0,
                "price": 10.0,
                "discount": 0.0,
                "paid": True,
                "discount_value": 0.0,
                "net_price": 10.0,
            }
        },
    }
    assert reporter.to_dict() == reporter_dict
