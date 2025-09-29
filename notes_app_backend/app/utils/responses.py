from flask import jsonify


OCEAN_PROFESSIONAL_THEME = {
    "name": "Ocean Professional",
    "palette": {
        "primary": "#2563EB",
        "secondary": "#F59E0B",
        "success": "#F59E0B",
        "error": "#EF4444",
        "background": "#f9fafb",
        "surface": "#ffffff",
        "text": "#111827",
        "gradient": "from-blue-500/10 to-gray-50",
    },
    "style": "Modern clean API response with clear structure and subtle ocean accents.",
}


def themed_payload(status: str, message: str, data=None, meta=None):
    """
    Build a standardized themed response payload.

    Args:
        status: 'success' or 'error'
        message: Human-friendly short description
        data: Optional data payload
        meta: Optional metadata dict

    Returns:
        dict that can be returned as JSON response
    """
    payload = {
        "theme": OCEAN_PROFESSIONAL_THEME["name"],
        "style": OCEAN_PROFESSIONAL_THEME["style"],
        "palette": OCEAN_PROFESSIONAL_THEME["palette"],
        "status": status,
        "message": message,
        "data": data,
        "meta": meta or {},
    }
    return payload


def success(message: str, data=None, meta=None, status_code: int = 200):
    """Return a standardized success response."""
    return jsonify(themed_payload("success", message, data, meta)), status_code


def error(message: str, status_code: int = 400, errors=None, meta=None):
    """Return a standardized error response."""
    payload = themed_payload("error", message, data=None, meta=meta)
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), status_code
