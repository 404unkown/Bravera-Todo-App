from web import create_app
from mangum import Mangum  # wrap Flask for serverless

app = create_app()

# serverless handler for Vercel
handler = Mangum(app)
