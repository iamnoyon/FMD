from enum import Enum

class Permissions(str, Enum):
    CREATE_USER = 'create_user'
    READ_USER = 'read_user'
    UPDATE_USER = 'update_user'
    DELETE_USER = 'delete_user'

    CREATE_CATEGORY = 'create_category',
    READ_CATEGORY = 'read_category',
    UPDATE_CATEGORY = 'update_category',
    DELETE_CATEGORY = 'delete_category',