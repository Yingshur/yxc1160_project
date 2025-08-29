from app.decorators.management_functions import admin_only
from flask import render_template, redirect, url_for, flash, request
from app.mixed.emails import confirmation_email, approval_email, rejection_email
from app.models import User, Emperor, \
Image, TemporaryEmperor, TemporaryImage, LogBook
from app.forms import AllEmperorForm
from flask_login import current_user, login_required
from app.new_file import db

from app.mixed.version_control import to_csv, to_csv_overwrite
from app.mixed.images_handling import save_uploaded_images, approval_add_image, gallery_upload, gallery_upload_addition
from flask import Blueprint


emperor_bp = Blueprint("emperor_bp", __name__)


@emperor_bp.route("/manage_edits_additions_users/<int:id>", methods = ['GET', 'POST'], endpoint = "user_editing")
@login_required
def user_editing(id):
    emperors_edit_additions = db.session.get(TemporaryEmperor, id)
    form = AllEmperorForm(obj=emperors_edit_additions)
    form.edit.data = emperors_edit_additions.id
    return render_template("user_info.html", emperors_edit_additions=emperors_edit_additions, form_open = False, title="Macedonian dynasty", new_form=form)


@emperor_bp.route("/dynasties", endpoint ="dynasties")
def dynasties():
    return render_template('dynasties.html', title = "Dynasties")

@emperor_bp.route("/dynasties/macedonians", methods=['GET','POST'], endpoint = "macedonians")
def macedonians():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('macedonians.html', title = "Macedonian dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Macedonian Dynasty (867-1056)")


@emperor_bp.route("/dynasties/doukas", methods=['GET','POST'], endpoint = "doukas")
def doukas():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Doukas').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('doukas.html', title = "Doukas dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Doukas Dynasty (1059-1081)")


@emperor_bp.route("/dynasties/komnenos", methods=['GET','POST'], endpoint = "komnenos")
def komnenos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Komnenos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('komnenos.html', title = "Komnenos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Komnenos Dynasty (1081-1185)")


@emperor_bp.route("/dynasties/angelos", methods=['GET','POST'], endpoint = "angelos")
def angelos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Angelos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('angelos.html', title = "Angelos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Angelos Dynasty (1185-1204)")


@emperor_bp.route("/dynasties/palaiologos", methods=['GET','POST'], endpoint = "palaiologos")
def palaiologos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Palaiologos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('palaiologos.html', title = "Palaiologos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Palaiologos Dynasty (1259-1453)")


@emperor_bp.route('/edit_emperor_users/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_emperor_users")
@login_required
def edit_emperor_users(id):
    emperor_first_users = db.session.get(TemporaryEmperor, id)
    form = AllEmperorForm()
    if request.method == "GET":
        form = AllEmperorForm(obj=emperor_first_users, data={"edit": emperor_first_users.id})
    if form.validate_on_submit():
            emperor_new_edit_users = db.session.get(TemporaryEmperor, int(form.edit.data))
            form.populate_obj(emperor_new_edit_users)
            if form.portrait.data:
                save_uploaded_images(file=form.portrait.data, obj_id=emperor_new_edit_users.id,
                                     field_name="temporary_emperor_id",
                                     model=TemporaryImage, form_data=form, temporary=True)
            if emperor_first_users.status != "Pending":
                emperor_new_edit_users.status = "Pending"
                confirmation_email(id=emperor_first_users.id)
            db.session.commit()
            return redirect(url_for('emperor_bp.user_editing', id=emperor_first_users.id))
    return render_template("user_info.html", emperors_edit_additions = emperor_first_users, new_form = form, form_open = True, title = "Editing requests")


@emperor_bp.route("/manage_edits/edit_info_emperor/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_info_emperor")
@admin_only
@login_required
def edit_info_emperor(id):
    emperor_edit = db.session.get(TemporaryEmperor, id)
    return render_template("edit_info_emperor.html", emperor_edit = emperor_edit, title = "Preview")


@emperor_bp.route("/manage_additions/add_info_emperor/<int:id>", methods = ['GET', 'POST'], endpoint = "add_info_emperor")
@admin_only
@login_required
def add_info_emperor(id):
    emperor_add = db.session.get(TemporaryEmperor, id)
    return render_template("add_info_emperor.html", emperor_add = emperor_add, title = "Preview")



@emperor_bp.route("/approve_emperor_add/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_emperor_add")
@admin_only
def approve_emperor_add(id):
    add_emperor = db.session.get(TemporaryEmperor, id)
    column_names = [column.name for column in Emperor.__table__.columns if column.name != "id"]
    new_emperor = Emperor(**{column: getattr(add_emperor, column) for column in column_names if hasattr(add_emperor, column)})
    user = db.session.query(User).filter_by(username = add_emperor.username).first()
    db.session.add(new_emperor)
    db.session.commit()
    new_log_12 = LogBook(original_id=new_emperor.id, title=new_emperor.title,
                         username=current_user.username)
    db.session.add(new_log_12)
    if add_emperor.temporary_images:
        approval_add_image(add_emperor, obj_id=new_emperor.id, field_name="emperor_id", model=Image)
    approval_email(user_email=user.email, emperor_title=new_emperor.title)
    db.session.delete(add_emperor)
    to_csv(current_user.username, new_emperor.title)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('admin_bp.manage_additions'))


