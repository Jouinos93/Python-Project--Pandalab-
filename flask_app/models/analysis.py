from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import appointment

class Analysis :
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_analysis(cls, data):
        query = """
        INSERT INTO analyses (name, price) 
        VALUES (%(name)s,%(price)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM analyses;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        analysis = []
        for row in results:
            analysis.append(cls(row))
        return analysis

        