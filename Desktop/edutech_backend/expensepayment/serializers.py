from rest_framework import serializers
from .models import ExpensePayment


class ExpensePaymentSerializer(serializers.ModelSerializer):
    PAYMENT_DESTINATION_CHOICES = (
        ('Bank', 'Bank'),
        ('M-Pesa', 'M-Pesa'),
    )

    payment_destination = serializers.ChoiceField(choices=PAYMENT_DESTINATION_CHOICES)

    class Meta:
        model = ExpensePayment
        fields = '__all__'
