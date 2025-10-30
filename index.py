from mangum import Mangum
from web import create_app

app = create_app()
handler = Mangum(app)  # Vercel expects a handler for serverless

# Optional: for local testing
if __name__ == "__main__":
    app.run(debug=True)