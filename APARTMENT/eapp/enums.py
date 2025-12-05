from enum import Enum as UserEnum
from enum import Enum as ContractEnum
from enum import Enum as InvoiceEnum
from enum import Enum as PaymentEnum
from enum import Enum as PaymentStatus

class UserRole(UserEnum):
    USER=1
    CUSTOMER=2
    ADMIN=3

class ContractType(ContractEnum):
    TRONG=1
    DA_DAT_COC=2
    DANG_THUE=3


class InvoiceType(InvoiceEnum):
    CHUA_THANH_TOAN = 1
    DA_THANH_TOAN = 2
    TRE_HAN = 3

class PaymentType(PaymentEnum):
    TIEN_MAT = 1
    CHUYEN_KHOAN = 2
    MOMO = 3
    ZALO_PAY = 4


class PaymentStatus(PaymentStatus):
    THANH_CONG = 1
    THAT_BAI = 2
    CHO_XU_LY = 3