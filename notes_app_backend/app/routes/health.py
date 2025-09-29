from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """Simple health check endpoint to validate service availability."""
    @blp.doc(
        summary="Health check",
        description="Returns a simple JSON indicating the service is healthy.",
        operationId="healthCheck",
        tags=["Health"],
        responses={200: {"description": "Service healthy"}},
    )
    def get(self):
        return {"message": "Healthy"}
