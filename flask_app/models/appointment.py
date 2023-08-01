from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import patient
from flask_app.models import analysis
class Appointment :
    def __init__(self,data):
        self.id = data['id']
        self.analysis_id = data['analysis_id']
        self.patient_id = data['patient_id']
        self.admin_id = data['admin_id']
        self.date = data['date']
        self.prescription = data['prescription']
        self.status = data['status']
        self.result = data['result']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.admin = None


    @classmethod
    def add_appointment(cls, data):
        query = """
        INSERT INTO appointments (analysis_id,patient_id, date,prescription, result) 
        VALUES (%(analysis_id)s,%(patient_id)s,%(date)s,%(prescription)s,%(result)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def get_all(cls, data):
        query = """
            SELECT * FROM appointments
            JOIN analyses ON appointments.analysis_id = analyses.id
            WHERE appointments.patient_id = %(patient_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        list_of_appointment = []
        for row in results:
      
            this_appointment = cls(row)
            appointment_analysis = {
                **row,
                "created_at": row ["analyses.created_at"],
                "updated_at": row ["analyses.updated_at"],
                "id": row ["analyses.id"]
            }
            this_appointment.analysis = analysis.Analysis(appointment_analysis)
            list_of_appointment.append(this_appointment)
        
        return list_of_appointment
    
    @classmethod
    def get_by_patient_id(cls,data):
        query = """
        SELECT * FROM appointments
        WHERE appointments.patient_id = %(patient_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        list_of_appointment = []
        for row in results:
            list_of_appointment.append(cls(row))
        return list_of_appointment
    @classmethod
    def get_all_appointment(cls):
        query = """
        SELECT * 
        FROM appointments
        JOIN patients ON patients.id = appointments.patient_id
        JOIN analyses ON appointments.analysis_id = analyses.id

        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_appointments = []
        for row in results:
            one_appointment = (cls(row))

            patients_data = {
                **row,
                "created_at": row ["patients.created_at"],
                "updated_at": row ["patients.updated_at"],
                "id": row ["patients.id"]
            }
            analyses_data = {
                    **row,
                "created_at": row ["analyses.created_at"],
                "updated_at": row ["analyses.updated_at"],
                "id": row ["analyses.id"]
            }
            one_appointment.patients = patient.Patient(patients_data)
            one_appointment.analyses = analysis.Analysis(analyses_data)

            all_appointments.append(one_appointment)
        print(all_appointments,'**'*55)

        return all_appointments
    

    @classmethod
    def edit_appointment(cls,data):
        query = """
        UPDATE appointments SET date = %(date)s , status= %(status)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)  
    @classmethod
    def upload_file(cls,data):
        query = """
        UPDATE appointments SET result = %(result)s 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = """
        delete from appointments where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

       
    # def edit_recipe(cls, data):
    #     query = """
    #     UPDATE recipes SET name = %(name)s, description = %(description)s, instructions= %(instructions)s , date = %(date)s, under= %(under)s
    #     WHERE id = %(id)s;
    #     """
    #     return connectToMySQL(DATABASE).query_db(query, data)

