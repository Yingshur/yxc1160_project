from app import app
from app.mixed.scheduler import schedule_start
import os
if __name__ == '__main__':
    with app.app_context():
        schedule_start()
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 6089)))


    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7899)))

