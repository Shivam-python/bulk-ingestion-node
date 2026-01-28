from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Hospital Bulk Processor</title>
            <meta http-equiv="refresh" content="3;url=/docs" />
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>👋 Welcome to Hospital Bulk Processing API</h1>
            <p>Redirecting you to API documentation...</p>
        </body>
    </html>
    """
