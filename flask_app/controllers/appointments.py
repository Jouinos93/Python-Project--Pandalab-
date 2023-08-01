from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.patient import Patient
from flask_app.models import appointment
from flask_app.models.analysis import Analysis
from flask_app.models.admin import Admin
from flask import send_file

@app.route('/appointment')
def display_appointment():
    # if 'patient_id' in session:
    analysis = Analysis.get_all()
    print(analysis)
    return render_template("appointment.html", analysis = analysis)


# @app.route('/magazine/show')
# def new_magazine():
#     if 'user_id' in session:
#         return render_template("magazine_form.html")
#     return redirect('/')

@app.route('/appointment_create' ,methods=['POST'])
def creat_appointment():
    
        data = {
            **request.form,'patient_id':session['patient_id'], 'result': ""
        }
        print(session['patient_id'],'ùùùùùùùùùùùùùùù')
        appointment.Appointment.add_appointment(data)
        
        return redirect('/patient_dashboard')

@app.route("/appointment/<int:appointment_id>/update" ,methods=['POST'])
def update_appointment(appointment_id):
    print(request.form,'$$$$$'*55)
    data = {
         **request.form,
         'id' : appointment_id
    }
    appointment.Appointment.edit_appointment(data)
    return redirect('/technician_dashboard')

@app.route("/appointment/<int:appointment_id>/download_result" ,methods=['POST'])
def update_result(appointment_id):
    print(request.form,'$$$$$'*55)
    data = {
         **request.form,
         'id' : appointment_id
    }
    appointment.Appointment.upload_file(data)
    return redirect('/technician_dashboard')




@app.route('/appointment/<int:appointment_id>/destroy/')
def delete_appointment(appointment_id):
  
    if 'patient_id' in session:
        appointment.Appointment.delete({'id':appointment_id})
    return redirect('/patient_dashboard')
