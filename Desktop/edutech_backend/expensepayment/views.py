import requests
import logging
from django.conf import settings
from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ExpensePaymentSerializer

logger = logging.getLogger(__name__)


class ExpensePaymentAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Post method to handle expense payment.
        """
        serializer = ExpensePaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_destination = serializer.validated_data['payment_destination']
            if payment_destination == 'Bank':
                return self.handle_bank_payment(serializer.validated_data)
            elif payment_destination == 'M-Pesa':
                return self.handle_mpesa_payment(serializer.validated_data)
            else:
                logger.warning(f"Invalid payment destination: {payment_destination}")
                return Response({"detail": "Invalid payment destination"}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_bank_payment(self, payment_info):
        try:
            url = settings.JENGA_PAYMENT_URL
            payload = {
                "amount": payment_info["amount"],
                "currency": payment_info["currency"],
                "source_account": payment_info["source_account"],
                "destination_account": payment_info["destination_account"]
            }
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                return Response({"detail": "Bank-to-bank payment initiated successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Failed bank payment: {response.text}")
                return Response({"detail": "Failed to initiate bank-to-bank payment"},
                                status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            logger.error(f"Bank payment request exception: {e}")
            return Response({"detail": "Service unavailable. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Unhandled exception during bank payment: {e}")
            return Response({"detail": "An error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_mpesa_payment(self, payment_info):
        try:
            url = settings.JENGA_PAYMENT_URL
            payload = {
                "amount": payment_info["amount"],
                "currency": payment_info["currency"],
                "phone_number": payment_info["phone_number"],
                "account_number": payment_info["account_number"]
            }
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                return Response({"detail": "Bank-to-M-Pesa payment initiated successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Failed M-Pesa payment: {response.text}")
                return Response({"detail": "Failed to initiate bank-to-M-Pesa payment"},
                                status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            logger.error(f"M-Pesa payment request exception: {e}")
            return Response({"detail": "Service unavailable. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Unhandled exception during M-Pesa payment: {e}")
            return Response({"detail": "An error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
