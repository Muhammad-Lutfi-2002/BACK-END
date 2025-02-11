# models.py
from datetime import datetime
from database import Database

class UserModel:
    @staticmethod
    def create_user(cursor, user_data):
        sql = """INSERT INTO tenants (first_name, last_name, email, phone, 
                identity_number, emergency_contact, emergency_phone) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (
            user_data['first_name'],
            user_data['last_name'],
            user_data['email'],
            user_data['phone'],
            user_data['identity_number'],
            user_data.get('emergency_contact'),
            user_data.get('emergency_phone')
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

class PropertyModel:
    @staticmethod
    def get_all_properties(cursor, filters=None):
        query = """
            SELECT p.*, GROUP_CONCAT(pi.image_url) as images 
            FROM properties p 
            LEFT JOIN property_images pi ON p.property_id = pi.property_id 
            WHERE 1=1
        """
        params = []
        
        if filters and 'city' in filters:
            query += " AND p.city = %s"
            params.append(filters['city'])
        
        if filters and 'property_type' in filters:
            query += " AND p.property_type = %s"
            params.append(filters['property_type'])
        
        query += " GROUP BY p.property_id"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def create_property(cursor, property_data):
        sql = """INSERT INTO properties (property_name, address, city, postal_code,
                property_type, bedrooms, bathrooms, size_sqm, monthly_rent,
                is_furnished, description, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            property_data['property_name'],
            property_data['address'],
            property_data['city'],
            property_data['postal_code'],
            property_data['property_type'],
            property_data['bedrooms'],
            property_data['bathrooms'],
            property_data['size_sqm'],
            property_data['monthly_rent'],
            property_data.get('is_furnished', 0),
            property_data.get('description'),
            property_data.get('status', 'Available')
        )
        cursor.execute(sql, values)
        return cursor.lastrowid