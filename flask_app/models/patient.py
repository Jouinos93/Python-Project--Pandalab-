


from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Patient :
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.age = data['age']
        self.gender = data['gender']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    
    @classmethod
    def create_patient(cls, data):
        query = """
        INSERT INTO patients (first_name, last_name, email, password, age, gender, phone_number) 
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(age)s,%(gender)s,%(phone_number)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    # def __repr__(self) -> str:
    #     return f"{self.first_name}--{self.last_name}--{self.email}"
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM patients WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM patients WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return False
    
    # @classmethod
    # def update_p(cls,data):
    #     query = """UPDATE patients 
    #             SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,password=%(password)s 
    #             WHERE id = %(id)s;"""
    #     return connectToMySQL(DATABASE).query_db(query,data)
    

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])< 3:
            flash("First Name must be at least 3 caracters","reg")
            is_valid = False

        if len(data['last_name'])< 3:
            flash("Last name is required","reg")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","reg")
            is_valid = False
        elif Patient.get_by_email({'email':data['email']}):
            flash("Email address already used, try login","reg")
            is_valid = False

        if len(data['password'])< 8:
            flash("Password too short","reg")
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("Password does not match ","reg")
            is_valid = False

        if len(data['age']) < 1:
            flash("age is required","reg")
            is_valid = False

        if len(data['phone_number']) < 7:
            flash("phone number is required","reg")
            is_valid = False

        return is_valid
    
    # @staticmethod
    # def validate_1(data):
    #     is_valid = True
    #     if len(data['first_name'])< 3:
    #         flash("First Name must be at least 3 caracters","va")
    #         is_valid = False
    #     if len(data['last_name'])< 3:
    #         flash("Last name is required","va")
    #         is_valid = False
    #     if not EMAIL_REGEX.match(data['email']): 
    #         flash("Invalid email address!","va")
    #         is_valid = False
    #     if len(data['password'])< 8:
    #         flash("Password too short","reg")
    #         is_valid = False
        
    #     return is_valid
    
