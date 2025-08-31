from locust import HttpUser, task, between
from locust.exception import StopUser
from testing import response
import uuid


class Testing(HttpUser):
    wait_time = between(1, 6)
    def on_start(self):
        self.login()
    def login(self):
        payload = {"email": "chenyingshu1234@gmail.com",
                   "pw": "Chenxh1031!"}
        with self.client.post("login", data=payload, catch_response=True) as response:
            if "gone wrong" in response.text:
                response.failure("Not working")
                raise StopUser()
            else:
                print(f"login status: {response.status_code}")
    @task
    def index(self):
        self.client.get("/")

    @task
    def login_page(self):
        self.client.get("/login")

    @task
    def add_test(self):
        title = f"{uuid.uuid4()}_test"
        payload = {
            'title': title,
            'in_greek': '',
            'birth': 'test',
            'death': 'test',
            'reign': 'test',
            'life': "test",
            'dynasty': "test",
            'reign_start': 1,
            'ascent_to_power': 'test',
            'references': 'test',
            'edit': -1
        }
        with self.client.post("/add_new_emperor", data=payload, catch_response=True) as response:
            if response.status_code != 200 and response.status_code != 302:
                if "gone wrong" in response.text:
                    response.failure("Not working")
            else:
                    response.success()
    @task
    def edit_test(self):
        title = f"{uuid.uuid4()}_test"

        payload = {
            'title': title,
            'in_greek': '',
            'birth': 'test',
            'death': 'test',
            'reign': 'test',
            'life': "test",
            'dynasty': "test",
            'reign_start': 1,
            'ascent_to_power': 'test',
            'references': 'test',
            'edit': 1
        }
        with self.client.post(f"/edit_emperor/{1}", data=payload, catch_response=True) as response:
            if response.status_code != 200 and response.status_code != 302:
                if "gone wrong" in response.text:
                    response.failure("Not working")
            else:
                    response.success()




"""This section of code was used for "locust" stress testing
@emperor_bp.route('/edit_emperor/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_emperor")
@login_required
def edit_emperor(id):
    emperor_first = db.session.get(Emperor, id)
    form = AllEmperorForm()
    if request.method == "GET":
        form = AllEmperorForm(obj=emperor_first, data={"edit": emperor_first.id})
    if form.validate_on_submit():
        if current_user.role == "Admin":
            #This part is designed for "locust" stress testing
            if "test" not in form.title.data:
                emperor_new_edit = db.session.get(Emperor, int(form.edit.data))
                form.populate_obj(emperor_new_edit)
                new_log_2 = LogBook(original_id=emperor_new_edit.id, title=emperor_new_edit.title,
                                    username=current_user.username)
                to_csv(current_user.username, emperor_new_edit.title)
                db.session.add(new_log_2)
                if form.portrait.data:
                    save_uploaded_images(file=form.portrait.data, obj_id=emperor_new_edit.id, field_name="emperor_id", model=Image)
                db.session.commit()
            else:
                emperor_new_edit = db.session.get(Emperor, int(form.edit.data))
                form.populate_obj(emperor_new_edit)
            to_csv_overwrite(current_user.username)
            return redirect(url_for('emperor_bp.macedonian_emperors', id=emperor_first.id))
        else:
            column_names = [column.name for column in TemporaryEmperor.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryEmperor(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryEmperor).filter_by(username=current_user.username).order_by(
                TemporaryEmperor.id.desc()).first()
            if form.portrait.data:
                save_uploaded_images(file=form.portrait.data, obj_id=id_data.id, field_name = "temporary_emperor_id",model = TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id=id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for('emperor_bp.macedonian_emperors', id=emperor_first.id))
    return render_template("macedonian_emperors.html", id=emperor_first.id, form_open = True, m_e = emperor_first, new_form = form, title = "Dynasties")
"""




"""This section  of code was also used for "locust" stress testing
@emperor_bp.route("/add_new_emperor/<string:dynasty>", methods = ['POST'], endpoint = "add_new_emperor")
@login_required
def add_new_emperor(dynasty):
    form = AllEmperorForm()
    if dynasty == "Macedonian":
        template = "macedonians.html"
        redirect_ = "emperor_bp.macedonians"
        page_title = "Macedonian dynasty"
        article_title = "Macedonian Dynasty (867-1056)"
    elif dynasty == "Doukas":
        template = "doukas.html"
        redirect_ = "emperor_bp.doukas"
        page_title = "Doukas dynasty"
        article_title = "Doukas dynasty (1059-1081)"
    elif dynasty == "Komnenos":
        template = "komnenos.html"
        redirect_ = "emperor_bp.komnenos"
        page_title = "Komnenos dynasty"
        article_title = "Komnenos dynasty (1081-1185)"
    elif dynasty == "Angelos":
        template = "angelos.html"
        redirect_ = "emperor_bp.angelos"
        page_title = "Angelos dynasty"
        article_title = "Angelos dynasty (1085-1204)"
    elif dynasty == "Palaiologos":
        template = "palaiologos.html"
        redirect_ = "emperor_bp.palaiologos"
        page_title = "Palaiologos dynasty"
        article_title = "Palaiologos dynasty (1259-1453)"
    else:
        return None
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = dynasty).all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin" :
            column_names = [column.name for column in Emperor.__table__.columns if column.name != "id"]
            new_emperor = Emperor(**{column: getattr(form, column).data for column in column_names if hasattr(form, column)})
            db.session.add(new_emperor)
            #This function is designed for "locust" stress test
            if "test" not in form.title.data:
                db.session.commit()
                id_data = db.session.query(Image).first()
                new_log_300000 = LogBook(original_id=new_emperor.id, title=new_emperor.title,
                                         username=current_user.username)
                to_csv(current_user.username, new_emperor.title)
                db.session.add(new_log_300000)
                db.session.commit()
            else:
                db.session.commit()
                db.session.delete(new_emperor)
                db.session.commit()
            # print(form.portrait.data.filename)
            if form.portrait.data and "test" not in form.title.data:
                save_uploaded_images(file=form.portrait.data, obj_id=new_emperor.id, field_name="emperor_id",
                                     model=Image)
                db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for(redirect_))

        elif current_user.role != "Admin" and "test" not in form.title.data:
            column_names = [column.name for column in TemporaryEmperor.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryEmperor(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryEmperor).filter_by(username=current_user.username).order_by(
                TemporaryEmperor.id.desc()).first()
            if form.portrait.data:
                save_uploaded_images(file=form.portrait.data, obj_id=id_data.id, field_name="temporary_emperor_id",
                                     model=TemporaryImage, form_data=form, temporary=True)
                db.session.commit()
            confirmation_email(id=id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for(redirect_))

        else:
            return redirect(url_for(redirect_))
    return render_template(template, title = page_title, macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = article_title)
"""

