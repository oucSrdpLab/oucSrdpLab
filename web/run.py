from apps import app
from apps import config

if __name__ == "__main__":
    app.run(config.HOST, config.PORT)
