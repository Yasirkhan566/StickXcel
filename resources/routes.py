from .resources import (
    UserRegisterResource,
    UserLoginResource,
    AllTailors,
    TailorResource,
    MeasurementResource,
    DeliveryAddressResource,
    CustomerResource,
    TailorResource,
    TailorOrdersResource,
    CustomerOrdersResource,

)

def initialize_routes(api):
    # Add resources to the API
    api.add_resource(UserRegisterResource, '/api/register')
    api.add_resource(UserLoginResource, '/api/login')
    api.add_resource(AllTailors, '/api/tailors')
    api.add_resource(CustomerResource, '/api/customer')
    api.add_resource(TailorResource, '/api/tailor')
    api.add_resource(TailorOrdersResource, '/api/tailor_order')
    api.add_resource(CustomerOrdersResource, '/api/order')
    api.add_resource(MeasurementResource, '/api/measurement')
    api.add_resource(DeliveryAddressResource, '/api/delivery_address')
