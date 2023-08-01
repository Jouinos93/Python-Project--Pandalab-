from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import patient

class Feedback :
    def __init__(self,data):
        self.id = data['id']
        self.patient_id = data['patient_id']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    
    @classmethod
    def new_feedback(cls, data):
        query = """
                INSERT INTO feedbacks (patient_id, description)
                VALUES (%(patient_id)s, %(description)s)
                """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_all_feedbacks(cls):
        query = """
                SELECT * FROM feedbacks
                JOIN patients ON patients.id = feedbacks.patient_id;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        all_feedbacks = []
        for row in results:
            one_feedback = cls(row)
            patients_data = {
                **row,
                "created_at": row ["patients.created_at"],
                "updated_at": row ["patients.updated_at"],
                "id": row ["patients.id"]
            }
            one_feedback.patients = patient.Patient(patients_data)
            all_feedbacks.append(one_feedback)
            print(all_feedbacks,'$ù$ù$ù$ù'*44)
        return all_feedbacks
    