from web import create_app

# Create Flask app
app = create_app()

# Serverless entrypoint
def handler(request, response):
    return app(request.environ, response.start_response)