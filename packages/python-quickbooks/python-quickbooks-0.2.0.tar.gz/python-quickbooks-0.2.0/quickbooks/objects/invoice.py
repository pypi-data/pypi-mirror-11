from base import QuickbooksBaseObject, Ref, CustomField, Address, EmailAddress, CustomerMemo, QuickbooksManagedObject
from tax import TxnTaxDetail


class DiscountLineDetail(QuickbooksBaseObject):
    class_dict = {
        "DiscountAccountRef": Ref
    }

    def __init__(self):
        super(DiscountLineDetail, self).__init__()
        self.PercentBased = True
        self.DiscountPercent = 0
        self.DiscountAccountRef = None


class SalesItemLineDetail(QuickbooksBaseObject):
    class_dict = {
        "ItemRef": Ref,
        "TaxCodeRef": Ref
    }

    def __init__(self):
        super(SalesItemLineDetail, self).__init__()
        self.UnitPrice = 0
        self.Qty = 0


class InvoiceDetail(QuickbooksBaseObject):
    class_dict = {
        "DiscountLineDetail": DiscountLineDetail,
        "SalesItemLineDetail": SalesItemLineDetail,
    }

    def __init__(self):
        super(InvoiceDetail, self).__init__()
        self.LineNum = ""
        self.Description = ""
        self.Amount = ""
        self.DetailType = ""


class Invoice(QuickbooksManagedObject):
    """
    QBO definition: An Invoice represents a sales form where the customer pays for a product or service later.

    """

    class_dict = {
        "DepartmentRef": Ref,
        "CurrencyRef": Ref,
        "ClassRef": Ref,
        "SalesTermRef": Ref,
        "ShipMethodRef": Ref,
        "DepositToAccountRef": Ref,
        "BillAddr": Address,
        "ShipAddr": Address,
        "TxnTaxDetail": TxnTaxDetail,
        "BillEmail": EmailAddress,
        "CustomerMemo": CustomerMemo
    }

    list_dict = {
        "CustomField": CustomField,
        "Line": InvoiceDetail
    }

    qbo_object_name = "Invoice"

    def __init__(self):
        super(Invoice, self).__init__()
        self.Deposit = 0
        self.Balance = 0
        self.AllowIPNPayment = True
        self.DocNumber = ""
        self.TxnDate = ""
        self.PrivateNote = ""
        self.DueDate = ""
        self.ShipDate = ""
        self.TrackingNum = ""
        self.TotalAmt = ""
        self.ApplyTaxAfterDiscount = ""
        self.PrintStatus = ""
        self.EmailStatus = ""

        self.BillAddr = None
        self.ShipAddr = None
        self.BillEmail = None
        self.CustomerMemo = None
        self.CustomField = []
