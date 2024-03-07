from .db import db

# Define the User model
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    user_type = db.StringField(required=True, choices=['customer', 'tailor'])


# Define the Customer model
class Customer(db.Document):
    user = db.ReferenceField(User, required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    contact = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    gender =  db.StringField(required = True)
    


# Define the Tailor model
class Tailor(db.Document):
    user = db.ReferenceField(User, required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    contact = db.StringField(required=True)
    shop_name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    address = db.StringField()
    specialization = db.StringField(required=True)



from mongoengine import Document, ReferenceField, StringField, FloatField

class Order(db.Document):
    customer = ReferenceField(Customer, required=True)
    tailor = ReferenceField(Tailor, required=True)
    name = StringField(required=True)
    phone = StringField(requred = True)
    category = StringField(required=True)
    fabric_type = StringField(required = True)
    garment_style = StringField(required = True)
    color_type = StringField(required = True)
    kuff_style = StringField(required = True)

    


class Measurement(db.Document):
    order = ReferenceField(Order, required = True)
    customer = ReferenceField(Customer, required=True)
    tailor = ReferenceField(Tailor, required=True)
    shirt_length = FloatField(required = True)
    chest = FloatField()
    shoulder_width = FloatField()
    arm_length = FloatField()
    wrist = FloatField()    
    waist = FloatField()
    hip = FloatField()
    seat = FloatField()
    pants_length = FloatField(required = True)
    # Add other fields as needed for the measurement, e.g., height, weight, etc.



# Define the DeliveryAddress model
class DeliveryAddress(db.Document):
    customer = ReferenceField(Customer, required=True)
    tailor = ReferenceField(Tailor, required=True)
    city = db.StringField(required=True)
    country = db.StringField()
    home_town = db.StringField()
    zip_code = db.StringField(required=True)
    address1 = db.StringField(required=True)
    address2 = db.StringField()
