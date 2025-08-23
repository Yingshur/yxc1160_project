from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from app.new_file import db
from app.models import User, Verification
from app.mixed.total_backup import to_csv_total
from app import app

def deleting_expired_auto():
    with app.app_context():
        from datetime import datetime, timezone, timedelta
        from app.models import User, Verification
        from app.new_file import db
        the_threshold = datetime.now(timezone.utc) - timedelta(minutes=9)
        all_record = Verification.query.all()
        for each_record in all_record:
            try:
                raw = each_record.created_at.replace(" ", "T")
                creation_time = datetime.fromisoformat(raw)
                if creation_time < the_threshold:
                    db.session.delete(each_record)
            except Exception as e:
                #db.session.rollback()
                print(f"Invalid format: {each_record.created_at}-{e}")
        db.session.commit()


def schedule_start():
    schedule = BackgroundScheduler()
    schedule.add_job(deleting_expired_auto, 'interval', minutes = 10, misfire_grace_time=2)
    schedule.add_job(to_csv_total, 'interval', minutes = 720, misfire_grace_time=2)
    schedule.start()


