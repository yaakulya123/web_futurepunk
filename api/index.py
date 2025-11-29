import sys
import os

# Add parent directory and web_app to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web_app'))

from web_app.app import app

# Vercel serverless function handler
def handler(request, context):
    return app(request, context)
