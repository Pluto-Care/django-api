
# Base Permissions
base_permission = dict(
    FULL_ACCESS=dict(id="full_access", name="Full Access"),
    CREATE_NEW_USER=dict(id="create:new_user", name="Create New Users"),
    READ_USER=dict(id="read:user", name="Read User Details"),
    UPDATE_USER_PROFILE=dict(id="update:user", name="Update User Profile"),
    DELETE_USER=dict(id="delete:user", name="Delete User"),
    DELETE_USER_MFA=dict(id="delete:user_mfa", name="Delete User MFA"),
    UPDATE_USER_MFA=dict(id="update:user_mfa", name="Update User MFA"),
    UPDATE_USER_PASSWORD=dict(
        id="update:user_password", name="Update User Password"),
    DISABLE_USER=dict(id="disable:user", name="Disable User"),
    ENABLE_USER=dict(id="enable:user", name="Enable User"),
    UPDATE_ORGANIZATION=dict(id="update:organization",
                             name="Update Organization Details"),
    READ_ALL_LOGS=dict(id="read:all_logs", name="Read App Usage Logs"),
    READ_ALL_USERS=dict(id="read:all_users", name="Read All Users"),
    MODIFY_USER_ROLE=dict(id="update:user_role",
                             name="Modify User Role"),
    MODIFY_USER_PERMISSIONS=dict(id="update:user_permissions",
                                    name="Modify User Permissions"),
)

base_roles = [
    dict(
        name="Super Admin",
        permissions=[
            base_permission["FULL_ACCESS"]
        ],
    ),
    dict(
        name="Admin",
        permissions=[
            base_permission["CREATE_NEW_USER"],
            base_permission["READ_USER"],
            base_permission["UPDATE_USER_PROFILE"],
            base_permission["DELETE_USER"],
            base_permission["DELETE_USER_MFA"],
            base_permission["UPDATE_USER_MFA"],
            base_permission["UPDATE_USER_PASSWORD"],
            base_permission["DISABLE_USER"],
            base_permission["ENABLE_USER"],
            base_permission["UPDATE_ORGANIZATION"],
            base_permission["READ_ALL_LOGS"],
            base_permission["READ_ALL_USERS"],
            base_permission["MODIFY_USER_ROLE"],
            base_permission["MODIFY_USER_PERMISSIONS"],
        ],
    ),
    dict(
        name="User",
        permissions=[
            base_permission["READ_USER"],
            base_permission["UPDATE_USER_PROFILE"],
            base_permission["UPDATE_USER_PASSWORD"],
            base_permission["UPDATE_USER_MFA"],
        ],
    ),
]
