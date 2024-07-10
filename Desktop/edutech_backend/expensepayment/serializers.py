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

    def validate(self, data):
        payment_destination = data.get('payment_destination')
        if payment_destination == 'Bank':
            if not data.get('source_account') or not data.get('destination_account'):
                raise serializers.ValidationError("Bank payments require source_account and destination_account.")
        elif payment_destination == 'M-Pesa':
            if not data.get('phone_number') or not data.get('account_number'):
                raise serializers.ValidationError("M-Pesa payments require phone_number and account_number.")
        return data
