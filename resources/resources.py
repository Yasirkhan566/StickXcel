from flask import request, jsonify, abort, session, Response
from flask_restful import Resource
from database.models import User, Customer, Tailor, Order, Measurement, DeliveryAddress




# Define the UserRegisterResource
class UserRegisterResource(Resource):
    def post(self):
        # Parse the request data
        print("\n\n\n\n")
        data = request.get_json()
        print(data, '\n\n\n')
        # Check if the username is already taken
        existing_user = User.objects.filter(username=data['username']).first()
        if existing_user:
            return {'message': 'Username is already taken. Please choose a different username.'}, 409

        # Create a new user
        user = User(username=data['username'], password=data['password'], user_type=data['user_type'])
        user.save()

        return {'message': 'User registered successfully.', 'user_id': str(user.id)}, 201




class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        # Find the user with the provided username
        user = User.objects.filter(username=username).first()
        if not user or user.password != password:
            return {'message': 'Invalid credentials'}, 401
        print(user.id, '\n\n\n\n\n')
        if str(user.user_type) == 'customer':
            print(user.id)
            customer = Customer.objects.filter(user = user).first()
            if customer:
                session['customer_id'] = str(customer.id)
                return {'customer_id': str(customer.id)}
        elif str(user.user_type) == 'tailor':
            print(user.id)
            tailor = Tailor.objects.filter(user = user).first()
            if tailor:
                session['tailor_id'] = str(tailor.id)
                return {'tailor_id': str(tailor.id)}
        session['user_id'] = str(user.id)
        return {'user_type': str(user.user_type)}, 200

class AllTailors(Resource):
    def get(self):
        tailors = Tailor.objects()
        return Response(tailors.to_json(), mimetype="application/json", status=200)



# Customer Resource
class CustomerResource(Resource):
    def post(self):
        try:
            customer = request.get_json()
            print("123")
            print(customer)
            customer['user'] = session.get('user_id')
            print(customer)
            customer = Customer(**customer)
            customer.save()
            print("submitted")
            session['customer_id'] = str(customer.id)
            return {'id': str(customer.id)}, 200
        except:
            return {"message": 'Not completed'}, 500

    def get(self):
        # Get the authenticated user's ID
        id = session.get("customer_id")
        # Retrieve the customer from the database
        customer = Customer.objects.filter(id = id).first()
        print(customer)
        if not customer:
            abort(404, message='Customer not found')
        return customer.to_json(), 200

    def put(self):
        # Get the authenticated user's ID
        user_id = session.get('customer_id')

        # Retrieve the customer from the database
        customer = Customer.objects.filter(id=user_id).first()
        if not customer:
            abort(404, message='Customer not found')

        data = request.get_json()

        # Update the customer profile
        customer.update(**data)
        customer.save()

        return customer.to_json(), 200

    def delete(self):
        # Get the authenticated user's ID
        user_id = session.get('customer_id')

        # Retrieve the customer from the database
        customer = Customer.objects.filter(id=user_id).first()
        if not customer:
            abort(404, message='Customer not found')

        # Delete all orders associated with the customer
        Order.objects.filter(customer = user_id).delete()
        # Delete all measurements associated with the customer
        Measurement.objects.filter(customer = user_id).delete()
        # Delete all delivery addresses associated with the customer
        DeliveryAddress.objects.filter(customer = user_id).delete()
        # Delete the customer profile
        customer.delete()

        # Return an empty response with status code 204 (successful deletion)
        return '', 204


# Tailor Resource
class TailorResource(Resource):
    def post(self):
        try:
            tailor = request.get_json()
            print(tailor)
            tailor['user'] = session.get('user_id')
            print('\n\n\n\n',tailor)
            tailor = Tailor(**tailor).save()
            session['tailor_id'] = str(tailor.id)  # Convert to string
            print(str(tailor.id))
            return {'id': str(tailor.id)}, 200  # Convert to string
        except:
            return {"message": 'Not completed'}, 500
    def get(self):
        # Get the authenticated user's ID
        user_id =  session.get('tailor_id')
        # Retrieve the tailor from the database
        tailor = Tailor.objects.filter(id=user_id).first()
        if not tailor:
            abort(404, message='Tailor not found')

        return tailor.to_json(), 200


    def put(self):
        # Get the authenticated user's ID
        user_id =  session.get('tailor_id')

        # Retrieve the tailor from the database
        tailor = Tailor.objects.filter(id=user_id).first()
        if not tailor:
            abort(404, message='Tailor not found')

        data = request.get_json()

        # Update the tailor profile
        tailor.update(**data)
        tailor.save()

        return tailor.to_json(), 200

    def delete(self):
        # Get the authenticated user's ID
        user_id =  session.get('tailor_id')

        # Retrieve the tailor from the database
        tailor = Tailor.objects.filter(id=user_id).first()
        if not tailor:
            abort(404, message='Tailor not found')

        # Delete all orders associated with the tailor
        Order.objects.filter(tailor=tailor).delete()
        # Delete the tailor profile
        tailor.delete()

        # Return an empty response with status code 204 (successful deletion)
        return '', 204


