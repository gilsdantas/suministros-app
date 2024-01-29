from src import create_app
from src.models import build_sample_db

# config_name = os.getenv("FLASK_CONFIG")
config_name = "development"
app = create_app(config_name)

if __name__ == "__main__":
    build_sample_db()
    app.run(debug=True)
