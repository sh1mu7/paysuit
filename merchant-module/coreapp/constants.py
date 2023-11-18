from django.db import models
from django.utils.translation import gettext_lazy as _


# Business  Type
class BusinessType(models.IntegerChoices):
    SOLE = 0, _("Sole Trade")
    PARTNERSHIP = 1, _("Partnership")
    PRIVATE_LIMITED = 2, _("Private Limited")
    PUBLIC_LIMITED = 3, _("Public Limited")


# Document  Status
class BusinessStatus(models.IntegerChoices):
    PENDING = 0, _("Pending")
    APPROVED = 1, _("Approved")
    REJECTED = 2, _("Rejected")
    ON_PROCESSING = 3, _("On Processing")
    DEACTIVATED = 4, _("Deactivated")


# Legal Document  Options
class LegalDocumentChoices(models.IntegerChoices):
    NID = 0, _("NID")
    TIN = 1, _("TIN")
    BIN = 2, _("BIN")
    POA = 3, _("Power of Attorney")
    MOA = 4, _("Memorandum of Association")
    TRADE_LICENSE = 5, _("Trade License")
    VAT_CERTIFICATE = 6, _("Vat Certificate")
    TAX_CERTIFICATE = 7, _("Tax Certificate")
    INCORPORATION_CERTIFICATE = 8, _("Incorporation Certificate")
    FORM_XII = 9, _("FORM XII")
    CHEQUE_LEAF = 10, _("Cheque Leaf")
    BANK_STATEMENT = 11, _("Bank Statement")
    UTILITY_BILL = 12, _("Utility Bill")


# Document  Status
class DocumentStatus(models.IntegerChoices):
    PENDING = 0, _("Pending")
    APPROVED = 1, _("Approved")
    REJECTED = 2, _("Rejected")
    ON_PROCESSING = 3, _("On Processing")