# Tailor Orders Resource
class TailorOrdersResource(Resource):
    def get(self):
        logged_in_tailor_id = session.get('tailor_id')
        print('\n\n\ntailor_id', logged_in_tailor_id)
        if logged_in_tailor_id:
            # Assuming you have an Order model with a field 'tailor' to store the tailor reference
            orders = Order.objects(tailor=logged_in_tailor_id)

            tailor_data = []
            for order in orders:
                # Fetch customer data for each order
                print(order.category, order.customer.email )
                # Fetch measurement data for the current tailor and customer
                measurement = Measurement.objects.filter(order= order).first()
                if measurement:
                    print(measurement.shirt_length)
                    tailor_data.append({
                        'customer_name': order["customer"].first_name + ' ' + order["customer"].last_name,
                        'customer_phone': order["customer"].contact,
                        'customer_email': order["customer"].email,
                        'order_name': order.name,
                        'order_phone': order.phone,
                        'order_category': order.category,
                        'order_fabric_type': order.fabric_type,
                        'order_garment_style': order.garment_style,
                        'order_color_type': order.color_type,
                        'order_kuff_style': order.kuff_style,
                        'measurement_shirt_length': measurement.shirt_length if measurement else '',
                        'measurement_chest': measurement.chest if measurement else '',
                        'measurement_shoulder_width': measurement.shoulder_width if measurement else '',
                        'measurement_arm_length': measurement.arm_length if measurement else '',
                        'measurement_wrist': measurement.wrist if measurement else '',
                        'measurement_waist': measurement.waist if measurement else '',
                        'measurement_hip': measurement.hip if measurement else '',
                        'measurement_seat': measurement.seat if measurement else '',
                        'measurement_pants_length': measurement.pants_length if measurement else '',
                    })

            return {'tailor_data': tailor_data}, 200
        else:
            return {'message': 'Tailor not logged in'}, 401


# Customer Orders Resource
class CustomerOrdersResource(Resource):
    def get(self):
        # Get the authenticated user's ID
        customer_id =  session.get('customer_id')
        # Retrieve all orders associated with the customer
        orders = Order.objects.filter(customer=customer_id)
        customer_order = []
        for order in orders:
            customer_order.append({
            'name': order.name,
            'phone': order.phone,
            'category': order.category,
            'fabric_type': order.fabric_type,
            'garment_style': order.garment_style,
            'color_type': order.color_type,
            'kuff_style': order.kuff_style,
            'tailor_name': order['tailor'].first_name + ' ' + order['tailor'].last_name,
            })
        return {'customer_order': customer_order}, 200
        
    def post(self):
        # Get the authenticated user's ID
        customer_id =  session.get('customer_id')
        data = request.get_json()
        print(data, customer_id)
        if not customer_id:
            return 'Error'
        
        data['customer'] = customer_id

        
        order = Order(**data).save()
        session['order_id'] = str(order.id)
        return {"order_id": str(order.id)}, 201


# Measurement Resource
class MeasurementResource(Resource):
    def get(self):
        customer_id =  session.get('customer_id')
        # Retrieve all orders associated with the customer
        measurements = Measurement.objects.filter(customer=customer_id)
        return Response(measurements.to_json(), mimetype="application/json", status=200)
    def post(self):
        # Get the authenticated user's ID
        user_id = session.get("customer_id")
        order_id = session.get('order_id')
        data = request.get_json()
        print(str(order_id))
        if not user_id:
            return {'error': 'User ID is required.'}, 400

        # Retrieve the customer from the database
        customer = Customer.objects.filter(id=user_id).first()
        if not customer:
            abort(404, message='Customer not found')
        data['customer'] = customer
        measurement = Measurement(**data)
        measurement.save()
        return measurement.to_json(), 201

    def put(self, measurement_id):
        # Get the authenticated user's ID
        customer = session.get('customer_id')

        # Find the measurement based on the unique identifier and user
        measurement = Measurement.objects.filter(id=measurement_id, customer = customer).first()
        if not measurement:
            abort(404, message='Measurement not found')

        data = request.get_json()

        # Update the measurement
        measurement.update(**data)
        measurement.save()
        return measurement.to_json(), 200
    
    
    def delete(self, measurement_id):
        # Get the authenticated user's ID
        user_id = session.get("customer_id")
        # Find the measurement based on the unique identifier and user
        measurement = Measurement.objects.filter(id=measurement_id, customer=user_id).first()
        if not measurement:
            abort(404, message='Measurement not found')

        # Delete the measurement
        measurement.delete()
        return '', 204


# DeliveryAddress Resource
class DeliveryAddressResource(Resource):
    def post(self):
        # Get the authenticated user's ID
        user_id = session.get("customer_id")

        data = request.get_json()

        if not user_id:
            return {'error': 'User ID is required.'}, 400

        # Retrieve the customer from the database
        customer = Customer.objects.filter(id=user_id).first()
        if not customer:
            abort(404, message='Customer not found')

        data['customer'] = customer
        delivery_address = DeliveryAddress(**data)
        delivery_address.save()

        return delivery_address.to_json(), 201

    def put(self, delivery_address_id):
        # Get the authenticated user's ID
        user_id = session.get('customer_id')

        # Find the delivery address based on the unique identifier and user
        delivery_address = DeliveryAddress.objects.filter(id=delivery_address_id, customer=user_id).first()
        if not delivery_address:
            abort(404, message='Delivery Address not found')

        data = request.get_json()

        # Update the delivery address
        delivery_address.update(**data)
        delivery_address.save()

        return delivery_address.to_json(), 200

    def delete(self, delivery_address_id):
        # Get the authenticated user's ID
        user_id = session.get('customer_id')

        # Find the delivery address based on the unique identifier and user
        delivery_address = DeliveryAddress.objects.filter(id=delivery_address_id, customer=user_id).first()
        if not delivery_address:
            abort(404, message='Delivery Address not found')

        # Delete the delivery address
        delivery_address.delete()
        return '', 204

