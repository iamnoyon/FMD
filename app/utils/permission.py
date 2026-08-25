from enum import Enum

class Permissions(str, Enum):
    CREATE_USER = 'create_user'
    READ_USER = 'read_user'
    UPDATE_USER = 'update_user'
    DELETE_USER = 'delete_user'