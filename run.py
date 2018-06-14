import os
from app import create_app

app = create_app(config_name="development")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run()
