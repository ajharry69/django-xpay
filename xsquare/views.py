from rest_framework import status
from rest_framework.response import Response
from xauth.views import CreateAPIView

from . import serializers


class PaymentView(CreateAPIView):
    serializer_class = serializers.PaymentSerializer

    def post(self, request, format=None):
        response = super().post(request, format)
        data = response.data
        if 'errors' in data:
            errors = data.get('errors', [{'detail': 'Error occurred'}])
            response = Response(
                data={
                    'error': errors[0].get('detail', ),
                    'metadata': errors,
                },
                status=status.HTTP_412_PRECONDITION_FAILED,
            )
        elif 'payment' in data:
            response = Response(
                data=data.get('payment', ),
                status=status.HTTP_200_OK,
            )
        return response
