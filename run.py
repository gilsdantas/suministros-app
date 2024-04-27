# Built-in imports
import os

# Third-party imports
# Local imports
from src import create_app
from src.utils.utils import build_sample_db

config_name = os.getenv("FLASK_CONFIG", "development")

app = create_app(config_name)

if __name__ == "__main__":
    build_sample_db()
    app.run(debug=True)
