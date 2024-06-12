from django.db import models

from feecategories.models import FeeCategories, VirtualAccount
from students.models import Students



class StudentFeeCategories(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.student} "

    class Meta:
        db_table = 'StudentFeeCategories'  # Optional: specify the database table name
