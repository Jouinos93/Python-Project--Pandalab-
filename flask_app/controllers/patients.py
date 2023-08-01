from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.patient import Patient
from flask_app.models.appointment import Appointment
from flask_app.models.feedback import Feedback
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def home():
    # all_appointment = Appointment.get_all({'patient_id':session['patient_id']})
    all_feedbacks = Feedback.get_all_feedbacks()

    return render_template("home.html",all_feedbacks=all_feedbacks)

@app.route('/specialities')
def specialities():
    return render_template("specialities.html")

@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/patient_reg')
def patient_reg():
    if 'patient_id' in session:
        return redirect("/patient_dashboard")
    return render_template("registration.html")

@app.route('/patient_register', methods=['POST'])
def create_patient():
    print(request.form)
    if(Patient.validate(request.form)):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            **request.form,'password':pw_hash
            }
        patient_id = Patient.create_patient(data)
        session['patient_id'] = patient_id
        return redirect('/patient_dashboard')
    return redirect('/patient_reg')
    




@app.route('/patient_login', methods=['POST'])
def login_patient():
    patient_from_db = Patient.get_by_email({'email':request.form['email']})
    if(patient_from_db):
        if not bcrypt.check_password_hash(patient_from_db.password, request.form['password']):
            flash("Invalid Password","log")
            return redirect('/patient_log')
        session['patient_id'] = patient_from_db.id
        return redirect('/patient_dashboard')
    flash("Invalid Email","log")
    return redirect('/patient_log')
    # if(Patient.validate(request.form)):
    #     pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #     print(pw_hash)
    #     data = {
    #         **request.form,'password':pw_hash
    #     }
    #     patient_id = Patient.create_patient(data)
    #     session['patient_id'] = patient_id
    #     return redirect('/patient_dashboard')
    # return redirect('/patient_log')


@app.route('/patient_dashboard')
def dashboard():
    if not 'patient_id' in session:
        return redirect("/patient_register")
    
    patient = Patient.get_by_id({'id':session['patient_id']}) 
    all_appointment = Appointment.get_all({'patient_id':session['patient_id']})
    return render_template("patient_dashboard.html" , patient = patient, all_appointment=all_appointment )


@app.route('/patient_log')
def patient_log():
    if 'patient_id' in session:
        return redirect("/patient_dashboard")
    return render_template("login.html")

# @app.route('/patient/<patient_id>/account')
# def account(patient_id):
#     if 'patient_id' in session:
#         current_patient = Patient.get_by_id({"id": session["patient_id"]})
#         return render_template('account_patient.html', user = current_patient)
#     return redirect('/')

@app.route('/patient/<patient_id>/update',methods=['POST'])
def update_p(patient_id):
    if(Patient.validate_1(request.form)):
       Patient.update_p({
           **request.form,
           "id" : patient_id
       })
       return redirect('/patient_dashboard')
    return redirect('/patient/'+str(patient_id)+'/account')



@app.route('/create_feedback' , methods=['POST'])
def create_feedback():
    data = {
        **request.form,
        'patient_id' : session['patient_id']
    }
    
    Feedback.new_feedback(data)

    return redirect("/patient_dashboard")

# @app.route('/')
# def show_all_feedback():
#     all_feedbacks = Feedback.get_all_feedbacks()

#     return render_template('home.html',all_feedbacks = all_feedbacks)











@app.route('/logout_p')
def logout():
    session.clear()
    return redirect('/')
