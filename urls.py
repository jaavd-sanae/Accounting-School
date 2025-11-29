from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classes.views import ClassroomViewSet, get_grade_choices, get_gifted_grades
from students.views import StudentViewSet
from finance.views import (TransactionViewSet, get_transaction_categories, get_exam_types, get_withdraw_categories,
                            get_utility_types, get_all_categories, get_filtered_transactions,get_financial_summary,
                            get_operation_types)
from employees.views import (EmployeeViewSet , get_category_choices ,get_position_choices, 
                             get_positions_by_category,get_employees_by_position)


router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/grade-choices/', get_grade_choices, name='grade-choices'),
    path('api/transaction-categories/', get_transaction_categories, name='transaction-categories'),
    path('api/gifted-grades/', get_gifted_grades),
    path('api/exam-types/', get_exam_types),
    path('api/category-choices/', get_category_choices),
    path('api/position-choices/', get_position_choices),
    path('api/positions-by-category/', get_positions_by_category, name='positions-by-category'),
    path('api/employees-by-position/', get_employees_by_position, name='employees-by-position'),
    path('api/withdraw-categories/', get_withdraw_categories, name='withdraw-categories'),
    path('api/utility-types/', get_utility_types, name='utility-types'),
    path('api/all-categories/', get_all_categories, name='all-categories'),
    path('api/filtered-transactions/', get_filtered_transactions, name='filtered-transactions'),
    path('api/financial-summary/', get_financial_summary, name='financial-summary'),
    path('api/operation-types/', get_operation_types, name='operation-types'),
]