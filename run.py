#!/usr/bin/env python3
import os
from app import create_app
from app.models import db  # Import db to access create_all

app = create_app()

# Automatically create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
