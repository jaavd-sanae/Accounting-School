from rest_framework import viewsets
from .models import Student
from school_accounting.serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.filter(is_active=True)
    
    def get_queryset(self):
        queryset = Student.objects.filter(is_active=True)
        classroom_id = self.request.query_params.get('classroom_id')
        grade = self.request.query_params.get('grade')
        
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        elif grade:
            queryset = queryset.filter(classroom__grade=grade)
            
        return queryset