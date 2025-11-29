from django.db import models
from classes.models import Classroom

class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_code = models.CharField(max_length=10, unique=True, verbose_name="کد ملی") 
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name="کلاس")
    
    father_phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن پدر")
    mother_phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن مادر") 
    home_phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن ثابت")
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "دانش‌آموز"
        verbose_name_plural = "دانش‌آموزان"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.classroom.class_number}"