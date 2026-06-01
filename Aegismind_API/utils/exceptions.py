from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import psycopg2

def custom_exception_handler(exc, context):
    '''Custom exception handler that checks for database connection errors'''

    response = exception_handler(exc, context)

    if isinstance(exc, (psycopg2.OperationalError, ConnectionRefusedError)):
        return Response(
            {"detail": "Database service is currently unavailable. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    return response