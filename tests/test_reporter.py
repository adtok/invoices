from invoices.reporter import almost_equal, Invoice, Reporter


def test_reporter():
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
