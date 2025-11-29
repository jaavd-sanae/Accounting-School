from rest_framework import serializers
from students.models import Student
from classes.models import Classroom
from finance.models import Transaction 
from employees.models import Employee

class ClassroomSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Classroom
        fields = ['id', 'class_number', 'grade', 'teacher_name', 'capacity', 'student_count'] 
    
    def get_student_count(self, obj):
        return obj.student_set.count()

class StudentSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.class_number', read_only=True)
    grade = serializers.CharField(source='classroom.grade', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'national_code', 
            'classroom', 'classroom_name', 'grade',
            'father_phone', 'mother_phone', 'home_phone' 
        ]


class TransactionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    employee_name = serializers.SerializerMethodField(read_only=True)
    classroom_name = serializers.CharField(source='student.classroom.class_number', read_only=True)
    grade = serializers.CharField(source='student.classroom.grade', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    utility_type_display = serializers.CharField(source='get_utility_type_display', read_only=True)  # ✅ جدید
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)  # ✅ جدید

    def get_student_name(self, obj):
        return str(obj.student) if obj.student else "-"

    def get_employee_name(self, obj):
        return str(obj.employee) if obj.employee else "-"
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'transaction_type_display', 'category', 'category_display',
            'amount', 'date', 'payment_method', 'payment_method_display', 'description',
            'student', 'student_name', 'classroom_name', 'grade',
            'employee', 'employee_name', 'receipt_number', 'created_at',
            'subject', 'insurance_type', 'exam_type', 'exam_type_display',  # ✅ exam_type اضافه شد
            'utility_type', 'utility_type_display'  # ✅ این دو خط رو اضافه کن
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    
    class Meta:
        model = Employee
        fields = "__all__"