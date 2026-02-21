from app.core.error.error_types import ErrorType


def get_http_status(error_type: ErrorType) -> int:
    name = error_type.name

    if "_200_" in name:
        return 200
    if "_201_" in name:
        return 201
    if "_400_" in name:
        return 400
    if "_401_" in name:
        return 401
    if "_403_" in name:
        return 403
    if "_404_" in name:
        return 404
    if "_500_" in name:
        return 500

    return 200