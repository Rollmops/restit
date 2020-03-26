RESOURCE_TEMPLATE = """{imports}


@path("{path}")
class {resource_class_name}(Resource):
    def __init__():
        # you can remove the constructor if you do not pass any object in here
        super().__init__()
        
{request_methods}
"""
