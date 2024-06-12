from rest_framework import serializers

from fee.models import StudentFeeCategories


class StudentFeeCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeCategories
        fields = "__all__"
