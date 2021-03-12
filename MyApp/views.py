
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from .helpers import validate

# Create your views here.



@api_view(['POST'])
def testAPI(request):

    """Get info method is an endpoint for validating and extracting information
    from the egyptian national id. It expects data to be {"id_number": "your_id_number"}
    Returns:
        JsonResponse: - True OK, json_info: national id is validated and info extraction ok
                      - False Bad Request: Wrong national id number
    """
    

    data = {}   #declar empty dictionairy for data
    if not 'id' in request.data:
        return JsonResponse({
            'status' : False ,
            'message' : 'missing data'

        })
    id = request.data[ 'id' ]
    validate_data = validate(id)
    if not validate_data: 
        status = False
        message = 'invalid id number'  
       
    else: 
        status = True
        message = 'success'
        data  = validate_data

    return JsonResponse({
            'status':status,
            'message':message,
            'data':data    
        })
