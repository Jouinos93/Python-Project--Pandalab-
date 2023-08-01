from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.patient import Patient
from flask_app.models.admin import Admin
from flask_app.models.appointment import Appointment

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route('/admin_log')
def admin_log():
    if 'admin_id' in session:
        data ={
            'id': session['admin_id']
        }
        admin = Admin.get_by_id_admin(data)
        if admin.type == "manager":
            return redirect('/manager_dashboard')
        elif admin.type == "technician":
            return redirect('/technician_dashboard')
    return render_template("login_admin.html")



@app.route('/admin_login', methods=['POST'])
def login_admin():
    admin_from_db = Admin.get_by_email_admin({'email':request.form['email']})
    print(admin_from_db)
    if(admin_from_db):
        if not (admin_from_db.password == request.form['password']):
            flash("Invalid Password","log")
            return redirect('/')
        session['admin_id'] = admin_from_db.id
    
        if admin_from_db.type == "manager":
            return redirect('/manager_dashboard')
        elif admin_from_db.type == "technician":
            
            return redirect('/technician_dashboard')
    flash("Invalid Email","log")
    return redirect('/admin_log')


@app.route('/manager_dashboard')
def admin_1():
    all_appointments = Appointment.get_all_appointment()
    return render_template("manager_dashboard.html" ,all_appointments=all_appointments )

@app.route('/technician_dashboard')
def admin_2():
    all_appointments = Appointment.get_all_appointment()
    
    print(all_appointments,'$$$'*55)
    return render_template("technician_dashboard.html",all_appointments=all_appointments)


@app.route('/logout_m')
def logout_m():
    session.clear()
    return redirect('/')

@app.route('/logout_t')
def logout_t():
    session.clear()
    return redirect('/')

