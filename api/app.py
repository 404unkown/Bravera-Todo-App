from web import create_app
from mangum import Mangum  # For serverless support on Vercel

# Create Flask app
app = create_app()

# Wrap Flask app for Vercel serverless function
handler = Mangum(app)
