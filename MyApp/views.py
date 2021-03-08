from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
from .models import National_ID


# Create your views here.
@app_view(["POST"])
def get_info(request):

    """Get info method is an endpoint for validating and extracting information
    from the egyptian national id. It expects data to be {"id_number": "<your_id_number"}
    Returns:
        HTTPResponse: - 200 OK, json_info: national id is validated and info extraction ok
                      - 400 Bad Request: Wrong national id number
    """
    request_body = request.body.read()

    try:
        request_data = json.loads(request_body)
        national_id_number = request_data["id_number"]
    except (JSONDecodeError, KeyError) as e:
        json_error_msg = f"Error parsing input data:\n{str(e)}"
        return HTTPResponse({"error": json_error_msg}, status=400, headers={"Content-Type": "application/json"},)

    national_id_object = NationalID(national_id_number)

    is_valid_id, national_id_information = national_id_object.get_info()

    if is_valid_id:
        return HTTPResponse(
            {"nationl_id_data": national_id_information}, status=200, headers={"Content-Type": "application/json"},
        )
    else:
        return HTTPResponse(national_id_information, status=400, headers={"Content-Type": "application/json"},)