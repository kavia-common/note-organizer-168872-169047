from app import app

# PUBLIC_INTERFACE
def create_app():
    """Factory to return the Flask app instance."""
    return app

if __name__ == "__main__":
    # Bind to 0.0.0.0:3001 for container readiness and external access
    app.run(host="0.0.0.0", port=3001)
