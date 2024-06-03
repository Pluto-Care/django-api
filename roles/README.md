# Roles and Permissions

## How it works

-   A user can be assigned to a single role and additionally granted multiple permissions.
-   A role can have multiple permissions.
-   A permission granted explicitly to a user will take precedence over permissions granted through the role.

## API

These are base functions and do not check if the user accessing the function has the required permissions. **Please check the user permissions before calling these functions.**

| Function                                         | Note                                               |
| ------------------------------------------------ | -------------------------------------------------- |
| `assign_role_to_user(user, role_id)`             | Check `base_permission['MODIFY_USER_ROLE']`        |
| `assign_permission_to_user(user, permission_id)` | Check `base_permission['MODIFY_USER_PERMISSIONS']` |
| `check_user_for_permission(user, permission_id)` |                                                    |
| `has_full_access(user)`                          |                                                    |

## DRF Permissions

-   `HasFullAccess`
-   `HasPermission(base_permission['READ_USER'])`
