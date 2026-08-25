from waitress import serve
from countycivictrack.wsgi import application
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

application = WhiteNoise(
    application,
    root="staticfiles",
    prefix="static/"
)

application.add_files(
    "media",
    prefix="media/"
)

print("Starting Civic System...")
print("Open: http://127.0.0.1:8000")

serve(
    application,
    host="0.0.0.0",
    port=8000
)