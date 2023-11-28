from datetime import datetime
from fastapi import Request

from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.core.settings import settings
from app.utils.vnpay import Vnpay


def payment(request: Request, order_id: int, amount: int, order_desc: str, bank_code: str, language: str = "vn",
            order_type: str = "billpayment"):
    """
        order_id: time in_progress transaction
        order_desc: content transaction
        bank_code: bank transaction
    """
    ipaddr = request.client.host
    # Build URL Payment
    vnp = Vnpay()
    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = amount * 100
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = order_id
    vnp.requestData['vnp_OrderInfo'] = order_desc
    vnp.requestData['vnp_OrderType'] = order_type
    # Check language, default: vn
    if language and language != '':
        vnp.requestData['vnp_Locale'] = language
    else:
        vnp.requestData['vnp_Locale'] = 'vn'
        # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
    if bank_code and bank_code != "":
        vnp.requestData['vnp_BankCode'] = bank_code

    vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.requestData['vnp_IpAddr'] = ipaddr
    vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
    print(vnpay_payment_url)
    return vnpay_payment_url


def payment_return(request: Request):
    inputData = request.query_params
    print(inputData)
    if inputData:
        vnp = Vnpay()
        vnp.responseData = dict(inputData)
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return {
                    "result": "Thành công", "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode}

    raise error_exception_handler(error=Exception, app_status=AppStatus.ERROR_TRANSACTION_UNSUCCESSFUL)
