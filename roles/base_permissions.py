FULL_ACCESS = dict(id="full_access", name="Full Access")
CREATE_NEW_USER = dict(id="create:new_user", name="Create New Users")
READ_USER = dict(id="read:user", name="Read User Details")
UPDATE_USER_PROFILE = dict(id="update:user", name="Update User Profile")
DELETE_USER = dict(id="delete:user", name="Delete User")
DELETE_USER_MFA = dict(id="delete:user_mfa", name="Delete User MFA")
UPDATE_USER_MFA = dict(id="update:user_mfa", name="Update User MFA")
UPDATE_USER_PASSWORD = dict(
    id="update:user_password", name="Update User Password")
DISABLE_USER = dict(id="disable:user", name="Disable User")
ENABLE_USER = dict(id="enable:user", name="Enable User")
UPDATE_ORGANIZATION = dict(id="update:organization",
                           name="Update Organization Details")
READ_ALL_LOGS = dict(id="read:all_logs", name="Read App Usage Logs")
READ_ALL_USERS = dict(id="read:all_users", name="Read All Users")
MODIFY_USER_ROLE = dict(id="update:user_role", name="Modify User Role")
MODIFY_USER_PERMISSIONS = dict(
    id="update:user_permissions", name="Modify User Permissions")


# Base Permissions that setup when Django is setup
base_permission = dict(
    FULL_ACCESS=FULL_ACCESS,
    CREATE_NEW_USER=CREATE_NEW_USER,
    READ_USER=READ_USER,
    UPDATE_USER_PROFILE=UPDATE_USER_PROFILE,
    DELETE_USER=DELETE_USER,
    DELETE_USER_MFA=DELETE_USER_MFA,
    UPDATE_USER_MFA=UPDATE_USER_MFA,
    UPDATE_USER_PASSWORD=UPDATE_USER_PASSWORD,
    DISABLE_USER=DISABLE_USER,
    ENABLE_USER=ENABLE_USER,
    UPDATE_ORGANIZATION=UPDATE_ORGANIZATION,
    READ_ALL_LOGS=READ_ALL_LOGS,
    READ_ALL_USERS=READ_ALL_USERS,
    MODIFY_USER_ROLE=MODIFY_USER_ROLE,
    MODIFY_USER_PERMISSIONS=MODIFY_USER_PERMISSIONS,
)

# Base Roles that setup when Django is setup
base_roles = [
    dict(
        name="Super Admin",
        permissions=[
            FULL_ACCESS
        ],
    ),
    dict(
        name="Admin",
        permissions=[
            CREATE_NEW_USER,
            READ_USER,
            UPDATE_USER_PROFILE,
            DELETE_USER,
            DELETE_USER_MFA,
            UPDATE_USER_MFA,
            UPDATE_USER_PASSWORD,
            DISABLE_USER,
            ENABLE_USER,
            UPDATE_ORGANIZATION,
            READ_ALL_LOGS,
            READ_ALL_USERS,
            MODIFY_USER_ROLE,
            MODIFY_USER_PERMISSIONS,
        ],
    ),
    dict(
        name="User",
        permissions=[
            READ_USER,
            UPDATE_USER_PROFILE,
            UPDATE_USER_PASSWORD,
            UPDATE_USER_MFA,
        ],
    ),
]
