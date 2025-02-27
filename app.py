import os

import dotenv
from flask import Flask, request, send_from_directory
from sqlalchemy import inspect

from extensions import db
from models.admin import Admin
from models.file import File
from models.note import Note
from models.user import User
from routes.about import about_bp
from routes.admin import admin_bp, init_admin_db

dotenv.load_dotenv()
app = Flask(__name__, template_folder="frontend/dist", static_folder="frontend/dist")

app.secret_key = os.getenv('SECRET_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boko_hacks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_file_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(static_file_path) and os.path.isfile(static_file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def setup_database():
    """Setup database and print debug info"""
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            print("No existing tables found. Creating new tables...")
            db.create_all()

            init_admin_db()
        else:
            print("Existing tables found:", existing_tables)

            db.create_all()
            print("Updated schema with any new tables")

        for table in ["users", "notes", "admin_credentials", "files"]:
            if table in inspector.get_table_names():
                print(f"\n{table.capitalize()} table columns:")
                for column in inspector.get_columns(table):
                    print(f"- {column['name']}: {column['type']}")
            else:
                print(f"\n{table} table does not exist!")

if __name__ == "__main__":
    setup_database()
    app.run(debug=False)
