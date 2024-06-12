import os
import time
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny

from edutech_payment_engine import settings
from parents.models import Parents
from schools.models import Schools
from students.models import Students, StudentAccount
from students.serializers import StudentsSerializers
from studentsparents.models import StudentsParents
from studentsschools.models import StudentsSchools
from utils.ApiResponse import ApiResponse
from django.db.models import Q
from utils.Helpers import Helpers
from django.core.files.storage import FileSystemStorage
from edutech_payment_engine.settings import MEDIA_URL
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class StudentsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StudentsView(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializers
    pagination_class = StudentsPagination

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('school_code', openapi.IN_QUERY, description="School code for filtering students",
                          type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        school_code = request.query_params.get('school_code', None)

        if school_code:
            students = self.queryset.filter(schoolCode=school_code)
        else:
            students = self.queryset

        page = paginator.paginate_queryset(students, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = ApiResponse()
        helper = Helpers()
        StudentsData = StudentsSerializers(data=request.data)
        uniqueid = helper.generateUniqueId('KSH099', '96758')
        print(uniqueid)
        if not StudentsData.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill in the details correctly.", "status": status_code}, status_code)

        uniqueid = helper.generateUniqueId('KSH099', '96758')
        print(uniqueid)
        # StudentsData.save()
        response.setStatusCode(status.HTTP_201_CREATED)
        response.setMessage("Student created")
        response.setEntity(request.data)
        return Response(response.toDict(), status=response.status)

    def destroy(self, request, *args, **kwargs):
        regionData = Students.objects.filter(id=kwargs['pk'])
        if regionData:
            regionData.delete()
            status_code = status.HTTP_200_OK
            return Response({"message": "Users deleted Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Users data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        users_details = Students.objects.get(id=kwargs['pk'])
        users_serializer_data = StudentsSerializers(
            users_details, data=request.data, partial=True)
        if users_serializer_data.is_valid():
            users_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Users Update Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Users data Not found", "status": status_code})

    class FeeTransaction:
        pass

    def generate_report(self, request):
        try:
            students = Students.objects.all()
            fee_balance_report = []
            fee_payment_report = []

            for student in students:
                # Calculate fee balance for each student
                fee_transactions = FeeTransaction.objects.filter(student=student)
                total_fee_paid = sum(transaction.amount_paid for transaction in fee_transactions)
                fee_balance = student.total_fee - total_fee_paid

                # Generate fee balance report
                fee_balance_report.append({
                    'student_id': student.id,
                    'student_name': student.name,
                    'fee_balance': fee_balance,
                    # Add more fields as needed
                })

                # Generate fee payment report
                fee_payment_report.append({
                    'student_id': student.id,
                    'student_name': student.name,
                    'total_fee_paid': total_fee_paid,
                    # Add more fields as needed
                })

            report_data = {
                'fee_balance_report': fee_balance_report,
                'fee_payment_report': fee_payment_report
            }

            return Response(report_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    class Parent:
        pass

    def filter_students(self, request, *args, **kwargs):
        columns = ['admNumber', 'id']
        search_param = kwargs.get('str', '')

        filters = Q()
        for column in columns:
            filters |= Q(**{f"{column}__icontains": search_param})

        # Applying filters to the queryset
        students_data = Students.objects.filter(filters)

        if students_data.exists():
            response = {
                "message": "Records retrieved",
                "status_code": 200,
                "data": list(students_data.values())
            }
        else:
            response = {
                "message": "No records found for the provided search criteria",
                "status_code": 404,
                "data": []
            }

        return Response(response, status=status.HTTP_200_OK if students_data.exists() else status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def createStudent(self, request):
        response = ApiResponse()  # Initialize your custom API response
        helper = Helpers()  # Initialize a helper object, presumably containing utility methods
        print(request.data)  # Print the incoming request data to the console for debugging
        schoolCode = request.data.get('schoolCode')
        admNo = request.data.get('admNumber')

        # Unique Id
        urls = []
        uniqueid = helper.generateUniqueId(schoolCode, admNo)
        if request.FILES:
            print("File found..................")
            uploaded_files = request.FILES

            upload_dir = os.path.join(MEDIA_URL, "students")

            # Create upload directory if it doesn't exist
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for uploaded_file_name, uploaded_file in uploaded_files.items():
                print(uploaded_file_name)
                fs = FileSystemStorage(location=upload_dir)
                filename = fs.save(uploaded_file_name, uploaded_file)

                # Generate URL for the uploaded file
                uploaded_file_path = os.path.join(upload_dir, filename)

                # Rename the file with current milliseconds timestamp
                # Retain the original file extension
                timestamp = str(int(time.time() * 1000))
                file_name, file_extension = os.path.splitext(uploaded_file_name)
                new_filename = f"{uniqueid}_{timestamp}{file_extension}"
                new_file_path = os.path.join(upload_dir, new_filename)
                os.rename(uploaded_file_path, new_file_path)

                domain = request.get_host()
                protocol = 'https://' if request.is_secure() else 'http://'
                media_url = f"{protocol}{domain}/{MEDIA_URL}"
                file_url = media_url + 'students/' + new_filename
                urls.append(file_url)

        print(urls)

        # Actual student saving
        Students.objects.create(
            uniqueId=uniqueid,
            admNumber=request.data.get('admNumber'),
            schoolCode=request.data.get('schoolCode'),
            firstName=request.data.get('firstName'),
            middleName=request.data.get('middleName'),
            lastName=request.data.get('lastName'),
            studentGender=request.data.get('studentGender'),
            dob=request.data.get('dob'),
            dateOfAdmission=request.data.get('dateOfAdmission'),
            healthStatus=request.data.get('healthStatus'),
            grade=request.data.get('grade'),
            stream=request.data.get('stream'),
            schoolStatus=request.data.get('schoolStatus'),
            dormitory=request.data.get('dormitory'),
            parentID=request.data.get('parentID'),
            schoolID=request.data.get('schoolID'),
            urls=urls
        )

        parent = Parents.objects.get(id=request.data.get('parentID'))
        student = Students.objects.last()

        StudentsParents.objects.create(
            parentID=parent,
            studentID=student
        )

        school = Schools.objects.get(id=request.data.get('schoolID'))
        student = Students.objects.last()

        StudentsSchools.objects.create(
            schoolID=school,
            studentID=student
        )

        response.setMessage("Student created")
        response.setStatusCode(200)  # Set the status code of the API response

        return Response(response.toDict(),
                        200)  # Return the API response as a Django Response object with a 200 status
