import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ExpensePaymentSerializer


class ExpensePaymentAPIView(APIView):
    def post(self, request):
        """
        Post method to handle expense payment.
        """
        serializer = ExpensePaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_destination = serializer.validated_data.get('payment_destination')
            if payment_destination == 'Bank':
                return self.handle_bank_payment(serializer)
            elif payment_destination == 'M-Pesa':
                return self.handle_mpesa_payment(serializer)
            else:
                return Response({"detail": "Invalid payment destination"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_bank_payment(self, serializer):
        try:
            # Extract payment information from serializer
            payment_info = serializer.validated_data

            # Construct the URL for the Jenga API endpoint
            url = settings.JENGA_PAYMENT_URL

            # Prepare the payload
            payload = {
                "amount": payment_info["amount"],
                "currency": payment_info["currency"],
                "source_account": payment_info["source_account"],
                "destination_account": payment_info["destination_account"]
            }

            # Make the POST request to the Jenga API
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                return Response({"detail": "Bank-to-bank payment initiated successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Failed to initiate bank-to-bank payment"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle exceptions
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def handle_mpesa_payment(self, serializer):
        try:
            # Extract payment information from serializer
            payment_info = serializer.validated_data

            # Construct the URL for the Jenga API endpoint
            url = settings.JENGA_PAYMENT_URL

            # Prepare the payload
            payload = {
                "amount": payment_info["amount"],
                "currency": payment_info["currency"],
                "phone_number": payment_info["phone_number"],
                "account_number": payment_info["account_number"]
            }

            # Make the POST request to the Jenga API
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                return Response({"detail": "Bank-to-M-Pesa payment initiated successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Failed to initiate bank-to-M-Pesa payment"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle exceptions
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