@emperor_bp.route("/reject_emperor_add_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "reject_emperor_add_edit")
def reject_emperor_add_edit(id):
    add_emperor = db.session.get(TemporaryEmperor, id)
    add_emperor.status = "Reject"
    user = db.session.query(User).filter_by(username = add_emperor.username).first()
    rejection_email(user_email=user.email, emperor_title=add_emperor.title)
    db.session.commit()
    return redirect(request.referrer)


@emperor_bp.route("/approve_emperor_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_emperor_edit")
@admin_only
def approve_emperor_edit(id):
    try:
        edit_emperor = db.session.get(TemporaryEmperor, id)
        emperor_new_edit = db.session.get(Emperor, int(edit_emperor.old_id))
        column_names = [column.name for column in Emperor.__table__.columns if column.name not in ("id", "old_id")]
        for column in column_names:
            setattr(emperor_new_edit, column, getattr(edit_emperor, column))
        user = db.session.query(User).filter_by(username=edit_emperor.username).first()
        new_log_14 = LogBook(original_id=emperor_new_edit.id, title=emperor_new_edit.title,
                             username=current_user.username)
        db.session.add(new_log_14)
        to_csv(current_user.username, emperor_new_edit.title)
        if edit_emperor.temporary_images:
            approval_add_image(edit_emperor, obj_id=emperor_new_edit.id, field_name="emperor_id", model=Image)
        approval_email(user_email=user.email, emperor_title=edit_emperor.title)
        db.session.delete(edit_emperor)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    except Exception as e:
        flash("Article no longer available due to version change!", "warning")
    return redirect(url_for('admin_bp.manage_edits'))


@emperor_bp.route("/delete_emperors_/<int:id>", methods = ['GET', 'POST'], endpoint = "delete_emperors_")
@admin_only
def delete_emperors_(id):
    delete_emperors_ = db.session.get(Emperor, id)
    to_csv(current_user.username, delete_emperors_.title)
    if delete_emperors_.images:
        delete_images_ = delete_emperors_.images[0]
        db.session.delete(delete_images_)
    db.session.delete(delete_emperors_)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(request.referrer)


@emperor_bp.route("/dynasties/macedonians/<int:id>", methods=['GET','POST'], endpoint = "macedonian_emperors")
def macedonian_emperors(id):
    #m_e = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    m_e = db.session.get(Emperor, id)
    form = AllEmperorForm(obj=m_e)
    form.edit.data = m_e.id
    if m_e.dynasty == "Macedonian":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Macedonian dynasty",new_form=form)
    elif m_e.dynasty == "Doukas":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Doukas dynasty",new_form=form)
    elif m_e.dynasty == "Angelos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Angelos dynasty",
                               new_form=form)
    elif m_e.dynasty == "Komnenos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Komnenos dynasty",
                               new_form=form)
    elif m_e.dynasty == "Palaiologos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Palaiologos dynasty",
                               new_form=form)
    else:
        return redirect(request.referrer)



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
            if form.portrait.data:
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                save_uploaded_images(file=form.portrait.data, obj_id=id_data.id, field_name="temporary_emperor_id",
                                     model=TemporaryImage, form_data=form, temporary=True)

                db.session.commit()
                confirmation_email(id=temporary_edit.id)
                return redirect(url_for(redirect_))

        else:
            return redirect(url_for(redirect_))
    return render_template(template, title = page_title, macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = article_title)



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
            if form.portrait.data:
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                save_uploaded_images(file=form.portrait.data, obj_id=id_data.id, field_name = "temporary_emperor_id",model = TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id=id)
            return redirect(url_for('emperor_bp.macedonian_emperors', id=emperor_first.id))
    return render_template("macedonian_emperors.html", id=emperor_first.id, form_open = True, m_e = emperor_first, new_form = form, title = "Dynasties")


@emperor_bp.route("/admin_delete_emperor/<int:id>", methods = ['GET', 'POST'], endpoint = "admin_delete_emperor")
@admin_only
def admin_delete_emperor(id):
    delete_emperor_temporary = db.session.get(TemporaryEmperor, id)
    if delete_emperor_temporary.temporary_images:
        delete_image_temporary = delete_emperor_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_emperor_temporary)
    db.session.commit()
    return redirect(request.referrer)
