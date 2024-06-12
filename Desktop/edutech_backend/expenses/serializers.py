from rest_framework import serializers
from .models import Expenses
from expensetypes.models import ExpenseTypes
from expensetypes.serializers import ExpenseTypesSerializer


class ExpensesSerializer(serializers.ModelSerializer):
    expensetypes = ExpenseTypesSerializer()

    class Meta:
        model = Expenses
        fields = ['amount', 'expensetypes', 'receipt']

    def create(self, validated_data):
        expensetypes_data = validated_data.pop('expensetypes')
        expensetype = ExpenseTypes.objects.create(**expensetypes_data)
        expense = Expenses.objects.create(expensetypes=expensetype, **validated_data)
        return expense

    def update(self, instance, validated_data):
        expensetypes_data = validated_data.pop('expensetypes', None)

        # Update expensetype if provided
        if expensetypes_data:
            expensetype = instance.expensetypes
            for attr, value in expensetypes_data.items():
                setattr(expensetype, attr, value)
            expensetype.save()

        # Update the instance with the rest of the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


