from app import app, schedule_start
import os

if __name__ == '__main__':
    with app.app_context():
        schedule_start()
        app.run(port=5807)


    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7899)))

