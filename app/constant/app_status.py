from enum import Enum

from starlette import status


class AppStatus(Enum):
    SUCCESS = status.HTTP_200_OK, 200, 'SUCCESS.'

    ERROR_OWNER_NOT_FOUND = status.HTTP_302_FOUND, 302, 'PRODUCT_OWNER_NOT_EXIST'
    ERROR_PRODUCT_NOT_EXIST = status.HTTP_302_FOUND, 302, 'PRODUCT_NOT_EXIST'
    ERROR_LESSON_NOT_EXIST = status.HTTP_302_FOUND, 302, 'LESSON_NOT_EXIST'
    ERROR_NOT_JOINED_TO_PRODUCT = status.HTTP_302_FOUND, 302, 'NOT_JOINED_TO_PRODUCT'

    ERROR_BAD_REQUEST = status.HTTP_400_BAD_REQUEST, 400, 'BAD_REQUEST'
    ERROR_LOGIN = status.HTTP_400_BAD_REQUEST, 400, 'ERROR_LOGIN_FAILED'
    ERROR_REGISTER_NOT_MATCH_PASSWORD = status.HTTP_400_BAD_REQUEST, 400, 'PASSWORDS_DO_NOT_MATCH'
    ERROR_CONFIRM_PASSWORD_DOES_NOT_MATCH = status.HTTP_400_BAD_REQUEST, 400, 'CONFIRM_PASSWORD_DOES_NOT_MATCH'
    ERROR_UNSUPPORTED_DATA_TYPES = status.HTTP_400_BAD_REQUEST, 400, 'UNSUPPORTED_DATA_TYPES'
    ERROR_MISSING_TOKEN_ERROR = status.HTTP_400_BAD_REQUEST, 400, 'MISSING_TOKEN_ERROR'
    ERROR_PASSWORD_INCORRECT = status.HTTP_400_BAD_REQUEST, 400, "ERROR_PASSWORD_INCORRECT"
    ERROR_PASSWORD_CONFIRM_WRONG = status.HTTP_400_BAD_REQUEST, 400, "ERROR_PASSWORD_CONFIRM_WRONG"
    ERROR_INVALID_PASSWORD_LENGTH = status.HTTP_400_BAD_REQUEST, 400, 'INVALID_PASSWORD_LENGTH'
    ERROR_INVALID_VERIFY_CODE = status.HTTP_400_BAD_REQUEST, 400, 'INVALID_VERIFY_CODE'
    ERROR_INVALID_INPUT = status.HTTP_400_BAD_REQUEST, 400, 'INVALID_INPUT'
    ERROR_INVALID_ACTION = status.HTTP_400_BAD_REQUEST, 400, 'INVALID_ACTION'
    ERROR_PLEASE_ADD_TRANSACTION_ID = status.HTTP_400_BAD_REQUEST, 400, 'PLEASE_ADD_TRANSACTION_ID'

    ERROR_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED, 401, 'UNAUTHORIZED'
    ERROR_INVALID_PRICE = status.HTTP_401_UNAUTHORIZED, 401, 'INVALID_PRICE'
    ERROR_INVALID_QUANTITY = status.HTTP_401_UNAUTHORIZED, 401, 'INVALID_QUANTITY'
    ERROR_PASSWORD_INVALID = status.HTTP_401_UNAUTHORIZED, 401, 'ACCOUNT_OR_PASSWORD_INVALID'
    ERROR_INACTIVE_USER = status.HTTP_401_UNAUTHORIZED, 401, 'INACTIVE_USER'
    ERROR_INVALID_TOKEN = status.HTTP_401_UNAUTHORIZED, 401, 'INVALID_TOKEN'
    ERROR_PRODUCT_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED, 401, 'PRODUCT_UNAUTHORIZED'

    ERROR_INVALID_ROLE = status.HTTP_403_FORBIDDEN, 403, 'INVALID_ROLE'

    ERROR_404_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'NOT_FOUND'
    ERROR_NOTIFICATION_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'NOTIFICATION_NOT_FOUND'
    ERROR_USER_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'ACCOUNT_NOT_FOUND'
    ERROR_PRODUCT_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'PRODUCT_NOT_FOUND'
    ERROR_PRODUCT_FARMER_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'PRODUCT_FARMER_NOT_FOUND'
    ERROR_SEEDLING_COMPANY_PRODUCT_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'SEEDLING_COMPANY_PRODUCT_NOT_FOUND'
    ERROR_FARMER_PRODUCT_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'FARMER_PRODUCT_NOT_FOUND'
    ERROR_MANUFACTURER_PRODUCT_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'MANUFACTURER_PRODUCT_NOT_FOUND'
    ERROR_TRANSACTION_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'TRANSACTION_NOT_FOUND'
    ERROR_TRANSACTION_SF_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'TRANSACTION_SF_NOT_FOUND'
    ERROR_TRANSACTION_FM_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'TRANSACTION_FM_NOT_FOUND'
    ERROR_COMMENT_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'COMMENT_NOT_FOUND'
    ERROR_MARKETPLACE_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'MARKETPLACE_NOT_FOUND'
    ERROR_EMAIL_NOT_FOUND = status.HTTP_404_NOT_FOUND, 404, 'EMAIL_NOT_FOUND'

    ERROR_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED, 405, 'METHOD_NOT_ALLOWED'
    ERROR_PRODUCT_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED, 405, 'PRODUCT_METHOD_NOT_ALLOWED'
    ERROR_COMMENT_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED, 405, 'COMMENT_METHOD_NOT_ALLOWED'
    ERROR_TRANSACTION_SF_METHOD_NOT_ALLOWED = (status.HTTP_405_METHOD_NOT_ALLOWED, 405,
                                               'TRANSACTION_SF_METHOD_NOT_ALLOWED')
    ERROR_TRANSACTION_FM_METHOD_NOT_ALLOWED = (status.HTTP_405_METHOD_NOT_ALLOWED, 405,
                                               'TRANSACTION_FM_METHOD_NOT_ALLOWED')
    ERROR_YOU_ARE_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED, 405, 'YOU_ARE_NOT_ALLOWED'
    ERROR_PURCHASE_PRODUCT_TYPE_INVALID = status.HTTP_405_METHOD_NOT_ALLOWED, 405, 'PURCHASE_PRODUCT_TYPE_INVALID'

    ERROR_ACCOUNT_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'ACCOUNT_ALREADY_EXIST'
    ERROR_ALREADY_JOINED_TO_PRODUCT = status.HTTP_409_CONFLICT, 409, 'ALREADY_JOINED_TO_PRODUCT'
    ERROR_EMAIL_ALREADY_EXIST = status.HTTP_409_CONFLICT, 409, 'EMAIL_ALREADY_EXIST'
    ERROR_PRODUCT_KEY_CONFLICT = status.HTTP_409_CONFLICT, 409, 'PRODUCT_KEY_ALREADY_EXIST'
    ERROR_TRANSACTION_SF_CONFLICT = status.HTTP_409_CONFLICT, 409, 'TRANSACTION_SF_ALREADY_EXIST'
    ERROR_TRANSACTION_FM_CONFLICT = status.HTTP_409_CONFLICT, 409, 'TRANSACTION_FM_ALREADY_EXIST'

    ERROR_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR, 500, 'SERVER_ERROR'
    ERROR_REGISTER_USER = status.HTTP_500_INTERNAL_SERVER_ERROR, 500, 'REGISTER_USER_FAILED'

    # need to refactor soon
    ERROR_NOTIFICATION_GET = status.HTTP_302_FOUND, 'NOTIFICATION_GET_ERROR'
    ERROR_NOTIFICATION_READ_ALL = status.HTTP_302_FOUND, 'ERROR_NOTIFICATION_READ_ALL'
    ERROR_NOTIFICATION_CREATE = status.HTTP_302_FOUND, 'ERROR_NOTIFICATION_CREATE'

    ERROR_VALIDATION = status.HTTP_400_BAD_REQUEST, 1000, 'ERROR_VALIDATION'
    ERROR_USER_UPDATE = status.HTTP_400_BAD_REQUEST, 1001, 'ERROR_USER_UPDATE'
    ERROR_USER_CHANGE_PASSWORD = status.HTTP_400_BAD_REQUEST, 1004, 'ERROR_USER_CHANGE_PASSWORD'
    ERROR_USER_SETTING_AVATAR_DEFAULT = status.HTTP_400_BAD_REQUEST, 1007, 'ERROR_USER_SETTING_AVATAR_DEFAULT'
    ERROR_USER_BUY_AVATAR = status.HTTP_400_BAD_REQUEST, 1008, 'ERROR_USER_BUY_AVATAR'
    USER_CHANGE_PASSWORD_SUCCESS = status.HTTP_200_OK, 200, 'USER_CHANGE_PASSWORD_SUCCESS'
    LOGIN_SUCCESS = status.HTTP_200_OK, 200, 'LOGIN_SUCCESS'
    LOGOUT_SUCESS = status.HTTP_200_OK, 200, 'LOGOUT_SUCCESS'
    LOGIN_ERROR = status.HTTP_400_BAD_REQUEST, 1009, 'LOGIN_ERROR'

    @property
    def status_code(self):
        return self.value[0]

    @property
    def app_status_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]

    @property
    def meta(self):
        return dict(status_code=self.value[0], message=self.value[2])
