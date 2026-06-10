from fastapi import HTTPException


ROLES = {
    "admin": [
        "view_logs",
        "manage_users",
        "view_dashboard"
    ],

    "security_analyst": [
        "view_logs",
        "view_dashboard"
    ],

    "user": [
        "basic_access"
    ]
}


def check_permission(role: str, permission: str):

    if role not in ROLES:
        raise HTTPException(
            status_code=403,
            detail="Invalid role"
        )

    if permission not in ROLES[role]:
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )

    return True