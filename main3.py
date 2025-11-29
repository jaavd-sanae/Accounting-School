import flet as ft

import requests

from datetime import datetime
import jdatetime

import webbrowser
import tempfile
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import mm


def map_utility_type(persian_type):
    """تبدیل نوع قبض از فارسی به انگلیسی"""
    utility_mapping = {
        "آب": "water",
        "برق": "electricity", 
        "گاز": "gas",
        "تلفن همراه": "mobile",
        "تلفن ثابت": "landline",
        "اینترنت": "internet"
    }
    return utility_mapping.get(persian_type, persian_type)


COLORS = {
        "gradient_start": "#667eea",
        "gradient_end": "#764ba2", 
        "white": "#ffffff",
        "gray_900": "#1a202c",
        "gray_100": "#edf2f7",
        "gray_200": "#e2e8f0",
        "gray_600": "#718096",
        "gray_300": "#e2e8f0",
        "gray_400": "#cbd5e0",
        "gray_500": "#a0aec0", 
        "gray_700": "#4a5568",
        "blue_600": "#3182ce",
        "blue_100": "#bee3f8",
        "blue_50": "#ebf8ff", 
        "red_600": "#e53e3e",
        "red_100": "#fed7d7", 
        "red_50": "#fff5f5",
        "green_600": "#38a169",
        "green_100": "#c6f6d5",
        "green_50": "#f0fff4",
        "orange_600": "#dd6b20",
        "orange_100": "#feebc8",
        "orange_50": "#fffaeb",  
        "orange_400": "#f6ad55", 
        "orange_600": "#dd6b20",
        "yellow_100": "#fefcbf", 
        "yellow_50": "#fefce8",  
        "yellow_500": "#ecc94b", 
        "purple_600": "#805ad5",
        "purple_400": "#9f7aea",
        "purple_500": "#805ad5", 
        "purple_600": "#6b46c1",
        "purple_100": "#e9d8fd",
        "purple_50": "#faf5ff",
        "indigo_600": "#5a67d8",
        "indigo_100": "#c3dafe",
        "indigo_50": "#e0e7ff",  
        "teal_600": "#319795",
        "teal_100": "#b2f5ea",
        "teal_50": "#e6fffa",    
        "cyan_600": "#00a3c4", 
        "cyan_100": "#a0f0ed",
        "cyan_50": "#e0fcff",  
        "pink_600": "#d53f8c",
        "pink_100": "#fed7e2",
        "pink_50": "#fff5f7",   
        "emerald_600": "#059669",
        "emerald_100": "#a7f3d0",
        "emerald_50": "#ecfdf5",
        "violet_50": "#f5f3ff", 
        "violet_400": "#9f7aea",
        "violet_500": "#805ad5",
        "violet_600": "#6b46c1", 
        "violet_100": "#e9d8fd",
        "rose_600": "#e11d48",
        "rose_100": "#ffe4e6",
        "rose_50": "#fff1f2",  
        "cyan_100": "#c4f1f9",
        "cyan_600": "#0891b2",
        "blue_400": "#4299e1", 
        "orange_400": "#ed8936",
        "green_400": "#48bb78",
        "blue_400": "#4299e1", 
        "purple_400": "#9f7aea",
        "orange_400": "#ed8936",
        "teal_400": "#38b2ac",
        "indigo_400": "#667eea",
        "red_400": "#f56565",
        "red_600": "#e53e3e",
        "blue_400": "#4299e1", 
        "blue_600": "#3182ce",
        "purple_400": "#9f7aea",
        "purple_600": "#805ad5",
        "purple_700": "#6b21a8",
        "teal_400": "#38b2ac",
        "teal_600": "#319795",
        "yellow_400": "#ecc94b",
        "yellow_600": "#d69e2e",
        "light_blue_50": "#f0f9ff",
        "light_blue_100": "#e0f2fe", 
        "light_blue_200": "#bae6fd",
        "light_blue_300": "#7dd3fc",
        "light_blue_400": "#38bdf8",
        "light_blue_500": "#0ea5e9",
        "light_blue_600": "#0284c7",
        "light_blue_700": "#0369a1",
        "light_blue_800": "#075985",
        "light_blue_900": "#0c4a6e",
        "cyan_50": "#ecfeff",
        "cyan_100": "#cffafe",
        "cyan_200": "#a5f3fc", 
        "cyan_300": "#67e8f9",
        "cyan_400": "#22d3ee",
        "cyan_500": "#06b6d4",
        "cyan_600": "#0891b2",
        "cyan_700": "#0e7490",
        "cyan_800": "#155e75",
        "cyan_900": "#164e63",

        "teal_50": "#f0fdfa",
        "teal_100": "#ccfbf1",
        "teal_200": "#99f6e4",
        "teal_300": "#5eead4",
        "teal_400": "#2dd4bf",
        "teal_500": "#14b8a6", 
        "teal_600": "#0d9488",
        "teal_700": "#0f766e",
        "teal_800": "#115e59",
        "teal_900": "#134e4a",
        "blue_700": "#1d4ed8",
        "green_200": "#9ae6b4",
        "green_50": "#f0fff4",
        "red_200": "#feb2b2", 
        "red_50": "#fff5f5",
        "blue_200": "#90cdf4",
        "blue_50": "#ebf8ff",
        "gray_200": "#e2e8f0",
        "gray_50": "#f7fafc",
        "pink_50": "#fdf2f8",
        "pink_100": "#fce7f3", 
        "pink_200": "#fbcfe8",
        "pink_300": "#f9a8d4",
        "pink_400": "#f472b6",
        "pink_500": "#ec4899",
        "pink_600": "#db2777",
        "pink_700": "#be185d",
        "pink_800": "#9d174d",
        "pink_900": "#831843",
}

BASE_URL = "http://127.0.0.1:8000/api"

# این رو در بالای فایل frontend، نزدیک BASE_URL اضافه کن

class DateService:
    """سرویس مدیریت تاریخ - نسخه حرفه‌ای"""
    
    @staticmethod
    def get_current_jalali():
        """دریافت تاریخ امروز شمسی"""
        return jdatetime.datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def to_gregorian_if_needed(jalali_date, force_convert=False):
        """
        تبدیل تاریخ شمسی به میلادی در صورت نیاز
        - force_convert: اگر True باشد همیشه تبدیل کند
        - پیش‌فرض: تاریخ شمسی بازگردانده می‌شود (Backend هوشمند است)
        """
        if not jalali_date:
            return None
            
        if force_convert:
            try:
                year, month, day = map(int, jalali_date.split('-'))
                gregorian_date = jdatetime.date(year, month, day).togregorian()
                return gregorian_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(f"⚠️ خطا در تبدیل تاریخ {jalali_date}: {e}")
                return jalali_date
        else:
            # نسخه حرفه‌ای: تاریخ شمسی بازگردانده می‌شود
            return jalali_date
    
    @staticmethod
    def validate_jalali_date(date_string):
        """اعتبارسنجی تاریخ شمسی"""
        try:
            jdatetime.datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

def get_classrooms(grade=None):
    """گرفتن لیست کلاس‌ها از API - نسخه اصلاح شده"""
    try:
        url = f"{BASE_URL}/classrooms/"
        params = {}
        if grade:
            params['grade'] = grade  # ✅ درست شد
        
        print(f"🔍 درخواست کلاس‌ها با پارامترها: {params}")
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            classrooms = response.json()
            print(f"✅ تعداد کلاس‌های دریافت شده: {len(classrooms)}")
            return classrooms
        else:
            print(f"❌ خطا در دریافت کلاس‌ها: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ خطا در get_classrooms: {e}")
        return []
    
def get_students(classroom_id=None, grade=None):
    """گرفتن لیست دانش‌آموزان از API - نسخه اصلاح شده"""
    try:
        url = f"{BASE_URL}/students/"
        params = {}
        
        if classroom_id:
            params['classroom_id'] = classroom_id
        elif grade:
            params['grade'] = grade
            
        print(f"🔍 درخواست دانش‌آموزان با پارامترها: {params}")
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            students = response.json()
            print(f"✅ تعداد دانش‌آموزان دریافت شده: {len(students)}")
            return students
        else:
            print(f"❌ خطا در دریافت دانش‌آموزان: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ خطا در get_students: {e}")
        return []

def get_student_details(student_id):
    """گرفتن اطلاعات کامل یک دانش‌آموز از API"""
    try:
        response = requests.get(f"{BASE_URL}/students/{student_id}/")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error getting student details: {e}")
        return None

def get_payment_methods():
    """گرفتن انواع روش‌های پرداخت از مدل"""
    return [
        {'value': 'cash', 'label': 'نقدی'},
        {'value': 'card', 'label': 'کارت بانکی'},
        {'value': 'transfer', 'label': 'انتقال بانکی'},
        {'value': 'check', 'label': 'چک'},
        {'value': 'pos', 'label': 'دستگاه پوز'},
    ]

def create_tuition_payment(payment_data):
    try:
        jalali_date = payment_data['payment_date']  # یا sale_date, bill_date بسته به تابع
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'deposit',  # واریز
            'category': 'tuition',  # شهریه
            'amount': payment_data['amount'],
            'date': payment_data['payment_date'],  # تاریخ میلادی
            'payment_method': payment_data['payment_method'],
            'description': payment_data.get('description', '') or payment_data.get('notes', ''),
            'student': payment_data['student'],  # ID دانش‌آموز
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            return True, "پرداخت با موفقیت ثبت شد"
        else:
            print("خطا:", response.status_code, response.text)
            return False, f"خطا در ثبت پرداخت: {response.text}"
            
    except Exception as e:
        print(f"خطا در ارتباط با سرور: {e}")
        return False, f"خطا در برقراری ارتباط با سرور: {e}" 

# بعد از توابع create_breakfast_sale و create_cafeteria_sale این رو اضافه کن:

def create_salary_payment(payment_data):
    """ثبت پرداخت حقوق در API"""
    try:
        jalali_date = payment_data['payment_date']  # یا sale_date, bill_date بسته به تابع
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'withdraw',  # ✅ برداشت
            'category': 'salary',            # ✅ حقوق
            'amount': payment_data['amount'],
            'date': payment_data['payment_date'],
            'payment_method': payment_data.get('payment_method', 'cash'),
            'description': f"پرداخت حقوق - {payment_data.get('description', '')}",
            'employee': payment_data['employee'],  # ID کارمند
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "پرداخت حقوق با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت پرداخت: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"

def create_insurance_payment(payment_data):
    """ثبت پرداخت بیمه در API"""
    try:
        jalali_date = payment_data['payment_date']  # یا sale_date, bill_date بسته به تابع
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'withdraw',
            'category': 'insurance',          
            'amount': payment_data['amount'],
            'date': payment_data['payment_date'],
            'payment_method': payment_data.get('payment_method', 'cash'),
            'description': f"بیمه {payment_data.get('insurance_type', '')} - {payment_data.get('description', '')}",
            'employee': payment_data['employee'],
            'receipt_number': payment_data.get('receipt_number', ''),
            'insurance_type': payment_data['insurance_type']
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "پرداخت بیمه با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت پرداخت: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"
    

def create_extra_class_teacher_payment(payment_data):
    """ثبت هزینه کلاس تقویتی به معلم در API - نسخه اصلاح شده"""
    try:
        # 🔼 نیازی به تبدیل تاریخ نیست - از Backend انتظار تاریخ میلادی داریم
        transaction_data = {
            'transaction_type': 'withdraw',          # برداشت
            'category': 'extra_class_cost',          # هزینه کلاس تقویتی
            'amount': payment_data['amount'],
            'date': payment_data['payment_date'],    # 🔥 همین تاریخ میلادی که فرستادی
            'payment_method': 'cash',
            'description': f"هزینه کلاس تقویتی {payment_data['subject']} - {payment_data.get('description', '')}",
            'employee': payment_data['teacher'],
            'subject': payment_data['subject'],
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های ارسالی به API: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data
        )
        
        print(f"🔍 وضعیت پاسخ API: {response.status_code}")
        
        if response.status_code == 201:
            return True, "هزینه کلاس تقویتی با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا: {response.text}"
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return False, f"خطا: {e}"

# این تابع باید در فایل باشه
def convert_jalali_to_gregorian(jalali_date):
    """تبدیل تاریخ شمسی به میلادی"""
    try:
        year, month, day = map(int, jalali_date.split('-'))
        gregorian_date = jdatetime.date(year, month, day).togregorian()
        return gregorian_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"❌ خطا در تبدیل تاریخ: {e}")
        return None

def get_financial_reports(filters=None):
    """گرفتن گزارش‌های مالی از API"""
    try:
        url = f"{BASE_URL}/payments/financial-report/"
        params = {}
        
        if filters:
            if filters.get('start_date'):
                params['start_date'] = filters['start_date']
            if filters.get('end_date'):
                params['end_date'] = filters['end_date']
            if filters.get('grade'):
                params['grade'] = filters['grade']
            if filters.get('classroom_id'):
                params['classroom_id'] = filters['classroom_id']
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {'transactions': [], 'total_count': 0, 'total_amount': 0}
    except Exception as e:
        print(f"Error getting financial reports: {e}")
        return {'transactions': [], 'total_count': 0, 'total_amount': 0}
    
# در بالای فایل، نزدیک توابع get_classrooms و get_students

def get_operation_types():
    """گرفتن انواع عملیات از API"""
    try:
        response = requests.get(f"{BASE_URL}/operation-types/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting operation types: {e}")
        return []

def get_transaction_types(operation_type):
    if operation_type == 'deposit':
        categories = get_deposit_categories()
        return [
            {'value': '', 'label': 'همه انواع واریز'}
        ] + [
            {'value': cat[0], 'label': cat[1]} 
            for cat in categories
        ]
    elif operation_type == 'withdraw':
        categories = get_withdraw_categories()
        return [
            {'value': '', 'label': 'همه انواع برداشت'}
        ] + [
            {'value': cat[0], 'label': cat[1]} 
            for cat in categories
        ]
    return []

def get_grades():
    return [
        {'value': '', 'label': 'همه پایه‌ها'},
        {'value': '1', 'label': 'پایه اول'},
        {'value': '2', 'label': 'پایه دوم'},
    ]

def get_classrooms_by_grade(grade):
    """گرفتن کلاس‌ها بر اساس پایه از API"""
    return get_classrooms(grade=grade)


def create_cafeteria_sale(sale_data):
    try:
        jalali_date = sale_data['sale_date']
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'deposit',
            'category': 'buffet',  # بوفه
            'amount': sale_data['amount'],
            'date': sale_data['sale_date'],
            'payment_method': 'cash',  # یا از کاربر بگیر
            'description': sale_data.get('description', 'فروش بوفه'),
            'receipt_number': ''  # اگر شماره رسید داری
        }
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            return True, "فروش بوفه با موفقیت ثبت شد"
        else:
            return False, f"خطا در ثبت فروش: {response.text}"
    except Exception as e:
        return False, f"خطا در ارتباط: {e}"
    
def create_breakfast_sale(sale_data):
    try:
        jalali_date = sale_data['sale_date']
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'deposit',      # واریز
            'category': 'breakfast',            # صبحانه
            'amount': sale_data['amount'],
            'date': sale_data['sale_date'],     # تاریخ میلادی
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"فروش صبحانه - {sale_data.get('description', '')}",
            'receipt_number': ''                # اگر شماره رسید داری
        }
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            return True, "فروش صبحانه با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.status_code} - {response.text}")
            return False, f"خطا در ثبت فروش: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"
    
def create_purchase(purchase_data):
    """ثبت خرید در API"""
    try:
        jalali_date = purchase_data['purchase_date']
        gregorian_date = convert_jalali_to_gregorian(jalali_date)
        transaction_data = {
            'transaction_type': 'withdraw',     # ✅ برداشت
            'category': 'purchase',             # ✅ خرید
            'amount': purchase_data['amount'],
            'date': purchase_data['purchase_date'],
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"{purchase_data['item_title']} - {purchase_data.get('description', '')}",
            'receipt_number': purchase_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "خرید با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت خرید: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"
    
def create_rent(rent_data):
    """ثبت کرایه در API"""
    try:
        today_jalali = jdatetime.datetime.now().strftime("%Y-%m-%d")
        gregorian_date = convert_jalali_to_gregorian(today_jalali)
        transaction_data = {
            'transaction_type': 'withdraw',     # برداشت
            'category': 'rent',                 # کرایه
            'amount': rent_data['amount'],
            'date': datetime.now().strftime("%Y-%m-%d"),  # تاریخ امروز
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"کرایه {rent_data['month']} - {rent_data.get('description', '')}",
            'receipt_number': ''
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "کرایه با موفقیت ثبت شد"
        else:
            return False, f"خطا در ثبت کرایه: {response.text}"
    except Exception as e:
        return False, f"خطا در ارتباط: {e}"
    
def create_utility_bill(bill_data):
    """ثبت قبض در API - نسخه اصلاح شده"""
    try:
        # تبدیل نوع قبض از فارسی به انگلیسی
        utility_mapping = {
            "آب": "water",
            "برق": "electricity", 
            "گاز": "gas",
            "تلفن همراه": "mobile",
            "تلفن ثابت": "landline",
            "اینترنت": "internet"
        }
        
        utility_type_english = utility_mapping.get(bill_data['utility_type'], bill_data['utility_type'])
        
        # استفاده مستقیم از تاریخ شمسی
        transaction_data = {
            'transaction_type': 'withdraw',     # برداشت
            'category': 'utilities',            # قبوض
            'amount': bill_data['amount'],
            'date': bill_data['bill_date'],     # تاریخ شمسی خام
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"قبض {bill_data['utility_type']} - {bill_data.get('description', '')}",
            'receipt_number': bill_data.get('bill_number', ''),
            'utility_type': utility_type_english  # ✅ حالا انگلیسی هست
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "قبض با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت قبض: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"
    
def create_extra_class_payment(payment_data):
    """ثبت پرداخت کلاس تقویتی در API - نسخه حرفه‌ای"""
    try:
        # ✅ استفاده از سرویس تاریخ هوشمند
        jalali_date = payment_data['payment_date']
        
        # تشخیص خودکار فرمت تاریخ
        try:
            # اول سعی کن به عنوان تاریخ شمسی parse کن
            gregorian_date = jdatetime.datetime.strptime(jalali_date, '%Y-%m-%d').togregorian()
            print(f"📅 تشخیص تاریخ شمسی: {jalali_date} → {gregorian_date}")
        except ValueError:
            try:
                # اگر شمسی نبود، سعی کن به عنوان میلادی parse کن
                gregorian_date = datetime.strptime(jalali_date, '%Y-%m-%d').date()
                print(f"📅 تشخیص تاریخ میلادی: {jalali_date} → {gregorian_date}")
            except ValueError:
                print(f"❌ فرمت تاریخ نامعتبر: {jalali_date}")
                return False, "فرمت تاریخ نامعتبر است"
        
        transaction_data = {
            'transaction_type': 'deposit',           # واریز
            'category': 'extra_class_income',        # درآمد از کلاس تقویتی
            'amount': payment_data['amount'],
            'date': gregorian_date.strftime("%Y-%m-%d"),  # تاریخ میلادی
            'payment_method': 'cash',
            'description': f"کلاس تقویتی - {payment_data.get('description', '')}",
            'student': payment_data['student'],
            'subject': payment_data['subject'],
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های تراکنش: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "پرداخت کلاس تقویتی با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت پرداخت: {response.text}"
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return False, f"خطا: {e}"
    
def create_gifted_class_payment(payment_data):
    """ثبت پرداخت کلاس تیزهوشان در API - نسخه اصلاح شده"""
    try:
        jalali_date = payment_data['payment_date']
        
        # استفاده از سرویس تاریخ هوشمند
        try:
            # اول سعی کن به عنوان تاریخ شمسی parse کن
            gregorian_date = jdatetime.datetime.strptime(jalali_date, '%Y-%m-%d').togregorian()
            print(f"📅 تشخیص تاریخ شمسی: {jalali_date} → {gregorian_date}")
        except ValueError:
            try:
                # اگر شمسی نبود، سعی کن به عنوان میلادی parse کن
                gregorian_date = datetime.strptime(jalali_date, '%Y-%m-%d').date()
                print(f"📅 تشخیص تاریخ میلادی: {jalali_date} → {gregorian_date}")
            except ValueError:
                print(f"❌ فرمت تاریخ نامعتبر: {jalali_date}")
                return False, "فرمت تاریخ نامعتبر است"
        
        
        transaction_data = {
            'transaction_type': 'deposit',
            'category': 'gifted_class',
            'amount': payment_data['amount'],
            'date': gregorian_date.strftime("%Y-%m-%d"),
            'payment_method': 'cash',
            'description': f"کلاس تیزهوشان - {payment_data.get('description', '')}",
            'student': payment_data['student'],
            'subject': payment_data['subject'],
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های ارسالی به API: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ API: {response.status_code}")
        print(f"🔍 متن پاسخ API: {response.text}")
        
        if response.status_code == 201:
            return True, "پرداخت کلاس تیزهوشان با موفقیت ثبت شد"
        else:
            return False, f"خطا در ثبت پرداخت: {response.text}"
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return False, f"خطا: {e}"
    
def create_exam_payment(payment_data):
    """ثبت پرداخت آزمون در API - نسخه کاملاً اصلاح شده"""
    try:
        print("🎯 شروع ثبت پرداخت آزمون در backend...")
        print(f"🔍 داده‌های دریافتی: {payment_data}")
        
        jalali_date = payment_data['payment_date']
        
        # استفاده از سرویس تاریخ هوشمند
        try:
            gregorian_date = jdatetime.datetime.strptime(jalali_date, '%Y-%m-%d').togregorian()
            print(f"📅 تشخیص تاریخ شمسی: {jalali_date} → {gregorian_date}")
        except ValueError:
            try:
                gregorian_date = datetime.strptime(jalali_date, '%Y-%m-%d').date()
                print(f"📅 تشخیص تاریخ میلادی: {jalali_date} → {gregorian_date}")
            except ValueError:
                print(f"❌ فرمت تاریخ نامعتبر: {jalali_date}")
                return False, "فرمت تاریخ نامعتبر است"
        
        # 🔼 ساختار کامل transaction_data
        transaction_data = {
            'transaction_type': 'deposit',
            'category': 'exam',  # دسته‌بندی آزمون
            'amount': payment_data['amount'],
            'date': gregorian_date.strftime("%Y-%m-%d"),
            'payment_method': payment_data.get('payment_method', 'cash'),
            'description': f"آزمون {payment_data.get('exam_type', '')} - {payment_data.get('description', '')}",
            'student': payment_data['student'],
            'exam_type': payment_data.get('exam_type'),  # نوع آزمون
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های ارسالی به API: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ API: {response.status_code}")
        print(f"🔍 متن پاسخ API: {response.text}")
        
        if response.status_code == 201:
            print("✅ آزمون با موفقیت ثبت شد")
            return True, "پرداخت آزمون با موفقیت ثبت شد"
        else:
            print(f"❌ خطا در ثبت آزمون: {response.text}")
            return False, f"خطا در ثبت پرداخت: {response.text}"
            
    except Exception as e:
        print(f"❌ خطای کلی در ثبت آزمون: {e}")
        return False, f"خطا: {e}"
    
def create_gifted_class_teacher_payment(payment_data):
    """ثبت هزینه کلاس تیزهوشان به معلم در API"""
    try:
        transaction_data = {
            'transaction_type': 'withdraw',
            'category': 'gifted_class_cost',  # باید به مدل‌ها اضافه بشه
            'amount': payment_data['amount'],
            'date': payment_data['payment_date'],
            'payment_method': 'cash',
            'description': f"هزینه کلاس تیزهوشان {payment_data['subject']} - {payment_data.get('description', '')}",
            'employee': payment_data['teacher'],
            'subject': payment_data['subject'],
            'receipt_number': payment_data.get('receipt_number', '')
        }
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data
        )
        
        if response.status_code == 201:
            return True, "هزینه کلاس تیزهوشان با موفقیت ثبت شد"
        else:
            return False, f"خطا: {response.text}"
            
    except Exception as e:
        return False, f"خطا: {e}"
    
def get_employees(position=None):
    """گرفتن لیست کارکنان از API"""
    try:
        url = f"{BASE_URL}/employees/"
        if position:
            url += f"?position={position}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting employees: {e}")
        return []
    
def get_employees_by_category(category):
    """گرفتن کارکنان بر اساس دسته سمت - فیلتر در سمت کلاینت"""
    # همه کارکنان رو بگیر
    all_employees = get_employees()
    
    if not all_employees:
        return []
    
    # مپ کردن دسته به positionهای مربوطه
    category_map = {
        'managers': ['manager_first_period', 'manager_second_period'],
        'assistants': ['assistant_educational', 'assistant_cultural', 'assistant_executive'],
        'teachers': ['teacher_grade1', 'teacher_grade2', 'teacher_grade3', 'teacher_grade4', 'teacher_grade5', 'teacher_grade6'],
        'coaches': ['sport_teacher', 'art_teacher'],
        'counselors': ['counselor'],
        'services': ['service'],
    }
    
    positions = category_map.get(category, [])
    
    # فیلتر کردن در سمت کلاینت
    filtered_employees = [
        emp for emp in all_employees 
        if emp.get('position') in positions
    ]
    
    # برای دیباگ - نمایش کارکنان فیلتر شده
    for emp in filtered_employees:
        print(f"   - {emp['first_name']} {emp['last_name']} | سمت: {emp['position']}")
    
    return filtered_employees


def get_teachers_by_grade(grade):
    """گرفتن لیست معلمان یک پایه خاص"""
    try:
        # همه کارکنان رو بگیر
        all_employees = get_employees()
        
        # فیلتر کن فقط معلمان این پایه رو
        teachers = [
            emp for emp in all_employees 
            if emp.get('position') == f'teacher_grade{grade}'
        ]
        
        return teachers
    except Exception as e:
        print(f"Error getting teachers: {e}")
        return []


def get_teachers_by_grade(grade):
    """گرفتن لیست معلمان یک پایه خاص"""
    try:
        all_employees = get_employees()
        print(f"🔍 تعداد کل کارکنان: {len(all_employees)}")
        
        teachers = [
            emp for emp in all_employees 
            if emp.get('position') == f'teacher_grade{grade}'
        ]
        
        print(f"🎯 تعداد معلمان پایه {grade}: {len(teachers)}")
        for teacher in teachers:
            print(f"   - {teacher['first_name']} {teacher['last_name']}")
        
        return teachers
    except Exception as e:
        print(f"❌ Error getting teachers: {e}")
        return []

def get_grade_choices():
    """گرفتن لیست پایه‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/grade-choices/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting grade choices: {e}")
        return []

def get_transaction_categories():
    """گرفتن لیست دسته‌بندی‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/transaction-categories/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting transaction categories: {e}")
        return []
    
def get_gifted_grades():
    """گرفتن پایه‌های مجاز برای تیزهوشان از API"""
    try:
        response = requests.get(f"{BASE_URL}/gifted-grades/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting gifted grades: {e}")
        return []

def get_exam_types():
    """گرفتن انواع آزمون‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/exam-types/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting exam types: {e}")
        return []

def get_category_choices():
    """گرفتن لیست دسته‌بندی‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/category-choices/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting category choices: {e}")
        return []

def get_positions_by_category(category):
    """گرفتن سمت‌های یک دسته خاص از API - نسخه اصلاح شده"""
    try:
        print(f"🔍 درخواست سمت‌ها برای دسته: {category}")
        
        response = requests.get(
            f"{BASE_URL}/positions-by-category/",  # ✅ اسلش اضافه شد
            params={'category': category}  # ✅ با پارامتر درست
        )
        
        if response.status_code == 200:
            positions = response.json()
            print(f"✅ تعداد سمت‌های دریافت شده: {len(positions)}")
            return positions
        else:
            print(f"❌ خطا در دریافت سمت‌ها: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ خطا در get_positions_by_category: {e}")
        return []
    
def get_withdraw_categories():
    """گرفتن لیست دسته‌بندی‌های برداشت از API"""
    try:
        response = requests.get(f"{BASE_URL}/withdraw-categories/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting withdraw categories: {e}")
        return []
    
def get_employees_by_position(position):
    """گرفتن کارکنان بر اساس سمت از API"""
    try:
        response = requests.get(f"{BASE_URL}/employees-by-position/?position={position}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting employees by position: {e}")
        return []

def get_withdraw_categories():
    """گرفتن لیست دسته‌بندی‌های برداشت از API"""
    try:
        response = requests.get(f"{BASE_URL}/withdraw-categories/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting withdraw categories: {e}")
        return []

def get_utility_types():
    """گرفتن انواع قبض‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/utility-types/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting utility types: {e}")
        return []

def create_financial_summary(operation_type, filters):
    """ایجاد کامپوننت خلاصه مالی - نسخه حرفه‌ای"""
    
    print(f"🎯 ایجاد خلاصه مالی برای: {operation_type}")
    print(f"🔍 فیلترهای دریافتی: {filters}")
    
    # فراخوانی API برای گرفتن داده‌ها
    summary_data = fetch_financial_summary(filters)
    
    print(f"🔍 پاسخ خلاصه مالی: {summary_data}")
    
    if not summary_data.get('success'):
        print("❌ خطا در دریافت خلاصه مالی")
        return ft.Container()  # خالی برگردون اگر خطا داشت
    
    summary = summary_data.get('summary', {})
    print(f"📊 داده‌های خلاصه مالی: {summary}")

    if operation_type == 'deposit':
        total_deposits = summary.get('total_deposits', 0)
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.TRENDING_UP, color=COLORS["green_600"], size=32),
                ft.Column([
                    ft.Text("مجموع واریزها", 
                           size=16, 
                           color=COLORS["gray_600"],
                           weight=ft.FontWeight.W_500),
                    ft.Text(f"{total_deposits:,} تومان", 
                           size=22, 
                           weight=ft.FontWeight.BOLD, 
                           color=COLORS["green_600"])
                ], spacing=6)
            ], spacing=16),
            bgcolor=COLORS["green_50"],
            padding=24,
            border_radius=12,
            border=ft.border.all(2, COLORS["green_200"]),
            margin=ft.margin.only(top=20)
        )
        
    elif operation_type == 'withdraw':
        # جمع هوشمند از روی تراکنش‌های نمایش داده شده (همیشه درست!)
        transactions_data = fetch_filtered_transactions(filters).get('transactions', [])
        total_withdrawals = sum(
            int(float(t.get("amount") or 0)) 
            for t in transactions_data
        )

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.TRENDING_DOWN, color=COLORS["red_600"], size=32),
                ft.Column([
                    ft.Text("مجموع برداشت‌ها",
                        size=16,
                        color=COLORS["gray_600"],
                        weight=ft.FontWeight.W_500),
                    ft.Text(f"{total_withdrawals:,} تومان",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["red_600"])
                ], spacing=6)
            ], spacing=16),
            bgcolor=COLORS["red_50"],
            padding=24,
            border_radius=12,
            border=ft.border.all(2, COLORS["red_200"]),
            margin=ft.margin.only(top=20)
        )
        
    else:  # همه عملیات
        total_deposits = summary.get('total_deposits', 0)
        total_withdrawals = summary.get('total_withdrawals', 0)
        net_profit = summary.get('net_profit', 0)
        
        # تعیین رنگ سود/ضرر
        profit_color = COLORS["green_600"] if net_profit >= 0 else COLORS["red_600"]
        profit_icon = ft.Icons.TRENDING_UP if net_profit >= 0 else ft.Icons.TRENDING_DOWN
        
        return ft.Container(
            content=ft.Column([
                ft.Text("خلاصه مالی", 
                       size=18, 
                       weight=ft.FontWeight.BOLD, 
                       color=COLORS["gray_700"],
                       text_align=ft.TextAlign.CENTER),
                ft.Container(height=12),
                ft.Row([
                    # واریزها
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ARROW_UPWARD, color=COLORS["green_600"], size=28),
                            ft.Text(f"{total_deposits:,}", 
                                   size=20, 
                                   weight=ft.FontWeight.BOLD, 
                                   color=COLORS["green_600"]),
                            ft.Text("کل واریز", 
                                   size=14, 
                                   color=COLORS["gray_600"],
                                   weight=ft.FontWeight.W_500)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                        spacing=8),
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=8)
                    ),
                    
                    # خط جداکننده
                    ft.Container(
                        width=1,
                        height=60,
                        bgcolor=COLORS["gray_300"]
                    ),
                    
                    # برداشت‌ها
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ARROW_DOWNWARD, color=COLORS["red_600"], size=28),
                            ft.Text(f"{total_withdrawals:,}", 
                                   size=20, 
                                   weight=ft.FontWeight.BOLD, 
                                   color=COLORS["red_600"]),
                            ft.Text("کل برداشت", 
                                   size=14, 
                                   color=COLORS["gray_600"],
                                   weight=ft.FontWeight.W_500)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                        spacing=8),
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=8)
                    ),
                    
                    # خط جداکننده
                    ft.Container(
                        width=1,
                        height=60,
                        bgcolor=COLORS["gray_300"]
                    ),
                    
                    # سود خالص
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(profit_icon, color=profit_color, size=28),
                            ft.Text(f"{net_profit:,}", 
                                   size=20, 
                                   weight=ft.FontWeight.BOLD, 
                                   color=profit_color),
                            ft.Text("سود خالص", 
                                   size=14, 
                                   color=COLORS["gray_600"],
                                   weight=ft.FontWeight.W_500)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                        spacing=8),
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=8)
                    ),
                ]),
            ]),
            bgcolor=COLORS["white"],
            padding=24,
            border_radius=12,
            border=ft.border.all(2, COLORS["gray_200"]),
            margin=ft.margin.only(top=20),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )

def fetch_financial_summary(filters):
    """گرفتن خلاصه مالی از API - نسخه اصلاح شده"""
    try:
        # فیلترهای مورد نیاز برای خلاصه مالی
        summary_filters = {
            'operation_type': filters.get('operation_type'),
            'start_date': filters.get('start_date'),
            'end_date': filters.get('end_date'),
            'transaction_type': filters.get('transaction_type'),
            'withdraw_type': filters.get('withdraw_type'),
            'grade': filters.get('grade'),
            'classroom': filters.get('classroom'),
            'student': filters.get('student'),
            'exam_type': filters.get('exam_type'),
            'employee': filters.get('employee'),
            'position': filters.get('position'),
            'utility_type': filters.get('utility_type'),
            'teacher': filters.get('teacher'),
            'rent_type': filters.get('rent_type'),  # 🔥 این خط رو اضافه کن
            'description': filters.get('description')  # 🔥 اینم اگه لازمه
        }
        
        print(f"📡 درخواست خلاصه مالی با فیلترها: {summary_filters}")
        
        response = requests.get(
            f"{BASE_URL}/financial-summary/",
            params=summary_filters,
            timeout=10
        )
        
        print(f"🔍 وضعیت پاسخ خلاصه مالی: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ داده‌های خلاصه مالی دریافت شد: {data}")
            return data
        else:
            print(f"❌ خطا در دریافت خلاصه مالی: {response.text}")
            return {'success': False}
            
    except Exception as e:
        print(f"❌ خطا در دریافت خلاصه مالی: {e}")
        return {'success': False}

def get_all_categories():
    """گرفتن همه دسته‌بندی‌ها از API"""
    try:
        response = requests.get(f"{BASE_URL}/all-categories/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting all categories: {e}")
        return []

def get_deposit_categories():
    """گرفتن فقط دسته‌بندی‌های واریز"""
    all_categories = get_all_categories()
    deposit_categories = [
        cat for cat in all_categories 
        if cat[0] in ['tuition', 'buffet', 'breakfast', 'extra_class_income', 'gifted_class', 'exam']
    ]
    return deposit_categories

def get_withdraw_categories():
    """گرفتن فقط دسته‌بندی‌های برداشت"""
    all_categories = get_all_categories()
    withdraw_categories = [
        cat for cat in all_categories 
        if cat[0] in ['salary', 'insurance', 'purchase', 'rent', 'utilities', 'extra_class_cost', 'gifted_class_cost' ,'petty_cash', 'service']  # 🔥 service اضافه شد
    ]
    return withdraw_categories

def fetch_filtered_transactions(filters):
    """گرفتن داده‌های فیلتر شده از API - نسخه اصلاح شده"""
    try:
        print(f"🎯 ارسال فیلترها به API: {filters}")
        
        
        api_filters = filters.copy()
        if 'student' in api_filters and api_filters['student']:
            api_filters['student'] = api_filters['student']  # این خط رو حذف کن
        
        print(f"🔍 فیلترهای تبدیل شده برای API: {api_filters}")
        
        response = requests.get(
            f"{BASE_URL}/filtered-transactions/", 
            params=api_filters,
            timeout=10
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ داده‌های دریافت شده: {data.get('count', 0)} تراکنش")
            return data
        else:
            print(f"❌ خطای API: {response.status_code} - {response.text}")
            return {'success': False, 'count': 0, 'transactions': []}
            
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return {'success': False, 'count': 0, 'transactions': []}
    
def gregorian_to_jalali(gregorian_date):
    """تبدیل تاریخ میلادی به شمسی برای نمایش"""
    try:
        if not gregorian_date:
            return "-"
        
        # تبدیل رشته تاریخ میلادی به object
        date_obj = datetime.strptime(gregorian_date, '%Y-%m-%d')
        
        # تبدیل به تاریخ شمسی
        jalali_date = jdatetime.date.fromgregorian(
            year=date_obj.year,
            month=date_obj.month,
            day=date_obj.day
        )
        
        return jalali_date.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"⚠️ خطا در تبدیل تاریخ {gregorian_date}: {e}")
        return gregorian_date  # اگر خطا خورد، همون تاریخ اصلی رو برگردون
    
def gregorian_to_jalali_safe(gregorian_date_str):
    """تبدیل تاریخ میلادی به شمسی - برای نمایش در جدول"""
    try:
        if not gregorian_date_str:
            return "-"
        
        # تبدیل رشته تاریخ میلادی به object
        date_obj = datetime.strptime(gregorian_date_str, '%Y-%m-%d')
        
        # تبدیل به تاریخ شمسی
        jalali_date = jdatetime.date.fromgregorian(
            year=date_obj.year,
            month=date_obj.month,
            day=date_obj.day
        )
        
        return jalali_date.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"⚠️ خطا در تبدیل تاریخ {gregorian_date_str}: {e}")
        return gregorian_date_str  # اگر خطا خورد، همون تاریخ اصلی رو برگردون
    
def safe_int(value):
    """تبدیل امن مقدار به عدد"""
    try:
        if isinstance(value, str):
            value = value.replace(',', '')
        return int(float(value))
    except:
        return 0

def create_dynamic_table(transactions, page, on_filter_click):
    """ایجاد جدول پویا بر اساس نوع داده‌ها - با تاریخ شمسی و دکمه جزئیات"""
    
    def delete_transaction_local(transaction_id):
        """تابع حذف محلی - کاملاً مستقل"""
        try:
            print(f"🎯 در حال حذف تراکنش {transaction_id}...")
            
            response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}/")
            
            if response.status_code == 204:
                # نمایش پیام موفقیت
                page.dialog = ft.AlertDialog(
                    title=ft.Text("✅ موفق"),
                    content=ft.Text("تراکنش با موفقیت حذف شد"),
                    actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog())]
                )
                page.dialog.open = True
                page.update()
                
                # رفرش جدول بعد از 1 ثانیه
                import threading
                def refresh_table():
                    import time
                    time.sleep(1)
                    if on_filter_click:
                        on_filter_click(None)
                
                threading.Thread(target=refresh_table).start()
                    
            else:
                print(f"❌ خطا در حذف: {response.status_code}")
                page.dialog = ft.AlertDialog(
                    title=ft.Text("❌ خطا"),
                    content=ft.Text("خطا در حذف تراکنش"),
                    actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog())]
                )
                page.dialog.open = True
                page.update()
                
        except Exception as e:
            print(f"❌ خطا: {str(e)}")
            page.dialog = ft.AlertDialog(
                title=ft.Text("❌ خطا"),
                content=ft.Text(f"خطا: {str(e)}"),
                actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog())]
            )
            page.dialog.open = True
            page.update()
    
    def show_transaction_details_wrapper(transaction):
        """Wrapper function that has access to page"""
        def show_transaction_details(e):
            """نمایش جزئیات کامل تراکنش در دیالوگ"""
            print(f"🎯 نمایش جزئیات برای تراکنش: {transaction['id']}")
            
            # تبدیل تاریخ میلادی به شمسی برای نمایش
            display_date = gregorian_to_jalali_safe(transaction['date'])
            
            # ایجاد محتوای دیالوگ
            content_items = [
                ft.Text(f"💰 مبلغ: {int(transaction['amount']):,} تومان", 
                       size=16, weight=ft.FontWeight.BOLD, color=COLORS["green_600"]),
                ft.Text(f"📅 تاریخ: {display_date}", size=14),
                ft.Text(f"🔸 نوع تراکنش: {transaction.get('transaction_type_display', '-')}", size=14),
                ft.Text(f"🏷️ دسته‌بندی: {transaction.get('category_display', '-')}", size=14),
            ]
            
            # اضافه کردن اطلاعات دانش‌آموز اگر وجود دارد
            if transaction.get('student_name') and transaction.get('student_name') != '-':
                content_items.append(
                    ft.Text(f"👦 دانش‌آموز: {transaction.get('student_name', '-')}", size=14)
                )
            
            # اضافه کردن اطلاعات کارمند اگر وجود دارد
            if transaction.get('employee_name') and transaction.get('employee_name') != '-':
                content_items.append(
                    ft.Text(f"👨‍💼 کارمند: {transaction.get('employee_name', '-')}", size=14)
                )
            
            # اضافه کردن اطلاعات کلاس اگر وجود دارد
            if transaction.get('classroom_name'):
                content_items.append(
                    ft.Text(f"🏫 کلاس: {transaction.get('classroom_name', '-')}", size=14)
                )
            
            # اضافه کردن اطلاعات پایه اگر وجود دارد
            if transaction.get('grade'):
                content_items.append(
                    ft.Text(f"📚 پایه: {transaction.get('grade', '-')}", size=14)
                )
            
            # اضافه کردن روش پرداخت
            if transaction.get('payment_method_display'):
                content_items.append(
                    ft.Text(f"💳 روش پرداخت: {transaction.get('payment_method_display', '-')}", size=14)
                )
            
            # اضافه کردن شماره رسید اگر وجود دارد
            if transaction.get('receipt_number'):
                content_items.append(
                    ft.Text(f"🧾 شماره رسید: {transaction.get('receipt_number', '-')}", size=14)
                )
            
            # اضافه کردن توضیحات
            description = transaction.get('description', 'بدون توضیح')
            content_items.extend([
                ft.Text("📝 شرح تراکنش:", size=14, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        description,
                        size=14,
                        color=COLORS["gray_700"],
                        selectable=True  # 🔥 این خط رو اضافه کن
                    ),
                    padding=12,
                    bgcolor=COLORS["gray_50"],
                    border_radius=8,
                    width=450,
                    margin=ft.margin.only(top=8)
                )
            ])
            
            dialog = ft.AlertDialog(
                title=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=COLORS["blue_600"]),
                    ft.Text("جزئیات کامل تراکنش", size=18, weight=ft.FontWeight.BOLD)
                ]),
                content=ft.Container(
                    content=ft.Column(
                        content_items,
                        spacing=8,
                        scroll=ft.ScrollMode.ADAPTIVE
                    ),
                    height=min(400, 150 + len(description) // 3),  # ارتفاع داینامیک
                    width=500
                ),
                actions=[
                    ft.TextButton(
                        "بستن", 
                        on_click=lambda _:page.close(dialog),
                        style=ft.ButtonStyle(color=COLORS["blue_600"])
                    )
                ]
            )
            page.open(dialog)
            page.update()        
        return show_transaction_details
    
    

    if not transactions:
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=COLORS["gray_400"]),
                ft.Text("هیچ تراکنشی یافت نشد", size=18, color=COLORS["gray_600"], weight=ft.FontWeight.BOLD),
                ft.Text("لطفاً فیلترهای دیگری را امتحان کنید", size=14, color=COLORS["gray_500"])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
            padding=60,
            alignment=ft.alignment.center
        )
    
    # تشخیص نوع داده‌ها برای تعیین ستون‌ها
    has_student = any(t.get('student_name') and t.get('student_name') != '-' for t in transactions)
    has_employee = any(t.get('employee_name') and t.get('employee_name') != '-' for t in transactions)
    has_classroom = any(t.get('classroom_name') for t in transactions)
    
    # تعریف ستون‌های پویا
    columns = []
    
    # ستون‌های ثابت
    columns.extend([
        ft.DataColumn(ft.Text("تاریخ", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("نوع تراکنش", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("دسته‌بندی", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("مبلغ (تومان)", weight=ft.FontWeight.BOLD)),
    ])
    
    # ستون‌های شرطی
    if has_student:
        columns.append(ft.DataColumn(ft.Text("دانش‌آموز", weight=ft.FontWeight.BOLD)))
    
    if has_employee:
        columns.append(ft.DataColumn(ft.Text("کارمند", weight=ft.FontWeight.BOLD)))
    
    if has_classroom:
        columns.append(ft.DataColumn(ft.Text("کلاس", weight=ft.FontWeight.BOLD)))
    
    columns.append(ft.DataColumn(ft.Text("شرح", weight=ft.FontWeight.BOLD)))
    columns.append(ft.DataColumn(ft.Text("عملیات", weight=ft.FontWeight.BOLD)))
    
    # ایجاد ردیف‌های داده با تاریخ شمسی
    data_rows = []
    for transaction in transactions:
        # ✅ تبدیل تاریخ میلادی به شمسی برای نمایش
        display_date = gregorian_to_jalali_safe(transaction['date'])
        
        cells = [
            ft.DataCell(ft.Text(display_date)),  # ✅ تاریخ شمسی
            ft.DataCell(ft.Text(transaction.get('transaction_type_display', ''))),
            ft.DataCell(ft.Text(transaction.get('category_display', ''))),
            ft.DataCell(ft.Text(f"{int(transaction['amount']):,}")),
        ]
        
        # سلول‌های شرطی
        if has_student:
            cells.append(ft.DataCell(ft.Text(transaction.get('student_name', '-'))))
        
        if has_employee:
            cells.append(ft.DataCell(ft.Text(transaction.get('employee_name', '-'))))
        
        if has_classroom:
            cells.append(ft.DataCell(ft.Text(transaction.get('classroom_name', '-'))))
        
        # نمایش توضیحات کوتاه در جدول
        description = transaction.get('description', '-')
        short_description = description[:50] + "..." if len(description) > 50 else description
        cells.append(ft.DataCell(ft.Text(short_description)))
        
        # 🔥 دکمه‌های عملیات - نسخه اصلاح شده
        action_cell_content = ft.Row([
            # دکمه مشاهده جزئیات
            ft.IconButton(
                icon=ft.Icons.REMOVE_RED_EYE,
                icon_color=COLORS["blue_600"],
                icon_size=20,
                tooltip="مشاهده جزئیات",
                on_click=show_transaction_details_wrapper(transaction)  # 🔥 اینجا درست شده
            ),
            # دکمه حذف
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=COLORS["red_600"],
                icon_size=20,
                tooltip="حذف تراکنش",
                on_click=lambda e, t_id=transaction['id']: delete_transaction_local(t_id)
            )
        ], spacing=8)
        
        cells.append(ft.DataCell(action_cell_content))
        
        data_rows.append(ft.DataRow(cells=cells))
    
    return ft.Container(
        content=ft.Column([
            # هدر نتیجه
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FILTER_LIST, color=COLORS["green_600"]),
                    ft.Text(f"تعداد نتایج: {len(transactions)} تراکنش", 
                           size=16, weight=ft.FontWeight.BOLD, color=COLORS["green_600"])
                ], spacing=8),
                bgcolor=COLORS["green_50"],
                padding=12,
                border_radius=8,
                margin=ft.margin.only(bottom=16)
            ),
            
            # جدول
            ft.Container(
                content=ft.DataTable(
                    columns=columns,
                    rows=data_rows,
                    vertical_lines=ft.border.BorderSide(1, COLORS["gray_300"]),
                    horizontal_lines=ft.border.BorderSide(1, COLORS["gray_200"]),
                    heading_row_color=COLORS["blue_50"],
                    heading_row_height=48,
                    data_row_max_height=60,
                ),
                padding=16,
            )
        ]),
        bgcolor=COLORS["white"],
        border_radius=12,
        margin=ft.margin.only(top=20),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )

def check_available_fonts():
    """بررسی فونت‌های موجود در سیستم"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.fonts import addMapping
    
    print("🔍 در حال بررسی فونت‌های موجود...")
    
    # لیست فونت‌های پیش‌فرض ReportLab
    default_fonts = ['Helvetica', 'Times-Roman', 'Courier', 'Symbol']
    
    for font in default_fonts:
        try:
            pdfmetrics.getFont(font)
            print(f"✅ فونت {font} موجود است")
        except:
            print(f"❌ فونت {font} موجود نیست")
    
    # فونت‌های فارسی احتمالی
    persian_fonts = ['DejaVuSans', 'Arial', 'Tahoma']
    
    for font in persian_fonts:
        try:
            pdfmetrics.getFont(font)
            print(f"🎉 فونت فارسی {font} موجود است!")
            return font
        except:
            print(f"⚠️ فونت {font} موجود نیست")
    
    return 'Helvetica'  # فونت پیش‌فرض

def create_pdf_report(transactions, filters=None):
    """ایجاد گزارش HTML ساده به جای PDF"""
    try:
        print("🎯 ایجاد گزارش HTML ساده...")
        
        # ایجاد HTML ساده
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <title>گزارش مالی مدرسه</title>
            <style>
                body {{ font-family: Tahoma, Arial, sans-serif; direction: rtl; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
                .total {{ font-weight: bold; background-color: #e8f4fd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>گزارش مالی - سیستم حسابداری مدرسه</h1>
                <p>تاریخ ایجاد: {jdatetime.datetime.now().strftime('%Y/%m/%d - %H:%M')}</p>
            </div>
            
            <h2>خلاصه تراکنش‌ها</h2>
            <table>
                <thead>
                    <tr>
                        <th>ردیف</th>
                        <th>تاریخ</th>
                        <th>نوع</th>
                        <th>دسته‌بندی</th>
                        <th>مبلغ (تومان)</th>
                        <th>شرح</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        total_amount = 0
        total_deposits = 0
        total_withdrawals = 0
        
        for i, transaction in enumerate(transactions, 1):
            display_date = gregorian_to_jalali_safe(transaction['date'])
            amount = safe_int(transaction['amount'])
            transaction_type = 'واریز' if transaction.get('transaction_type') == 'deposit' else 'برداشت'
            
            total_amount += amount
            if transaction.get('transaction_type') == 'deposit':
                total_deposits += amount
            else:
                total_withdrawals += amount
            
            html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{display_date}</td>
                        <td>{transaction_type}</td>
                        <td>{transaction.get('category_display', '-')}</td>
                        <td>{amount:,}</td>
                        <td>{transaction.get('description', '-')}</td>
                    </tr>
            """
        
        html_content += f"""
                </tbody>
            </table>
            
            <div class="total">
                <h3>خلاصه مالی</h3>
                <p>تعداد تراکنش‌ها: {len(transactions):,}</p>
                <p>مجموع واریزها: {total_deposits:,} تومان</p>
                <p>مجموع برداشت‌ها: {total_withdrawals:,} تومان</p>
                <p>مانده خالص: {total_deposits - total_withdrawals:,} تومان</p>
            </div>
        </body>
        </html>
        """
        
        # ذخیره فایل HTML
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
            f.write(html_content)
            html_file = f.name
        
        print("✅ گزارش HTML با موفقیت ایجاد شد!")
        return html_file, True, "گزارش HTML با موفقیت ایجاد شد"
        
    except Exception as e:
        print(f"❌ خطا در ایجاد گزارش: {str(e)}")
        return None, False, f"خطا: {str(e)}"

def print_transactions_pdf(transactions, filters=None):
    """چاپ گزارش - نسخه HTML"""
    try:
        print("🎯 ایجاد گزارش برای چاپ...")
        
        # استفاده از نسخه HTML
        html_file, success, message = create_pdf_report(transactions, filters)
        
        if success and html_file:
            print(f"✅ HTML ایجاد شد: {html_file}")
            webbrowser.open(f'file://{html_file}')
            return True, "گزارش با موفقیت ایجاد شد"
        else:
            return False, message
            
    except Exception as e:
        print(f"❌ خطا در ایجاد گزارش: {str(e)}")
        return False, f"خطا در ایجاد گزارش: {str(e)}"

def convert_gregorian_to_jalali_safe(gregorian_date_str):
    """تبدیل تاریخ میلادی به شمسی - برای نمایش"""
    try:
        if not gregorian_date_str:
            return None
            
        print(f"🔍 تبدیل تاریخ میلادی به شمسی: {gregorian_date_str}")
        
        # تبدیل رشته به تاریخ میلادی
        from datetime import datetime
        gregorian_date = datetime.strptime(gregorian_date_str, "%Y-%m-%d").date()
        
        # تبدیل به تاریخ شمسی
        jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
        result = jalali_date.strftime("%Y-%m-%d")
        
        print(f"✅ تبدیل موفق: {gregorian_date_str} → {result}")
        return result
        
    except Exception as e:
        print(f"❌ خطا در تبدیل تاریخ میلادی {gregorian_date_str}: {e}")
        return gregorian_date_str  # اگر خطا خورد، همون میلادی رو برگردون
    
def create_petty_cash(petty_cash_data):
    """ثبت تنخواه در API - نسخه هوشمند تاریخ"""
    try:
        jalali_date = petty_cash_data['payment_date']
        
        # 🔼 استفاده از سرویس تاریخ هوشمند (همون منطق بخش‌های دیگه)
        try:
            # اول سعی کن به عنوان تاریخ شمسی parse کن
            gregorian_date = jdatetime.datetime.strptime(jalali_date, '%Y-%m-%d').togregorian()
            print(f"📅 تشخیص تاریخ شمسی: {jalali_date} → {gregorian_date}")
        except ValueError:
            try:
                # اگر شمسی نبود، سعی کن به عنوان میلادی parse کن
                gregorian_date = datetime.strptime(jalali_date, '%Y-%m-%d').date()
                print(f"📅 تشخیص تاریخ میلادی: {jalali_date} → {gregorian_date}")
            except ValueError:
                print(f"❌ فرمت تاریخ نامعتبر: {jalali_date}")
                return False, "فرمت تاریخ نامعتبر است"
        
        transaction_data = {
            'transaction_type': 'withdraw',     # برداشت
            'category': 'petty_cash',           # تنخواه
            'amount': petty_cash_data['amount'],
            'date': gregorian_date.strftime("%Y-%m-%d"),  # تاریخ میلادی
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"تنخواه گردان - {petty_cash_data.get('description', '')}",
            'receipt_number': petty_cash_data.get('receipt_number', '')
        }
        
        print(f"🔍 داده‌های تراکنش تنخواه: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "تنخواه با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت تنخواه: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"

def create_service_payment(service_data):
    """ثبت هزینه سرویس در API"""
    try:
        jalali_date = service_data['payment_date']
        
        # استفاده از سرویس تاریخ هوشمند
        try:
            gregorian_date = jdatetime.datetime.strptime(jalali_date, '%Y-%m-%d').togregorian()
            print(f"📅 تشخیص تاریخ شمسی: {jalali_date} → {gregorian_date}")
        except ValueError:
            try:
                gregorian_date = datetime.strptime(jalali_date, '%Y-%m-%d').date()
                print(f"📅 تشخیص تاریخ میلادی: {jalali_date} → {gregorian_date}")
            except ValueError:
                print(f"❌ فرمت تاریخ نامعتبر: {jalali_date}")
                return False, "فرمت تاریخ نامعتبر است"
        
        transaction_data = {
            'transaction_type': 'withdraw',     # برداشت
            'category': 'service',              # سرویس
            'amount': service_data['amount'],
            'date': gregorian_date.strftime("%Y-%m-%d"),
            'payment_method': 'cash',           # پیش‌فرض نقدی
            'description': f"هزینه سرویس - {service_data.get('description', '')}",
            'receipt_number': ''
        }
        
        print(f"🔍 داده‌های تراکنش سرویس: {transaction_data}")
        
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=transaction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"🔍 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 201:
            return True, "هزینه سرویس با موفقیت ثبت شد"
        else:
            print(f"❌ خطای API: {response.text}")
            return False, f"خطا در ثبت سرویس: {response.text}"
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return False, f"خطا در برقراری ارتباط: {e}"
    
def delete_transaction(transaction_id, page, refresh_callback=None):
    """حذف تراکنش از API - نسخه نهایی"""
    try:
        print(f"🎯 در حال حذف تراکنش {transaction_id}...")
        
        response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}/")
        
        if response.status_code == 204:
            # نمایش پیام موفقیت
            page.dialog = ft.AlertDialog(
                title=ft.Text("✅ موفق"),
                content=ft.Text("تراکنش با موفقیت حذف شد"),
                actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog(page))]
            )
            page.dialog.open = True
            
            # رفرش جدول اگر تابع callback وجود دارد
            if refresh_callback:
                refresh_callback(None)
                
        else:
            print(f"❌ خطا در حذف: {response.status_code}")
            page.dialog = ft.AlertDialog(
                title=ft.Text("❌ خطا"),
                content=ft.Text("خطا در حذف تراکنش"),
                actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog(page))]
            )
            page.dialog.open = True
            
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
        page.dialog = ft.AlertDialog(
            title=ft.Text("❌ خطا"),
            content=ft.Text(f"خطا: {str(e)}"),
            actions=[ft.TextButton("باشه", on_click=lambda e: close_dialog(page))]
        )
        page.dialog.open = True

def close_dialog(page):
    """بستن دیالوگ"""
    page.dialog.open = False
    page.update()


def main(page: ft.Page):
    # تنظیمات صفحه
    page.title = "دبستان شاهدان قلم"
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    selected_category = None 
    current_employee = None
    selected_exam_type = None
    current_teacher = None
    page.fonts = {
        "Vazirmatn": "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn[wght].ttf"
    }
    page.theme = ft.Theme(font_family="Vazirmatn")

    # متغیرهای اصلی
    current_page = "login"
    selected_grade = ""
    selected_classroom = None
    current_student = None
    selected_category = None
    selected_exam_type = None
    
    # فیلترهای صفحه حساب کتاب
    transactions_current = [] 
    ledger_filters = {}

    selected_utility_type = None  # آب، برق یا گاز

    
    username_field = ft.TextField(
        hint_text="نام کاربری خود را وارد کنید",
        border_radius=8,
        border_color=COLORS["gray_300"],
        focused_border_color=COLORS["blue_600"],
        height=52,
        text_size=14,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=COLORS["white"]
    )
    
    password_field = ft.TextField(
        hint_text="رمز عبور خود را وارد کنید",
        border_radius=8,
        border_color=COLORS["gray_300"],
        focused_border_color=COLORS["blue_600"],
        height=52,
        text_size=14,
        password=True,
        can_reveal_password=True,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=COLORS["white"]
    )

    # توابع مدیریت صفحات
    def show_login(e=None):
        nonlocal current_page
        current_page = "login"
        username_field.value = ""
        password_field.value = ""
        update_display()
    
    def show_main(e=None):
        nonlocal current_page
        current_page = "main"
        update_display()
    
    def show_deposit_type(e=None):
        nonlocal current_page
        current_page = "deposit_type"
        update_display()
    
    def show_withdraw_type(e=None):
        nonlocal current_page
        current_page = "withdraw_type"
        update_display()
    
    def show_tuition_grade(e=None):
        nonlocal current_page
        current_page = "tuition_grade"
        update_display()
    
    def show_class_selection(grade):
        nonlocal current_page, selected_grade
        current_page = "class_selection"
        selected_grade = grade
        update_display()
    
    def show_student_list(classroom):
        nonlocal current_page, selected_classroom
        current_page = "student_list"
        selected_classroom = classroom
        update_display()
    
    def show_tuition_payment(student):
        nonlocal current_page, current_student
        current_page = "tuition_payment"
        current_student = student
        update_display()

    def show_student_list_page():
        nonlocal current_page
        current_page = "student_list"
        update_display()
    
    def show_ledger_page(e=None):
        nonlocal current_page
        current_page = "ledger"
        update_display()

    def show_cafeteria_sales(e=None):
        nonlocal current_page
        current_page = "cafeteria_sales"
        update_display()

    def show_breakfast_sales(e=None):
        nonlocal current_page
        current_page = "breakfast_sales"
        update_display()

    def show_purchase_page(e=None):
        nonlocal current_page
        current_page = "purchase"
        update_display()

    def show_extra_class_grade(e=None):
        nonlocal current_page
        current_page = "extra_class_grade"
        update_display()

    def show_extra_class_selection(grade):
        """نمایش صفحه انتخاب کلاس برای کلاس تقویتی"""
        nonlocal current_page, selected_grade
        current_page = "extra_class_selection"
        selected_grade = grade
        update_display()

    def show_extra_class_payment(student):
        nonlocal current_page, current_student
        current_page = "extra_class_payment"
        current_student = student
        update_display()

    def show_extra_class_student_list(classroom):
        """نمایش لیست دانش‌آموزان برای کلاس تقویتی"""
        nonlocal current_page, selected_classroom
        current_page = "extra_class_student_list"  # این متفاوته
        selected_classroom = classroom
        update_display()

    def show_gifted_class_grade(e=None):
        """نمایش صفحه انتخاب پایه برای تیزهوشان"""
        nonlocal current_page
        current_page = "gifted_class_grade"
        update_display()

    def show_gifted_class_selection(grade):
        """نمایش صفحه انتخاب کلاس برای تیزهوشان"""
        nonlocal current_page, selected_grade
        print(f"🎯 وارد gifted_class_selection - current_page قبل: {current_page}")
        current_page = "gifted_class_selection"
        selected_grade = grade
        print(f"🎯 وارد gifted_class_selection - current_page بعد: {current_page}")
        update_display()

    def show_gifted_class_student_list(classroom):
        """نمایش لیست دانش‌آموزان برای تیزهوشان"""
        nonlocal current_page, selected_classroom
        print(f"🎯 وارد gifted_class_student_list - current_page: {current_page}")
        current_page = "gifted_class_student_list"
        selected_classroom = classroom
        update_display()

    def show_gifted_class_payment(student):
        nonlocal current_page, current_student
        print(f"🎯 show_gifted_class_payment فراخوانی شد برای: {student['first_name']}")
        print(f"🎯 current_page قبل: {current_page}")
        current_page = "gifted_class_payment"
        current_student = student
        print(f"🎯 current_page بعد: {current_page}")
        update_display()
        print("🎯 update_display فراخوانی شد")

    def show_exam_type_page(e=None):
        nonlocal current_page
        current_page = "exam_type"
        update_display()

    def show_exam_class_selection(exam_type, grade):
        nonlocal current_page, selected_exam_type, selected_grade
        current_page = "exam_class_selection"
        selected_exam_type = exam_type
        selected_grade = grade
        update_display()


    def show_salary_position_selection(e=None):
        nonlocal current_page
        current_page = "salary_position_selection"
        update_display()

    def show_salary_employee_list(category):
        """نمایش لیست کارکنان یک دسته سمت"""
        nonlocal current_page, selected_category
        current_page = "salary_employee_list"
        selected_category = category 
        update_display()

    def show_salary_payment_page(employee):
        """نمایش صفحه پرداخت حقوق"""
        nonlocal current_page, current_employee
        current_page = "salary_payment"
        current_employee = employee
        update_display()

    def show_exam_grade_selection(exam_type):
        """نمایش صفحه انتخاب پایه برای آزمون"""
        nonlocal current_page, selected_exam_type
        current_page = "exam_grade_selection"
        selected_exam_type = exam_type
        update_display()

    def show_exam_class_selection(exam_type, grade):
        nonlocal current_page, selected_exam_type, selected_grade
        current_page = "exam_class_selection"
        selected_exam_type = exam_type
        selected_grade = grade
        update_display()

    def show_exam_student_list(exam_type, grade, classroom):
        """نمایش لیست دانش‌آموزان برای آزمون"""
        nonlocal current_page, selected_exam_type, selected_grade, selected_classroom
        current_page = "exam_student_list"
        selected_exam_type = exam_type
        selected_grade = grade
        selected_classroom = classroom
        update_display()

    def show_teacher_list(grade):
        """نمایش لیست معلمان یک پایه"""
        nonlocal current_page, selected_grade
        current_page = "teacher_list"
        selected_grade = grade
        update_display()

    def show_extra_class_teacher_payment(teacher):
        """نمایش صفحه پرداخت به معلم"""
        nonlocal current_page, current_teacher
        current_page = "extra_class_teacher_payment" 
        current_teacher = teacher
        update_display()
        
    def show_insurance_employee_list(category):
        """نمایش لیست کارکنان برای بیمه"""
        nonlocal current_page, selected_category
        current_page = "insurance_employee_list"
        selected_category = category
        update_display()

    def show_exam_payment_page(exam_type, student):
        """نمایش صفحه پرداخت آزمون"""
        nonlocal current_page, selected_exam_type, current_student
        current_page = "exam_payment"
        selected_exam_type = exam_type
        current_student = student
        update_display()
    
    def show_alert(message):
        dlg = ft.AlertDialog(
            title=ft.Text("اطلاع"),
            content=ft.Text(message),
            actions=[ft.TextButton("باشه", on_click=lambda e: page.close(dlg))]
        )
        page.open(dlg)
        page.update()

    def show_extra_class_withdraw_grade(e=None):
        """نمایش صفحه انتخاب پایه برای کلاس تقویتی (در بخش برداشت)"""
        nonlocal current_page
        current_page = "extra_class_withdraw_grade"
        update_display()

    def show_insurance_page(e=None):
        """نمایش صفحه بیمه"""
        nonlocal current_page
        current_page = "insurance"
        update_display()

    def show_insurance_payment_page(employee):
        """نمایش صفحه پرداخت بیمه"""
        nonlocal current_page, current_employee
        current_page = "insurance_payment"
        current_employee = employee
        update_display()

    def show_petty_cash_page(e=None):
        """نمایش صفحه ثبت تنخواه"""
        nonlocal current_page
        current_page = "petty_cash"
        update_display()

    def show_service_page(e=None):
        """نمایش صفحه ثبت سرویس"""
        nonlocal current_page
        current_page = "service"
        update_display()

    def show_rent_type_selection(e=None):
        """نمایش صفحه انتخاب نوع کرایه (صفحه با دو دکمه)"""
        nonlocal current_page
        current_page = "rent_type_selection"
        update_display()

    def show_rent_page(e=None):
        nonlocal current_page
        current_page = "rent"
        update_display()

    def show_gym_rent_page(e=None):
        """نمایش صفحه ثبت کرایه باشگاه"""
        nonlocal current_page
        current_page = "gym_rent"
        update_display()

    def show_gifted_class_withdraw_grade(e=None):
        """نمایش صفحه انتخاب پایه برای هزینه کلاس تیزهوشان"""
        nonlocal current_page
        current_page = "gifted_class_withdraw_grade"
        update_display()

    def show_gifted_class_teacher_list(grade):
        """نمایش لیست معلمان تیزهوشان یک پایه"""
        nonlocal current_page, selected_grade
        current_page = "gifted_class_teacher_list"
        selected_grade = grade
        update_display()

    def show_gifted_class_teacher_payment(teacher):
        """نمایش صفحه پرداخت به معلم تیزهوشان"""
        nonlocal current_page, current_teacher
        current_page = "gifted_class_teacher_payment"
        current_teacher = teacher
        update_display()

    def show_transaction_details(transaction):
        """نمایش جزئیات کامل تراکنش در دیالوگ"""
        dialog = ft.AlertDialog(
            title=ft.Text("جزئیات تراکنش"),
            content=ft.Column([
                ft.Text(f"مبلغ: {transaction['amount']:,} تومان", size=16),
                ft.Text(f"تاریخ: {transaction['date']}", size=16),
                ft.Text(f"نوع: {transaction.get('transaction_type_display', '')}", size=16),
                ft.Text(f"دسته‌بندی: {transaction.get('category_display', '')}", size=16),
                ft.Text(f"شرح:", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        transaction.get('description', 'بدون توضیح'),
                        size=14,
                        color=COLORS["gray_700"]
                    ),
                    padding=10,
                    bgcolor=COLORS["gray_100"],
                    border_radius=8,
                    width=400
                )
            ], scroll=ft.ScrollMode.ADAPTIVE, height=300),
            actions=[ft.TextButton("بستن", on_click=lambda e: close_dialog())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # ساخت آیکون‌ها
    def create_icon(icon_name, color, bg_color, size=32):
        return ft.Container(
            width=size + 32,
            height=size + 32,
            border_radius=(size + 32) // 2,
            bgcolor=bg_color,
            content=ft.Icon(
                name=icon_name,
                color=color,
                size=size
            ),
            alignment=ft.alignment.center
        )

    # ساخت دایره عددی
    def create_number_circle(number, color, bg_color, size=80):
        return ft.Container(
            width=size,
            height=size,
            border_radius=size // 2,
            bgcolor=bg_color,
            content=ft.Text(
                number,
                size=size // 2.5,
                weight=ft.FontWeight.BOLD,
                color=color
            ),
            alignment=ft.alignment.center
        )

    # صفحه لاگین
    def create_login_page():
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            padding=20,
            content=ft.Column(
                [
                    ft.Container(height=100),
                    ft.Container(
                        width=400,
                        bgcolor=COLORS["white"],
                        border_radius=16,
                        padding=32,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=25,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 10)
                        ),
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            create_icon(
                                                ft.Icons.BOOK_OUTLINED,
                                                COLORS["blue_600"],
                                                COLORS["blue_100"],
                                                32
                                            ),
                                            ft.Text(
                                                "سیستم حسابداری مدرسه",
                                                size=28,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["gray_900"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=8),
                                            ft.Text(
                                                "لطفاً وارد حساب کاربری خود شوید",
                                                size=16,
                                                color=COLORS["gray_600"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=32),
                                
                                ft.Column(
                                    [
                                        ft.Container(
                                            content=ft.Text(
                                                "نام کاربری",
                                                size=14,
                                                weight=ft.FontWeight.W_500,
                                                color=COLORS["gray_900"],
                                                text_align=ft.TextAlign.RIGHT
                                            ),
                                            alignment=ft.alignment.center_right,
                                            padding=ft.padding.only(bottom=8)
                                        ),
                                        username_field
                                    ],
                                    spacing=0,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH
                                ),
                                
                                ft.Container(height=24),
                                
                                ft.Column(
                                    [
                                        ft.Container(
                                            content=ft.Text(
                                                "رمز عبور",
                                                size=14,
                                                weight=ft.FontWeight.W_500,
                                                color=COLORS["gray_900"],
                                                text_align=ft.TextAlign.RIGHT
                                            ),
                                            alignment=ft.alignment.center_right,
                                            padding=ft.padding.only(bottom=8)
                                        ),
                                        password_field
                                    ],
                                    spacing=0,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH
                                ),
                                
                                ft.Container(height=32),
                                
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Text(
                                            "ورود به سیستم",
                                            size=16,
                                            weight=ft.FontWeight.W_500,
                                            color=COLORS["white"]
                                        ),
                                        width=400,
                                        height=52,
                                        on_click=lambda e: show_main() if username_field.value and password_field.value else None,
                                        style=ft.ButtonStyle(
                                            bgcolor=COLORS["blue_600"],
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=16)
                                        )
                                    )
                                )
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            )
        )

    # صفحه اصلی
    def create_main_page():
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        create_icon(
                                            ft.Icons.BOOK_OUTLINED,
                                            COLORS["blue_600"],
                                            COLORS["blue_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "سیستم حسابداری مدرسه",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.LOGOUT,
                                    icon_color=COLORS["gray_600"],
                                    on_click=show_login,
                                    tooltip="خروج"
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "خوش آمدید",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "عملیات مورد نظر خود را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    width=1000,
                                    content=ft.Row(
                                        [
                                            # دکمه برداشت
                                            ft.Container(
                                                width=300,
                                                bgcolor=COLORS["white"],
                                                border_radius=16,
                                                padding=32,
                                                shadow=ft.BoxShadow(
                                                    spread_radius=1,
                                                    blur_radius=25,
                                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                                    offset=ft.Offset(0, 10)
                                                ),
                                                on_click=lambda e: show_withdraw_type(),
                                                content=ft.Column(
                                                    [
                                                        create_icon(
                                                            ft.Icons.ARROW_UPWARD,
                                                            COLORS["red_600"],
                                                            COLORS["red_100"],
                                                            32
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Text(
                                                            "برداشت از حساب",
                                                            size=24,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=COLORS["gray_900"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=16),
                                                        ft.Text(
                                                            "برداشت وجه از حساب مدرسه",
                                                            size=16,
                                                            color=COLORS["gray_600"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Container(
                                                            bgcolor=COLORS["red_50"],
                                                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                                            border_radius=8,
                                                            content=ft.Text(
                                                                "کلیک کنید",
                                                                size=14,
                                                                weight=ft.FontWeight.W_500,
                                                                color=COLORS["red_600"]
                                                            )
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    spacing=0
                                                )
                                            ),
                                            
                                            ft.Container(width=20),
                                            
                                            # دکمه واریز
                                            ft.Container(
                                                width=300,
                                                bgcolor=COLORS["white"],
                                                border_radius=16,
                                                padding=32,
                                                shadow=ft.BoxShadow(
                                                    spread_radius=1,
                                                    blur_radius=25,
                                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                                    offset=ft.Offset(0, 10)
                                                ),
                                                on_click=lambda e: show_deposit_type(),
                                                content=ft.Column(
                                                    [
                                                        create_icon(
                                                            ft.Icons.ATTACH_MONEY,
                                                            COLORS["green_600"],
                                                            COLORS["green_100"],
                                                            32
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Text(
                                                            "واریز به حساب",
                                                            size=24,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=COLORS["gray_900"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=16),
                                                        ft.Text(
                                                            "واریز وجه به حساب مدرسه",
                                                            size=16,
                                                            color=COLORS["gray_600"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Container(
                                                            bgcolor=COLORS["green_50"],
                                                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                                            border_radius=8,
                                                            content=ft.Text(
                                                                "کلیک کنید",
                                                                size=14,
                                                                weight=ft.FontWeight.W_500,
                                                                color=COLORS["green_600"]
                                                            )
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    spacing=0
                                                )
                                            ),
                                            
                                            ft.Container(width=20),
                                            
                                            # دکمه حساب کتاب
                                            ft.Container(
                                                width=300,
                                                bgcolor=COLORS["white"],
                                                border_radius=16,
                                                padding=32,
                                                shadow=ft.BoxShadow(
                                                    spread_radius=1,
                                                    blur_radius=25,
                                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                                    offset=ft.Offset(0, 10)
                                                ),
                                                on_click=lambda e: show_ledger_page(),
                                                content=ft.Column(
                                                    [
                                                        create_icon(
                                                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                                                            COLORS["blue_600"],
                                                            COLORS["blue_100"],
                                                            32
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Text(
                                                            "حساب کتاب",
                                                            size=24,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=COLORS["gray_900"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=16),
                                                        ft.Text(
                                                            "مشاهده گزارش‌های مالی",
                                                            size=16,
                                                            color=COLORS["gray_600"],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                        ft.Container(height=24),
                                                        ft.Container(
                                                            bgcolor=COLORS["blue_50"],
                                                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                                            border_radius=8,
                                                            content=ft.Text(
                                                                "کلیک کنید",
                                                                size=14,
                                                                weight=ft.FontWeight.W_500,
                                                                color=COLORS["blue_600"]
                                                            )
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    spacing=0
                                                )
                                            )
                                        ]
                                    )
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                spacing=0
            )
        )

    # صفحه انتخاب نوع واریز
    def create_deposit_type_page():
        deposit_options = [
            ("شهریه مدرسه", ft.Icons.HOME_WORK, COLORS["blue_600"], COLORS["blue_100"], "واریز شهریه تحصیلی"),
            ("بوفه", ft.Icons.SHOPPING_CART, COLORS["orange_600"], COLORS["orange_100"], "درآمد بوفه مدرسه"),
            ("صبحانه", ft.Icons.WB_SUNNY, COLORS["yellow_600"], COLORS["yellow_100"], "درآمد صبحانه مدرسه"),
            ("کلاس های تقویتی", ft.Icons.SCHOOL, COLORS["purple_600"], COLORS["purple_100"], "شهریه کلاس های تقویتی"),
            ("کلاس های تیزهوشان", ft.Icons.EMOJI_EVENTS, COLORS["indigo_600"], COLORS["indigo_100"], "شهریه کلاس های تیزهوشان"),
            ("آزمون ها", ft.Icons.ASSIGNMENT, COLORS["teal_600"], COLORS["teal_100"], "درآمد آزمون های مدرسه")
        ]
        
        option_rows = []
        for i in range(0, len(deposit_options), 2):
            row_options = deposit_options[i:i+2]
            row_cards = []
            
            for title, icon, color, bg_color, description in row_options:
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, t=title: (
                        show_tuition_grade() if t == "شهریه مدرسه" else
                        show_cafeteria_sales() if t == "بوفه" else
                        show_breakfast_sales() if t == "صبحانه" else
                        show_extra_class_grade() if t == "کلاس های تقویتی" else
                        show_gifted_class_grade() if t == "کلاس های تیزهوشان" else
                        show_exam_type_page() if t == "آزمون ها" else
                        show_alert(f"صفحه واریز {t} در حال توسعه است")
                    ),
                    content=ft.Row(
                        [
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                bgcolor=bg_color,
                                content=ft.Icon(
                                    name=icon,
                                    color=color,
                                    size=36
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        title,
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        description,
                                        size=14,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                row_cards.append(card)
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            option_rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=show_main
                                        ),
                                        create_icon(
                                            ft.Icons.ATTACH_MONEY,
                                            COLORS["green_600"],
                                            COLORS["green_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "انتخاب نوع واریز",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "نوع واریز را انتخاب کنید",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "از بین گزینه‌های زیر انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        option_rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    def create_tuition_grade_page():
        # گرفتن کلاس‌ها از API
        classrooms = get_classrooms()
        
        # گروه‌بندی کلاس‌ها بر اساس پایه
        grade_counts = {}
        for classroom in classrooms:
            grade = classroom.get('grade')  # استفاده از get برای جلوگیری از KeyError
            if grade:
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        # تبدیل شماره پایه به نام فارسی
        grade_names = {
            '1': 'اول',
            '2': 'دوم', 
            '3': 'سوم',
            '4': 'چهارم',
            '5': 'پنجم',
            '6': 'ششم'
        }
        
        # رنگ‌های مختلف برای هر پایه
        colors = [
            COLORS["red_600"], COLORS["orange_600"], COLORS["yellow_600"],
            COLORS["green_600"], COLORS["blue_600"], COLORS["purple_600"]
        ]
        bg_colors = [
            COLORS["red_100"], COLORS["orange_100"], COLORS["yellow_100"],
            COLORS["green_100"], COLORS["blue_100"], COLORS["purple_100"]
        ]
        
        # ایجاد لیست پایه‌ها
        grade_options = []
        for i, grade_num in enumerate(['1', '2', '3', '4', '5', '6']):
            if i < len(colors):
                grade_persian = grade_names[grade_num]
                class_count = grade_counts.get(grade_num, 0)
                grade_options.append(
                    (f"کلاس {grade_persian}", grade_num, colors[i], bg_colors[i], 
                    f"شهریه پایه {grade_persian} - {class_count} کلاس")
                )
        
        # ایجاد کارت‌های مستطیلی دو به دو
        option_rows = []
        for i in range(0, len(grade_options), 2):
            row_options = grade_options[i:i+2]
            row_cards = []
            
            for title, number, color, bg_color, description in row_options:
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, grade_num=number: (
                        show_class_selection(f"کلاس {grade_names[grade_num]}") if current_page == "tuition_grade" else
                        show_extra_class_selection(f"کلاس {grade_names[grade_num]}") if current_page == "extra_class_grade" else
                        None
                    ),
                    content=ft.Row(
                        [
                            create_number_circle(number, color, bg_color, 80),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        title,
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        description,
                                        size=14,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                row_cards.append(card)
            
            # اگر تعداد پایه‌ها فرد باشد، یک کارت خالی اضافه کن
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            option_rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=show_deposit_type
                                        ),
                                        create_icon(
                                            ft.Icons.HOME_WORK,
                                            COLORS["blue_600"],
                                            COLORS["blue_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "انتخاب پایه تحصیلی",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "شهریه مدرسه",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "پایه تحصیلی مورد نظر را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        option_rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    # صفحه انتخاب کلاس
    def create_class_selection_page():
        # گرفتن کلاس‌های real از API بر اساس پایه انتخاب شده
        grade_number = selected_grade.split(" ")[-1]  # تبدیل "کلاس اول" به "اول"
        grade_mapping = {"اول": "1", "دوم": "2", "سوم": "3", "چهارم": "4", "پنجم": "5", "ششم": "6"}
        grade_num = grade_mapping.get(grade_number, "1")

        if "تیزهوشان" in selected_grade:
            # اگر از تیزهوشان اومدی
            grade_number = selected_grade.split(" ")[1]  # "پنجم" از "پایه پنجم تیزهوشان"
            grade_mapping = {"سوم": "3", "چهارم": "4", "پنجم": "5", "ششم": "6"}
            grade_num = grade_mapping.get(grade_number, "5")
        else:
            # اگر از شهریه معمولی اومدی  
            grade_number = selected_grade.split(" ")[-1]  # "اول" از "کلاس اول"
            grade_mapping = {"اول": "1", "دوم": "2", "سوم": "3", "چهارم": "4", "پنجم": "5", "ششم": "6"}
            grade_num = grade_mapping.get(grade_number, "1")
        
        classrooms = get_classrooms(grade=grade_num)
        
        # ایجاد کارت‌های مستطیلی برای کلاس‌ها
        option_rows = []
        for i in range(0, len(classrooms), 2):
            row_classes = classrooms[i:i+2]
            row_cards = []
            
            for classroom in row_classes:
                # رنگ‌های مختلف برای کلاس‌ها
                colors = [
                    COLORS["red_600"], COLORS["orange_600"], COLORS["yellow_600"],
                    COLORS["green_600"], COLORS["blue_600"], COLORS["purple_600"],
                    COLORS["indigo_600"], COLORS["teal_600"], COLORS["pink_600"]
                ]
                bg_colors = [
                    COLORS["red_100"], COLORS["orange_100"], COLORS["yellow_100"],
                    COLORS["green_100"], COLORS["blue_100"], COLORS["purple_100"],
                    COLORS["indigo_100"], COLORS["teal_100"], COLORS["pink_100"]
                ]
                
                color_index = i % len(colors)
                color = colors[color_index]
                bg_color = bg_colors[color_index]
                
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, c=classroom: (
                        print(f"🎯 کلیک روی کلاس - current_page: {current_page}"),
                        show_student_list(c) if current_page == "class_selection" else
                        show_extra_class_student_list(c) if current_page == "extra_class_selection" else
                        (print("🚀 فراخوانی show_gifted_class_student_list"), show_gifted_class_student_list(c)) if current_page == "gifted_class_selection" else
                        None
                    ),
                    content=ft.Row(
                        [
                            create_number_circle(str(classroom['class_number']), color, bg_color, 80),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"کلاس {classroom['class_number']}",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        f"پایه {classroom['grade']} - معلم: {classroom.get('teacher_name', 'ندارد')}",
                                        size=14,
                                        color=COLORS["gray_600"]
                                    ),
                                    ft.Container(height=4),
                                    ft.Text(
                                        f"ظرفیت: {classroom['capacity']} دانش‌آموز",
                                        size=12,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                row_cards.append(card)
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            option_rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=lambda e: (
                                                show_tuition_grade() if current_page == "class_selection" else
                                                show_gifted_class_grade() if current_page == "gifted_class_selection" else
                                                show_deposit_type()
                                            )
                                        ),
                                        create_icon(
                                            ft.Icons.HOME_WORK,
                                            COLORS["indigo_600"],
                                            COLORS["indigo_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "انتخاب کلاس",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                f"شهریه {selected_grade}",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "کلاس مورد نظر را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        option_rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    # صفحه لیست دانش‌آموزان
    def create_student_list_page():
        if not selected_classroom:
            return ft.Container(
                content=ft.Text("خطا: کلاس انتخاب نشده است"),
                alignment=ft.alignment.center
            )
        
        # گرفتن دانش‌آموزان این کلاس از API
        students = get_students(classroom_id=selected_classroom['id'])
        
        # ایجاد کارت‌های دانش‌آموزان
        student_cards = []
        for i, student in enumerate(students, 1):
            card = ft.Container(
                width=280,
                height=200,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, s=student: (
                    print(f"🎯 کلیک روی دانش‌آموز - current_page: {current_page}"),
                    show_tuition_payment(s) if current_page == "student_list" else
                    show_extra_class_payment(s) if current_page == "extra_class_student_list" else
                    (print("🚀 فراخوانی show_gifted_class_payment"), show_gifted_class_payment(s)) if current_page == "gifted_class_student_list" else
                    None
                ),
                content=ft.Column(
                    [
                        ft.Container(
                            width=64,
                            height=64,
                            border_radius=32,
                            bgcolor=COLORS["blue_100"],
                            content=ft.Icon(
                                name=ft.Icons.PERSON,
                                color=COLORS["blue_600"],
                                size=32
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            f"{student['first_name']} {student['last_name']}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            f"کد ملی: {student['national_code']}",
                            size=12,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            f"کلاس: {selected_classroom['class_number']}",
                            size=12,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            student_cards.append(card)
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=lambda e: show_class_selection(selected_grade)
                                        ),
                                        create_icon(
                                            ft.Icons.PERSON,
                                            COLORS["green_600"],
                                            COLORS["green_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "لیست دانش آموزان",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                f"دانش آموزان کلاس {selected_classroom['class_number']}",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                f"تعداد دانش‌آموزان: {len(students)} نفر",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.GridView(
                                        student_cards,
                                        max_extent=280,
                                        child_aspect_ratio=0.8,
                                        spacing=24,
                                        run_spacing=24
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    # صفحه واریز شهریه
    def create_tuition_payment_page():
        if not current_student:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: دانش‌آموز انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_student_list_page())
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ شهریه (تومان)",
            hint_text="مثال: 2500000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["green_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            prefix_text="تومان ",
            keyboard_type=ft.KeyboardType.NUMBER
        )

        
        
        date_field = ft.TextField(
            label="تاریخ واریز",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["green_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        method_dropdown = ft.Dropdown(
            label="نوع پرداخت",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["green_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option(method['value'], method['label'])
                for method in get_payment_methods()
            ]
        )
        
        receipt_field = ft.TextField(
            label="شماره رسید/تراکنش",
            hint_text="شماره رسید یا تراکنش",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["green_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد واریز...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["green_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["green_50"],
            border=ft.border.all(1, COLORS["green_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["green_600"]),
                ft.Column([
                    ft.Text("واریز شهریه با موفقیت ثبت شد!", color=COLORS["green_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات واریز در سیستم ذخیره گردید.", color=COLORS["green_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_payment(e):
            # جمع‌آوری داده‌ها از فرم
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
    
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # جمع‌آوری داده‌ها از فرم
            payment_data = {
                'student': current_student['id'],
                'amount': int(amount_field.value.replace(',', '')) if amount_field.value else 0,
                'payment_date': gregorian_date,  # تاریخ میلادی
                'payment_method': method_dropdown.value,
                'receipt_number': receipt_field.value,
                'description': notes_field.value
            }
            
            # ارسال به API
            success, message = create_tuition_payment(payment_data)
            
            if success:
                success_banner.content.controls[1].controls[0].value = "واریز شهریه با موفقیت ثبت شد!"
                success_banner.content.controls[1].controls[1].value = message
                success_banner.visible = True
            else:
                # نمایش خطا
                show_alert(message)
            
            page.update()
        
        def clear_form(e):
            amount_field.value = ""
            date_field.value = datetime.now().strftime("%Y-%m-%d")
            method_dropdown.value = None
            receipt_field.value = ""
            notes_field.value = ""
            success_banner.visible = False
            page.update()

        # ایجاد صفحه کامل
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_student_list_page()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["green_100"],
                                    content=ft.Icon(ft.Icons.ATTACH_MONEY, color=COLORS["green_600"], size=24),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("واریز شهریه", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                # عنوان
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("واریز شهریه دانش آموز", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات دانش آموز و مبلغ واریزی را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات دانش‌آموز
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=["#f0f9ff", "#e0f2fe"]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["blue_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["blue_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_student['first_name']} {current_student['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_student['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                    
                                                    ft.Container(height=16),
                                                    
                                                    ft.Row([
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("کلاس", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_student.get('classroom_name', 'ندارد')}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                        
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("پایه تحصیلی", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_student.get('grade', 'ندارد')}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                        
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("وضعیت", size=12, color=COLORS["gray_500"]),
                                                                ft.Text("فعال", size=16, weight=ft.FontWeight.BOLD, color=COLORS["green_600"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                    ], spacing=12)
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم واریز
                                            ft.Column([
                                                # ردیف اول
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ شهریه (تومان)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ واریز", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # ردیف دوم
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("نوع پرداخت", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        method_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("شماره رسید/تراکنش", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        receipt_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["green_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت واریز شهریه", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_payment
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )

    # صفحه انتخاب نوع برداشت
    def create_withdraw_type_page():
        withdraw_options = [
            ("حقوق", ft.Icons.PERSON, COLORS["green_600"], COLORS["green_100"], "پرداخت حقوق کارکنان"),
            ("بیمه", ft.Icons.HEALTH_AND_SAFETY, COLORS["blue_600"], COLORS["blue_100"], "پرداخت بیمه کارکنان"),
            ("خرید", ft.Icons.SHOPPING_BAG, COLORS["purple_600"], COLORS["purple_100"], "خرید تجهیزات و لوازم"),
            ("کلاس های تقویتی", ft.Icons.SCHOOL, COLORS["indigo_600"], COLORS["indigo_100"], "هزینه کلاس های تقویتی"),
            ("کلاس های تیزهوشان", ft.Icons.EMOJI_EVENTS, COLORS["violet_600"], COLORS["violet_100"], "هزینه کلاس های تیزهوشان"),  # 🆕 این خط رو اضافه کن
            ("کرایه", ft.Icons.HOME_WORK, COLORS["yellow_600"], COLORS["yellow_100"], "کرایه ساختمان و اجاره"),
            ("قبض", ft.Icons.FLASH_ON, COLORS["cyan_600"], COLORS["cyan_100"], " قبوض آب، برق و گاز و تلفن ثابت و همراه و اینترنت"),
            ("تنخواه", ft.Icons.ACCOUNT_BALANCE_WALLET, COLORS["pink_600"], COLORS["pink_100"], "برداشت تنخواه گردان"),
            ("سرویس", ft.Icons.CAR_REPAIR, COLORS["orange_600"], COLORS["orange_100"], "هزینه سرویس و خدمات"), 
        ]
        
        option_rows = []
        for i in range(0, len(withdraw_options), 2):
            row_options = withdraw_options[i:i+2]
            row_cards = []
            
            for title, icon, color, bg_color, description in row_options:
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, t=title: (
                        show_purchase_page() if t == "خرید" else
                        show_rent_type_selection() if t == "کرایه" else
                        show_utility_type_selection() if t == "قبض" else
                        show_salary_position_selection() if t == "حقوق" else
                        show_insurance_page() if t == "بیمه" else
                        show_extra_class_withdraw_grade() if t == "کلاس های تقویتی" else
                        show_gifted_class_withdraw_grade() if t == "کلاس های تیزهوشان" else
                        show_petty_cash_page() if t == "تنخواه" else
                        show_service_page() if t == "سرویس" else
                        show_alert(f"صفحه برداشت {t} در حال توسعه است")
                    ),
                    content=ft.Row(
                        [
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                bgcolor=bg_color,
                                content=ft.Icon(
                                    name=icon,
                                    color=color,
                                    size=36
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        title,
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        description,
                                        size=14,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                row_cards.append(card)
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            option_rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=show_main
                                        ),
                                        create_icon(
                                            ft.Icons.ARROW_UPWARD,
                                            COLORS["red_600"],
                                            COLORS["red_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "انتخاب نوع برداشت",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "نوع برداشت را انتخاب کنید",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "از بین گزینه‌های زیر انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        option_rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )
    
    def create_cafeteria_sales_page():
        """صفحه ثبت فروش بوفه"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ فروش (تومان)",
            hint_text="مثال: 850000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ فروش",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد فروش بوفه...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        
        success_banner = ft.Container(
            bgcolor=COLORS["orange_50"],
            border=ft.border.all(1, COLORS["orange_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["orange_600"]),
                ft.Column([
                    ft.Text("فروش بوفه با موفقیت ثبت شد! 🎉", 
                        color=COLORS["orange_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات فروش در سیستم ذخیره گردید.", 
                        color=COLORS["orange_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False  # اول مخفی باشه
        )
        
        
        def submit_sale(e):
            """ثبت فروش بوفه"""
            # اعتبارسنجی
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # تبدیل تاریخ شمسی به میلادی
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی داده‌ها
            sale_data = {
                'amount': int(amount_field.value),
                'sale_date': gregorian_date,
                'description': notes_field.value,
                'type': 'buffet'  # نوع تراکنش
            }
            
            # ارسال به API
            success, message = create_cafeteria_sale(sale_data)
            
            if success:
                # ✅ درست مثل شهریه
                success_banner.content.controls[1].controls[0].value = "فروش بوفه با موفقیت ثبت شد! 🎉"
                success_banner.content.controls[1].controls[1].value = "جزئیات فروش در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
            else:
                show_alert(message)
            
            page.update()
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            notes_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_deposit_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["orange_100"],
                                    content=ft.Icon(
                                        ft.Icons.SHOPPING_CART, 
                                        color=COLORS["orange_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت فروش بوفه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                # عنوان
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت فروش روزانه بوفه", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("مبلغ فروش بوفه و تاریخ را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["orange_400"], COLORS["orange_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.SHOPPING_CART,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("فروش بوفه مدرسه", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("درآمد حاصل از فروش اقلام بوفه", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # ردیف اول - مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ فروش (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ فروش", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["orange_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت فروش بوفه", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_sale
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_breakfast_sales_page():
        """صفحه ثبت فروش صبحانه"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ صبحانه (تومان)",
            hint_text="مثال: 1200000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ فروش",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد فروش صبحانه...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["yellow_50"],
            border=ft.border.all(1, COLORS["yellow_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["yellow_600"]),
                ft.Column([
                    ft.Text("", color=COLORS["yellow_600"], weight=ft.FontWeight.BOLD),  # عنوان
                    ft.Text("", color=COLORS["yellow_600"], size=12),  # پیام
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_sale(e):
            """ثبت فروش صبحانه"""
            nonlocal success_banner

            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            sale_data = {
                'amount': int(amount_field.value),
                'sale_date': gregorian_date,
                'description': notes_field.value,
                'type': 'breakfast'
            }
            
            success, message = create_breakfast_sale(sale_data)
            
            if success:
                print("✅ موفقیت - آپدیت بنر")
                success_banner.content.controls[1].controls[0].value = "فروش صبحانه با موفقیت ثبت شد! 🌅"
                success_banner.content.controls[1].controls[1].value = "جزئیات فروش در سیستم ذخیره گردید."
                success_banner.visible = True
                print(f"🔍 وضعیت بنر بعد از تغییر: {success_banner.visible}")
                page.update()
            else:
                print("❌ خطا")
                show_alert(message)
            
            page.update()
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            notes_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_deposit_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["yellow_100"],
                                    content=ft.Icon(
                                        ft.Icons.WB_SUNNY, 
                                        color=COLORS["yellow_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت فروش صبحانه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت فروش روزانه صبحانه", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("مبلغ فروش صبحانه و تاریخ را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["yellow_400"], COLORS["yellow_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.WB_SUNNY,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("فروش صبحانه مدرسه", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("درآمد حاصل از فروش صبحانه", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ صبحانه (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ فروش", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["yellow_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت فروش صبحانه", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_sale
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_extra_class_payment_page():
        """صفحه ثبت پرداخت کلاس تقویتی - نسخه حرفه‌ای"""
        print("🎯 وارد تابع create_extra_class_payment_page شدیم")
        
        if not current_student:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: دانش‌آموز انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_extra_class_student_list(selected_classroom))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # فیلدهای فرم
        subject_dropdown = ft.Dropdown(
            label="درس مورد نظر *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("ریاضی", "ریاضی"),
                ft.dropdown.Option("علوم", "علوم"),
                ft.dropdown.Option("فارسی", "فارسی"),
            ]
        )
        
        amount_field = ft.TextField(
            label="مبلغ کلاس تقویتی (تومان) *",
            hint_text="مثال: 500000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت *",
            value=DateService.get_current_jalali(),  # ✅ استفاده از سرویس تاریخ
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد کلاس تقویتی...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["indigo_50"],
            border=ft.border.all(1, COLORS["indigo_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["indigo_600"]),
                ft.Column([
                    ft.Text("", color=COLORS["indigo_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("", color=COLORS["indigo_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_payment(e):
            """ثبت پرداخت کلاس تقویتی - نسخه حرفه‌ای"""
            nonlocal success_banner
        
            print("🎯 شروع ثبت پرداخت کلاس تقویتی...")
            
            # اعتبارسنجی فرم
            if not subject_dropdown.value:
                show_alert("لطفاً درس مورد نظر را انتخاب کنید")
                return
                    
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                    
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # اعتبارسنجی تاریخ با سرویس تاریخ
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # ✅ استفاده از سرویس تاریخ - بدون تبدیل (Backend هوشمند است)
            payment_data = {
                'student': current_student['id'],
                'amount': int(amount_field.value),
                'payment_date': date_field.value,  # ✅ تاریخ شمسی خام
                'subject': subject_dropdown.value,
                'description': notes_field.value,
                'type': 'extra_class'
            }
            
            print(f"🔍 داده‌های پرداخت: {payment_data}")
            
            # ارسال به API
            success, message = create_extra_class_payment(payment_data)
            
            if success:
                print("✅ پرداخت با موفقیت ثبت شد")
                success_banner.content.controls[1].controls[0].value = "پرداخت کلاس تقویتی با موفقیت ثبت شد! 📚"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                success_banner.visible = True
                
                # بازنشانی فرم
                subject_dropdown.value = None
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()
                notes_field.value = ""
                
                page.update()
                print("🔄 فرم بازنشانی شد")
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            nonlocal success_banner
            subject_dropdown.value = None
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            notes_field.value = ""
            success_banner.visible = False
            page.update()

        
            
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_extra_class_student_list(selected_classroom)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["indigo_100"],
                                    content=ft.Icon(ft.Icons.SCHOOL, color=COLORS["indigo_600"], size=24),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت کلاس تقویتی", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت کلاس تقویتی دانش آموز", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات کلاس تقویتی را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات دانش‌آموز
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=["#f0f9ff", "#e0f2fe"]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["indigo_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["indigo_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_student['first_name']} {current_student['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_student['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # درس و مبلغ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("درس مورد نظر", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        subject_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("مبلغ کلاس (تومان)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # تاریخ
                                                ft.Column([
                                                    ft.Text("تاریخ پرداخت", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    date_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["indigo_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت کلاس تقویتی", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_payment
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_gifted_class_grade_page():
        """صفحه انتخاب پایه برای تیزهوشان (پایه ۳, ۴, ۵ و ۶)"""
        
        # پایه‌های ۳, ۴, ۵ و ۶ برای تیزهوشان
        grade_options = [
            {
                "title": "پایه سوم تیزهوشان",
                "number": "3", 
                "color": COLORS["yellow_600"],
                "bg_color": COLORS["yellow_100"],
                "gradient_start": COLORS["yellow_400"],
                "gradient_end": COLORS["yellow_600"],
                "description": "کلاس تیزهوشان پایه سوم"
            },
            {
                "title": "پایه چهارم تیزهوشان", 
                "number": "4",
                "color": COLORS["green_600"],
                "bg_color": COLORS["green_100"],
                "gradient_start": COLORS["green_400"],
                "gradient_end": COLORS["green_600"],
                "description": "کلاس تیزهوشان پایه چهارم"
            },
            {
                "title": "پایه پنجم تیزهوشان",
                "number": "5", 
                "color": COLORS["purple_600"],
                "bg_color": COLORS["purple_100"],
                "gradient_start": COLORS["purple_400"],
                "gradient_end": COLORS["purple_600"],
                "description": "کلاس تیزهوشان پایه پنجم"
            },
            {
                "title": "پایه ششم تیزهوشان", 
                "number": "6",
                "color": COLORS["violet_600"],
                "bg_color": COLORS["violet_100"],
                "gradient_start": COLORS["violet_400"],
                "gradient_end": COLORS["violet_600"],
                "description": "کلاس تیزهوشان پایه ششم"
            }
        ]
        
        # ایجاد کارت‌های پایه
        grade_cards = []
        for grade in grade_options:
            card = ft.Container(
                width=280,
                height=220,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=32,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, g=grade: show_gifted_class_selection(g["title"]),
                content=ft.Column(
                    [
                        ft.Container(
                            width=80,
                            height=80,
                            border_radius=40,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[grade["gradient_start"], grade["gradient_end"]]
                            ),
                            content=ft.Text(
                                grade["number"],
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=COLORS["white"]
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            grade["title"],
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            grade["description"],
                            size=14,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            grade_cards.append(card)
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(grade_cards), 2):
            row_cards = grade_cards[i:i+2]
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=show_deposit_type
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["purple_100"],
                                    content=ft.Icon(
                                        ft.Icons.EMOJI_EVENTS,
                                        color=COLORS["purple_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("انتخاب پایه تیزهوشان", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("کلاس تیزهوشان", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("پایه تحصیلی مورد نظر را انتخاب کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    

    def create_gifted_class_payment_page():
        """صفحه ثبت پرداخت کلاس تیزهوشان"""
        print("🎯 وارد create_gifted_class_payment_page شدیم")
        
        if not current_student:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: دانش‌آموز انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_gifted_class_student_list(selected_classroom))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        
        # فیلدهای فرم
        subject_dropdown = ft.Dropdown(
            label="درس مورد نظر",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("ریاضی", "ریاضی"),
                ft.dropdown.Option("علوم", "علوم"),
                ft.dropdown.Option("فارسی", "فارسی"),
            ]
        )
        
        amount_field = ft.TextField(
            label="مبلغ کلاس تیزهوشان (تومان)",
            hint_text="مثال: 600000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت",
            value=DateService.get_current_jalali(),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد کلاس تیزهوشان...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["purple_50"],
            border=ft.border.all(1, COLORS["purple_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["purple_600"]),
                ft.Column([
                    ft.Text("متن عنوان", color=COLORS["purple_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("متن پیام", color=COLORS["purple_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_payment(e):
            """ثبت پرداخت کلاس تیزهوشان"""
            nonlocal success_banner

            if not subject_dropdown.value:
                show_alert("لطفاً درس مورد نظر را انتخاب کنید")
                return
                    
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                    
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            payment_data = {
                'student': current_student['id'],
                'amount': int(amount_field.value),
                'payment_date': date_field.value,
                'subject': subject_dropdown.value,
                'description': notes_field.value,
                'type': 'gifted_class'
            }
            
            print("📡 در حال ارسال به API...")
            success, message = create_gifted_class_payment(payment_data)
            print(f"🔍 نتیجه API: success={success}, message={message}")
            
            if success:
                print("✅ موفقیت - شروع آپدیت بنر")
                print(f"🔍 وضعیت بنر قبل: {success_banner.visible}")
                
                # آپدیت متن بنر
                success_banner.content.controls[1].controls[0].value = "پرداخت کلاس تیزهوشان با موفقیت ثبت شد! 🏆"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                
                # نمایش بنر
                success_banner.visible = True
                print(f"🔍 وضعیت بنر بعد: {success_banner.visible}")
                
                # آپدیت صفحه
                page.update()
                print("🔄 صفحه آپدیت شد")
                
                # ❌ این خط رو حذف کن یا کامنت کن:
                # clear_form(None)
                
                # ✅ به جای آن فقط فیلدها رو پاک کن (بدون مخفی کردن بنر):
                subject_dropdown.value = None
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()
                notes_field.value = ""
                print("🧹 فقط فیلدها پاک شدند (بنر نمایش داده میشه)")
                
            else:
                print("❌ خطا - نمایش آلرت")
                show_alert(message)
            
            page.update()
        
        def clear_form(e):
            """پاک کردن فرم"""
            nonlocal success_banner
            print("🧹 تابع clear_form فراخوانی شد")
            subject_dropdown.value = None
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            notes_field.value = ""
            success_banner.visible = False
            page.update()
            print(f"🔍 وضعیت بنر بعد از پاک کردن: {success_banner.visible}")

        # ایجاد صفحه اصلی
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_gifted_class_student_list(selected_classroom)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["purple_100"],
                                    content=ft.Icon(
                                        ft.Icons.EMOJI_EVENTS,
                                        color=COLORS["purple_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت کلاس تیزهوشان", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت کلاس تیزهوشان دانش آموز", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات کلاس تیزهوشان را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات دانش‌آموز
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=["#f0f9ff", "#e0f2fe"]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["purple_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["purple_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_student['first_name']} {current_student['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_student['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # درس و مبلغ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("درس مورد نظر", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        subject_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("مبلغ کلاس (تومان)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # تاریخ
                                                ft.Column([
                                                    ft.Text("تاریخ پرداخت", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    date_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["purple_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت کلاس تیزهوشان", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_payment
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
        
    def create_exam_type_page():
        """صفحه انتخاب نوع آزمون"""
        
        exam_options = [
            {
                "type": "تیزهوشان",
                "icon": ft.Icons.EMOJI_EVENTS,
                "color": COLORS["purple_600"],
                "bg_color": COLORS["purple_100"],
                "gradient_start": COLORS["purple_400"],
                "gradient_end": COLORS["purple_600"],
                "description": "آزمون تیزهوشان و استعداد تحلیلی",
                "key":"gifted",
            },
            {
                "type": "پیشرفته", 
                "icon": ft.Icons.TRENDING_UP,
                "color": COLORS["blue_600"],
                "bg_color": COLORS["blue_100"],
                "gradient_start": COLORS["blue_400"],
                "gradient_end": COLORS["blue_600"],
                "description": "آزمون پیشرفته درسی",
                "key":"advanced",
            },
            {
                "type": "تقویتی",
                "icon": ft.Icons.SCHOOL,
                "color": COLORS["green_600"], 
                "bg_color": COLORS["green_100"],
                "gradient_start": COLORS["green_400"],
                "gradient_end": COLORS["green_600"],
                "description": "آزمون تقویتی و رفع اشکال",
                "key":"remedial",
            },
            {
                "type": "کلاسی",
                "icon": ft.Icons.CLASS_,
                "color": COLORS["orange_600"],
                "bg_color": COLORS["orange_100"],
                "gradient_start": COLORS["orange_400"],
                "gradient_end": COLORS["orange_600"],
                "description": "آزمون کلاسی و تمرینی",
                "key":"classroom",
            },
            {
                "type": "آمادگی",
                "icon": ft.Icons.ASSIGNMENT,
                "color": COLORS["teal_600"],
                "bg_color": COLORS["teal_100"],
                "gradient_start": COLORS["teal_400"],
                "gradient_end": COLORS["teal_600"],
                "description": "آزمون آمادگی و شبیه‌سازی",
                "key":"preparation",
            },
            {
                "type": "پیش نیاز", 
                "icon": ft.Icons.PLAY_LESSON,
                "color": COLORS["indigo_600"],
                "bg_color": COLORS["indigo_100"],
                "gradient_start": COLORS["indigo_400"],
                "gradient_end": COLORS["indigo_600"],
                "description": "آزمون پیش‌نیاز و پایه",
                "key":"prerequisite",
            }
        ]
        
        # ایجاد کارت‌های آزمون
        exam_cards = []
        for i in range(0, len(exam_options), 2):
            row_exams = exam_options[i:i+2]
            row_cards = []
            
            for exam in row_exams:
                card = ft.Container(
                    expand=True,
                    height=200,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, exam_key=exam["key"]: show_exam_grade_selection(exam_key),
                    content=ft.Column(
                        [
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.bottom_right,
                                    colors=[exam["gradient_start"], exam["gradient_end"]]
                                ),
                                content=ft.Icon(
                                    name=exam["icon"],
                                    color=COLORS["white"],
                                    size=36
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                exam["type"],
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=COLORS["gray_900"],
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                exam["description"],
                                size=14,
                                color=COLORS["gray_600"],
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    )
                )
                row_cards.append(card)
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=200))
            
            exam_cards.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=lambda e: show_deposit_type()  # به صفحه واریز برمی‌گرده
                                        ),
                                        ft.Container(
                                            width=40,
                                            height=40,
                                            border_radius=20,
                                            bgcolor=COLORS["teal_100"],
                                            content=ft.Icon(
                                                ft.Icons.ASSIGNMENT,
                                                color=COLORS["teal_600"],
                                                size=24
                                            ),
                                            alignment=ft.alignment.center
                                        ),
                                        ft.Text(
                                            "انتخاب نوع آزمون",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "انتخاب نوع آزمون",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "نوع آزمون مورد نظر را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        exam_cards,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    # تابع navigation جدید
    def show_exam_type_page(e=None):
        """نمایش صفحه انتخاب نوع آزمون"""
        nonlocal current_page
        current_page = "exam_type"
        update_display()


    def create_exam_grade_selection_page(exam_type):
        """صفحه انتخاب پایه برای آزمون"""
        
        # پایه‌های مجاز برای هر آزمون
        exam_grades = {
            'gifted': ['3','4','5', '6'],  # تیزهوشان فقط پایه ۵ و ۶
            'advanced': ['1', '2', '3', '4', '5', '6'],  # بقیه آزمون‌ها همه پایه‌ها
            'remedial': ['1', '2', '3', '4', '5', '6'],
            'classroom': ['1', '2', '3', '4', '5', '6'], 
            'preparation': ['1', '2', '3', '4', '5', '6'],
            'prerequisite': ['1', '2', '3', '4', '5', '6']
        }
        
        # نام فارسی آزمون‌ها
        exam_names = {
            'gifted': 'تیزهوشان',
            'advanced': 'پیشرفته',
            'remedial': 'تقویتی', 
            'classroom': 'کلاسی',
            'preparation': 'آمادگی',
            'prerequisite': 'پیش نیاز'
        }
        
        grades = exam_grades.get(exam_type, ['1', '2', '3', '4', '5', '6'])
        
        # نام فارسی پایه‌ها
        grade_names = {
            '1': 'اول',
            '2': 'دوم', 
            '3': 'سوم',
            '4': 'چهارم',
            '5': 'پنجم',
            '6': 'ششم'
        }
        
        # رنگ‌های مختلف برای هر پایه
        colors = [
            COLORS["red_600"], COLORS["orange_600"], COLORS["yellow_600"],
            COLORS["green_600"], COLORS["blue_600"], COLORS["purple_600"]
        ]
        bg_colors = [
            COLORS["red_100"], COLORS["orange_100"], COLORS["yellow_100"],
            COLORS["green_100"], COLORS["blue_100"], COLORS["purple_100"]
        ]
        
        # ایجاد کارت‌های پایه
        grade_cards = []
        for i, grade_num in enumerate(grades):
            if i < len(colors):
                grade_persian = grade_names[grade_num]
                
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, g=grade_num: show_exam_class_selection(exam_type, g),
                    content=ft.Row(
                        [
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                bgcolor=bg_colors[i],
                                content=ft.Text(
                                    grade_num,
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors[i]
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"پایه {grade_persian}",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        f"آزمون {exam_names.get(exam_type, exam_type)}",
                                        size=14,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                grade_cards.append(card)
        
        # ایجاد ردیف‌ها
        rows = []
        for i in range(0, len(grade_cards), 2):
            row_cards = grade_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=lambda e: show_exam_type_page()
                                        ),
                                        ft.Container(
                                            width=40,
                                            height=40,
                                            border_radius=20,
                                            bgcolor=COLORS["teal_100"],
                                            content=ft.Icon(
                                                ft.Icons.ASSIGNMENT,
                                                color=COLORS["teal_600"],
                                                size=24
                                            ),
                                            alignment=ft.alignment.center
                                        ),
                                        ft.Text(
                                            f"انتخاب پایه - {exam_names.get(exam_type, exam_type)}",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                f"آزمون {exam_names.get(exam_type, exam_type)}",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "پایه تحصیلی مورد نظر را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )
    
    def create_exam_class_selection_page(exam_type, grade):
        """صفحه انتخاب کلاس برای آزمون - با تم رنگی پویا"""
        
        # گرفتن کلاس‌های این پایه از API
        classrooms = get_classrooms(grade=grade)
        
        # نام فارسی آزمون‌ها
        exam_names = {
            'gifted': 'تیزهوشان',
            'advanced': 'پیشرفته',
            'remedial': 'تقویتی', 
            'classroom': 'کلاسی',
            'preparation': 'آمادگی',
            'prerequisite': 'پیش نیاز'
        }
        
        # نام فارسی پایه‌ها
        grade_names = {
            '1': 'اول', '2': 'دوم', '3': 'سوم',
            '4': 'چهارم', '5': 'پنجم', '6': 'ششم'
        }
        
        # رنگ‌های مختلف برای هر پایه
        grade_colors = {
            '1': (COLORS["red_400"], COLORS["red_600"], COLORS["red_100"]),      # پایه اول: قرمز
            '2': (COLORS["orange_400"], COLORS["orange_600"], COLORS["orange_100"]), # پایه دوم: نارنجی
            '3': (COLORS["yellow_400"], COLORS["yellow_600"], COLORS["yellow_100"]), # پایه سوم: زرد
            '4': (COLORS["green_400"], COLORS["green_600"], COLORS["green_100"]),    # پایه چهارم: سبز
            '5': (COLORS["blue_400"], COLORS["blue_600"], COLORS["blue_100"]),       # پایه پنجم: آبی
            '6': (COLORS["purple_400"], COLORS["purple_600"], COLORS["purple_100"])  # پایه ششم: بنفش
        }
        
        # گرفتن رنگ‌های مربوط به این پایه
        color_400, color_600, color_100 = grade_colors.get(grade, (COLORS["indigo_400"], COLORS["indigo_600"], COLORS["indigo_100"]))
        
        # ایجاد کارت‌های کلاس با تم رنگی پایه
        classroom_cards = []
        for classroom in classrooms:
            card = ft.Container(
                width=280,
                height=240,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=32,
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, c=classroom: show_exam_student_list(exam_type, grade, c),
                content=ft.Column(
                    [
                        ft.Container(
                            width=80,
                            height=80,
                            border_radius=40,
                            bgcolor=color_100,  # رنگ پایه
                            content=ft.Text(
                                str(classroom['class_number']),
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=color_600  # رنگ پایه
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            f"کلاس {classroom['class_number']}",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            f"معلم: {classroom.get('teacher_name', 'ندارد')}",
                            size=14,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            f"ظرفیت: {classroom['capacity']} دانش‌آموز",
                            size=12,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            classroom_cards.append(card)
        
        # اگر کلاسی نبود
        if not classroom_cards:
            classroom_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.CLASS_, size=48, color=COLORS["gray_400"]),
                        ft.Text("کلاسی یافت نشد", size=16, color=COLORS["gray_600"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(classroom_cards), 2):
            row_cards = classroom_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=280, height=180))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_exam_grade_selection(exam_type)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=color_100,  # رنگ پایه در هدر
                                    content=ft.Icon(
                                        ft.Icons.ASSIGNMENT,
                                        color=color_600,  # رنگ پایه در هدر
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(
                                    f"انتخاب کلاس - {exam_names.get(exam_type, exam_type)}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"]
                                )
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            f"آزمون {exam_names.get(exam_type, exam_type)}", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"پایه {grade_names.get(grade, grade)} - انتخاب کلاس", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"تعداد کلاس‌ها: {len(classrooms)}", 
                                            size=16, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                                ),
                                
                                ft.Container(height=48),
                                
                                # لیست کلاس‌ها
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    

    def create_exam_student_list_page(exam_type, grade, classroom):
        """صفحه لیست دانش‌آموزان برای ثبت‌نام آزمون"""
        
        # گرفتن دانش‌آموزان این کلاس از API
        students = get_students(classroom_id=classroom['id'])
        
        # نام فارسی آزمون‌ها
        exam_names = {
            'gifted': 'تیزهوشان',
            'advanced': 'پیشرفته',
            'remedial': 'تقویتی', 
            'classroom': 'کلاسی',
            'preparation': 'آمادگی',
            'prerequisite': 'پیش نیاز'
        }
        
        # نام فارسی پایه‌ها
        grade_names = {
            '1': 'اول', '2': 'دوم', '3': 'سوم',
            '4': 'چهارم', '5': 'پنجم', '6': 'ششم'
        }
        
        # ایجاد کارت‌های دانش‌آموزان
        student_cards = []
        for student in students:
            card = ft.Container(
                width=300,
                height=230,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, s=student: show_exam_payment_page(exam_type, s),
                content=ft.Column(
                    [
                        ft.Container(
                            width=64,
                            height=64,
                            border_radius=32,
                            bgcolor=COLORS["blue_100"],
                            content=ft.Icon(
                                name=ft.Icons.PERSON,
                                color=COLORS["blue_600"],
                                size=32
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            f"{student['first_name']} {student['last_name']}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            f"کد ملی: {student['national_code']}",
                            size=12,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            student_cards.append(card)
        
        # اگر دانش‌آموزی نبود
        if not student_cards:
            student_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF, size=48, color=COLORS["gray_400"]),
                        ft.Text("دانش‌آموزی یافت نشد", size=16, color=COLORS["gray_600"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۳ تایی با Row و Column
        rows = []
        for i in range(0, len(student_cards), 3):
            row_cards = student_cards[i:i+3]
            
            # مطمئن شو هر ردیف دقیقاً ۳ تا کارت داره
            while len(row_cards) < 3:
                row_cards.append(ft.Container(width=300, height=180))  # کارت خالی
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=8)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_exam_class_selection(exam_type, grade)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["teal_100"],
                                    content=ft.Icon(
                                        ft.Icons.ASSIGNMENT,
                                        color=COLORS["teal_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(
                                    f"لیست دانش‌آموزان - {exam_names.get(exam_type, exam_type)}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"]
                                )
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            f"دانش‌آموزان کلاس {classroom['class_number']}", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"آزمون {exam_names.get(exam_type, exam_type)} - پایه {grade_names.get(grade, grade)}", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"تعداد: {len(students)} نفر", 
                                            size=16, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                                ),
                                
                                ft.Container(height=48),
                                
                                # لیست دانش‌آموزان (۳ تایی قطعی)
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=1000,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_exam_payment_page():
        """صفحه ثبت پرداخت آزمون"""
        
        if not current_student:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: دانش‌آموز انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_exam_student_list(selected_exam_type, selected_grade, selected_classroom))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # نام فارسی آزمون‌ها
        exam_names = {
            'gifted': 'تیزهوشان',
            'advanced': 'پیشرفته',
            'remedial': 'تقویتی', 
            'classroom': 'کلاسی',
            'preparation': 'آمادگی',
            'prerequisite': 'پیش نیاز'
        }
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ آزمون (تومان) *",
            hint_text="مثال: 250000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["teal_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت *",
            value=DateService.get_current_jalali(),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["teal_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        payment_method_dropdown = ft.Dropdown(
            label="نوع پرداخت *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["teal_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option(method['value'], method['label'])
                for method in get_payment_methods()
            ]
        )
        
        receipt_field = ft.TextField(
            label="شماره رسید/تراکنش",
            hint_text="شماره رسید یا تراکنش بانکی",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["teal_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        description_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات مربوط به آزمون...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["teal_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        # Success Banner
        success_banner = ft.Container(
            bgcolor=COLORS["teal_50"],
            border=ft.border.all(1, COLORS["teal_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["teal_600"]),
                ft.Column([
                    ft.Text("", color=COLORS["teal_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("", color=COLORS["teal_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_exam_payment(e):
            """ثبت پرداخت آزمون"""
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
                
            if not payment_method_dropdown.value:
                show_alert("لطفاً نوع پرداخت را انتخاب کنید")
                return
            
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return

            payment_data = {
                'student': current_student['id'],  # ID دانش‌آموز انتخاب شده
                'amount': int(amount_field.value),
                'payment_date': date_field.value, 
                'payment_method': payment_method_dropdown.value,
                'exam_type': selected_exam_type,   # نوع آزمون (تیزهوشان، پیشرفته، ...)
                'receipt_number': receipt_field.value,
                'description': description_field.value
            }
            
            success, message = create_exam_payment(payment_data)
    
            if success:
                success_banner.content.controls[1].controls[0].value = "پرداخت آزمون با موفقیت ثبت شد! 📝"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن (بنر رو مخفی نکن)
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()
                payment_method_dropdown.value = None
                receipt_field.value = ""
                description_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            payment_method_dropdown.value = None
            receipt_field.value = ""
            description_field.value = ""
            success_banner.visible = False
            page.update()

        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_exam_student_list(selected_exam_type, selected_grade, selected_classroom)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["teal_100"],
                                    content=ft.Icon(
                                        ft.Icons.ASSIGNMENT,
                                        color=COLORS["teal_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(
                                    f"ثبت آزمون {exam_names.get(selected_exam_type, selected_exam_type)}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"]
                                )
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت پرداخت آزمون", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات پرداخت آزمون را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات دانش‌آموز
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=[COLORS["teal_50"], COLORS["teal_100"]]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["teal_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["teal_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_student['first_name']} {current_student['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_student['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                    
                                                    ft.Container(height=16),
                                                    
                                                    ft.Row([
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("کلاس", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_student.get('classroom_name', 'ندارد')}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                        
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("نوع آزمون", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{exam_names.get(selected_exam_type, selected_exam_type)}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                    ], spacing=12)
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم پرداخت
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ آزمون (تومان) *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # نوع پرداخت و شماره رسید
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("نوع پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        payment_method_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("شماره رسید/تراکنش", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        receipt_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    description_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["teal_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت پرداخت آزمون", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_exam_payment
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_purchase_page():
        """صفحه ثبت خرید"""
        
        # فیلدهای فرم
        item_title_field = ft.TextField(
            label="عنوان جنس خریداری شده",
            hint_text="مثال: لپ تاپ ایسوس، کتاب ریاضی، لوازم التحریر",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        amount_field = ft.TextField(
            label="مبلغ خرید (تومان)",
            hint_text="مثال: 2500000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ خرید",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد خرید، مشخصات کالا، گارانتی و...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["purple_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["purple_50"],
            border=ft.border.all(1, COLORS["purple_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["purple_600"]),
                ft.Column([
                    ft.Text("خرید با موفقیت ثبت شد! 🛍️", 
                        color=COLORS["purple_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات خرید در سیستم ذخیره گردید.", 
                        color=COLORS["purple_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_purchase(e):
            nonlocal success_banner
            
            print("🎯 شروع ثبت خرید...")
            
            # اعتبارسنجی فیلدها
            if not item_title_field.value:
                show_alert("لطفاً عنوان جنس را وارد کنید")
                return
                
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # تبدیل تاریخ
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی purchase_data
            purchase_data = {
                'item_title': item_title_field.value,
                'amount': int(amount_field.value),
                'purchase_date': gregorian_date,
                'description': notes_field.value
            }
            
            print(f"🔍 purchase_data: {purchase_data}")
            
            # فراخوانی API
            success, message = create_purchase(purchase_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "خرید با موفقیت ثبت شد! 🛍️"
                success_banner.content.controls[1].controls[1].value = "جزئیات خرید در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                item_title_field.value = ""
                amount_field.value = ""
                date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
                notes_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            item_title_field.value = ""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            notes_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["purple_100"],
                                    content=ft.Icon(
                                        ft.Icons.SHOPPING_BAG, 
                                        color=COLORS["purple_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت خرید", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت خرید جدید", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات خرید را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["purple_400"], COLORS["purple_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.SHOPPING_BAG,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("ثبت خرید", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("خرید تجهیزات و لوازم", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # عنوان جنس و مبلغ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("عنوان جنس خریداری شده", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        item_title_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("مبلغ خرید (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # تاریخ
                                                ft.Column([
                                                    ft.Text("تاریخ خرید", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    date_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["purple_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت خرید", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_purchase
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_rent_page():
        """صفحه ثبت کرایه"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ کرایه (تومان)",
            hint_text="مثال: 15000000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        # Dropdown برای انتخاب ماه
        month_dropdown = ft.Dropdown(
            label="ماه مربوطه",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("فروردین", "فروردین"),
                ft.dropdown.Option("اردیبهشت", "اردیبهشت"),
                ft.dropdown.Option("خرداد", "خرداد"),
                ft.dropdown.Option("تیر", "تیر"),
                ft.dropdown.Option("مرداد", "مرداد"),
                ft.dropdown.Option("شهریور", "شهریور"),
                ft.dropdown.Option("مهر", "مهر"),
                ft.dropdown.Option("آبان", "آبان"),
                ft.dropdown.Option("آذر", "آذر"),
                ft.dropdown.Option("دی", "دی"),
                ft.dropdown.Option("بهمن", "بهمن"),
                ft.dropdown.Option("اسفند", "اسفند"),
            ]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد کرایه، آدرس ملک و...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["yellow_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["yellow_50"],
            border=ft.border.all(1, COLORS["yellow_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["yellow_600"]),
                ft.Column([
                    ft.Text("کرایه با موفقیت ثبت شد! 🏠", 
                        color=COLORS["yellow_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات پرداخت کرایه در سیستم ذخیره گردید.", 
                        color=COLORS["yellow_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_rent(e):
            """ثبت کرایه"""
            nonlocal success_banner
            
            print("🎯 شروع ثبت کرایه...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not month_dropdown.value:
                show_alert("لطفاً ماه مربوطه را انتخاب کنید")
                return
            
            # آماده‌سازی rent_data
            rent_data = {
                'amount': int(amount_field.value),
                'month': month_dropdown.value,
                'description': notes_field.value
            }
            
            print(f"🔍 rent_data: {rent_data}")
            
            # فراخوانی API
            success, message = create_rent(rent_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "کرایه با موفقیت ثبت شد! 🏠"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                month_dropdown.value = None
                notes_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            month_dropdown.value = None
            notes_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_rent_type_selection()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["yellow_100"],
                                    content=ft.Icon(
                                        ft.Icons.HOME_WORK, 
                                        color=COLORS["yellow_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت کرایه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت کرایه", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات پرداخت کرایه را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["yellow_400"], COLORS["yellow_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.HOME_WORK,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("کرایه ساختمان", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("کرایه ساختمان و اجاره", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و ماه
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ کرایه (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("ماه مربوطه", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        month_dropdown
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["yellow_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت کرایه", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_rent
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def show_utility_type_selection(e=None):
        nonlocal current_page
        current_page = "utility_type_selection"
        update_display()
    
    def create_utility_type_selection_page():
        """صفحه انتخاب نوع قبض"""
        
        utility_options = [
            {
                "type": "آب",
                "title": "قبض آب",
                "icon": ft.Icons.WATER_DROP,
                "color": COLORS["blue_600"],
                "bg_color": COLORS["blue_100"],
                "gradient_start": COLORS["blue_400"],
                "gradient_end": COLORS["blue_600"],
                "description": "پرداخت قبض آب"
            },
            {
                "type": "برق", 
                "title": "قبض برق",
                "icon": ft.Icons.FLASH_ON,
                "color": COLORS["yellow_600"],
                "bg_color": COLORS["yellow_100"],
                "gradient_start": COLORS["yellow_400"],
                "gradient_end": COLORS["yellow_600"],
                "description": "پرداخت قبض برق"
            },
            {
                "type": "گاز",
                "title": "قبض گاز", 
                "icon": ft.Icons.LOCAL_FIRE_DEPARTMENT,
                "color": COLORS["orange_600"],
                "bg_color": COLORS["orange_100"],
                "gradient_start": COLORS["orange_400"],
                "gradient_end": COLORS["orange_600"],
                "description": "پرداخت قبض گاز"
            },
            # اضافه کردن موارد جدید
            {
                "type": "تلفن همراه",
                "title": "قبض تلفن همراه", 
                "icon": ft.Icons.PHONE_ANDROID,
                "color": COLORS["green_600"],
                "bg_color": COLORS["green_100"],
                "gradient_start": COLORS["green_400"],
                "gradient_end": COLORS["green_600"],
                "description": "پرداخت قبض تلفن همراه"
            },
            {
                "type": "تلفن ثابت",
                "title": "قبض تلفن ثابت", 
                "icon": ft.Icons.PHONE,
                "color": COLORS["purple_600"],
                "bg_color": COLORS["purple_100"],
                "gradient_start": COLORS["purple_400"],
                "gradient_end": COLORS["purple_600"],
                "description": "پرداخت قبض تلفن ثابت"
            },
            {
                "type": "اینترنت",
                "title": "قبض اینترنت", 
                "icon": ft.Icons.WIFI,
                "color": COLORS["indigo_600"],
                "bg_color": COLORS["indigo_100"],
                "gradient_start": COLORS["indigo_400"],
                "gradient_end": COLORS["indigo_600"],
                "description": "پرداخت قبض اینترنت"
            }
        ]
        
        option_cards = []
        for utility in utility_options:
            card = ft.Container(
                width=280,
                height=300,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=32,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, u=utility: select_utility_type(u),
                content=ft.Column(
                    [
                        ft.Container(
                            width=80,
                            height=80,
                            border_radius=40,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[utility["gradient_start"], utility["gradient_end"]]
                            ),
                            content=ft.Icon(
                                utility["icon"],
                                color=COLORS["white"],
                                size=40
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=24),
                        ft.Text(
                            utility["title"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            utility["description"],
                            size=14,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=24),
                        ft.Container(
                            bgcolor=utility["bg_color"],
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=8,
                            content=ft.Text(
                                "انتخاب کنید",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=utility["color"]
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            option_cards.append(card)
        
        # ایجاد ردیف‌های ۳ تایی
        rows = []
        for i in range(0, len(option_cards), 3):
            row_cards = option_cards[i:i+3]
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["cyan_100"],
                                    content=ft.Icon(
                                        ft.Icons.FLASH_ON,
                                        color=COLORS["cyan_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("انتخاب نوع قبض", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("نوع قبض را انتخاب کنید", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("آب، برق، گاز، تلفن و اینترنت", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=1000,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def select_utility_type(utility):
        """انتخاب نوع قبض و رفتن به صفحه ثبت"""
        nonlocal selected_utility_type  
        selected_utility_type = utility
        
        show_utility_bill_page()

    def show_utility_bill_page(e=None):
        nonlocal current_page
        current_page = "utility_bill"
        update_display()
    
    def create_utility_bill_page():
        """صفحه ثبت قبض با تم پویا"""
        
        if not selected_utility_type:
            return ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
                ),
                expand=True,
                content=ft.Column([
                    ft.Container(height=200),
                    ft.Container(
                        width=600,
                        bgcolor=COLORS["white"],
                        border_radius=16,
                        padding=32,
                        content=ft.Column([
                            ft.Icon(ft.Icons.ERROR, color=COLORS["red_600"], size=64),
                            ft.Text("خطا در بارگذاری صفحه", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("لطفاً ابتدا نوع قبض را انتخاب کنید", size=16, color=COLORS["gray_600"]),
                            ft.Container(height=24),
                            ft.ElevatedButton(
                                "بازگشت به صفحه انتخاب",
                                on_click=lambda e: show_utility_type_selection()
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        
        # رنگ‌های متناسب با نوع قبض
        utility_colors = {
            "آب": {
                "color": COLORS["blue_600"],
                "bg_color": COLORS["blue_100"],
                "gradient_start": COLORS["blue_400"],
                "gradient_end": COLORS["blue_600"],
                "icon": ft.Icons.WATER_DROP
            },
            "برق": {
                "color": COLORS["yellow_600"],
                "bg_color": COLORS["yellow_100"], 
                "gradient_start": COLORS["yellow_400"],
                "gradient_end": COLORS["yellow_600"],
                "icon": ft.Icons.FLASH_ON
            },
            "گاز": {
                "color": COLORS["orange_600"],
                "bg_color": COLORS["orange_100"],
                "gradient_start": COLORS["orange_400"],
                "gradient_end": COLORS["orange_600"],
                "icon": ft.Icons.LOCAL_FIRE_DEPARTMENT
            },
            "تلفن همراه": {
                "color": COLORS["green_600"],
                "bg_color": COLORS["green_100"],
                "gradient_start": COLORS["green_400"],
                "gradient_end": COLORS["green_600"],
                "icon": ft.Icons.PHONE_ANDROID
            },
            "تلفن ثابت": {
                "color": COLORS["purple_600"],
                "bg_color": COLORS["purple_100"],
                "gradient_start": COLORS["purple_400"],
                "gradient_end": COLORS["purple_600"],
                "icon": ft.Icons.PHONE
            },
            "اینترنت": {
                "color": COLORS["indigo_600"],
                "bg_color": COLORS["indigo_100"],
                "gradient_start": COLORS["indigo_400"],
                "gradient_end": COLORS["indigo_600"],
                "icon": ft.Icons.WIFI
            }
        }
        
        colors = utility_colors[selected_utility_type["type"]]
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ قبض (تومان)",
            hint_text="مثال: 450000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=colors["color"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=colors["color"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        # فیلد شماره قبض برای همه انواع قبض
        bill_number_field = ft.TextField(
            label="شماره قبض (اختیاری)",
            hint_text="شماره قبض در صورت موجودی",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=colors["color"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد قبض...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=colors["color"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=colors["bg_color"],
            border=ft.border.all(1, colors["color"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=colors["color"]),
                ft.Column([
                    ft.Text("قبض با موفقیت ثبت شد! ⚡", 
                        color=colors["color"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات قبض در سیستم ذخیره گردید.", 
                        color=colors["color"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_bill(e):
            """ثبت قبض"""
            nonlocal success_banner
    
            print("🎯 شروع ثبت قبض...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # تبدیل تاریخ
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی bill_data
            bill_data = {
                'amount': int(amount_field.value),
                'bill_date': gregorian_date,
                'utility_type': selected_utility_type['type'],
                'description': notes_field.value,
                'bill_number': bill_number_field.value
            }
            
            print(f"🔍 bill_data: {bill_data}")
            
            # فراخوانی API
            success, message = create_utility_bill(bill_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = f"قبض {selected_utility_type['type']} با موفقیت ثبت شد! ⚡"
                success_banner.content.controls[1].controls[1].value = "جزئیات قبض در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
                bill_number_field.value = ""
                notes_field.value = ""
            else:
                show_alert(message)
            
            page.update()
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            bill_number_field.value = ""
            notes_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_utility_type_selection()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=colors["bg_color"],
                                    content=ft.Icon(
                                        colors["icon"],
                                        color=colors["color"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(f"ثبت قبض {selected_utility_type['type']}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت قبض", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات قبض را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[colors["gradient_start"], colors["gradient_end"]]
                                                        ),
                                                        content=ft.Icon(
                                                            colors["icon"],
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text(f"قبض {selected_utility_type['type']}", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text(selected_utility_type["description"], 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ قبض (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ پرداخت", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # شماره قبض برای همه
                                                ft.Column([
                                                    ft.Text("شماره قبض (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    bill_number_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=colors["color"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت قبض", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_bill
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_salary_position_selection_page():
        """صفحه انتخاب سمت برای حقوق - چیدمان ۲ در ۲"""
        
        # سمت‌های اصلی
        main_positions = [
            {'key': 'managers', 'name': 'مدیران', 'icon': ft.Icons.SUPERVISOR_ACCOUNT, 'color': (COLORS["red_400"], COLORS["red_600"])},
            {'key': 'assistants', 'name': 'معاونان', 'icon': ft.Icons.GROUP, 'color': (COLORS["blue_400"], COLORS["blue_600"])},
            {'key': 'teachers', 'name': 'معلم‌ها', 'icon': ft.Icons.SCHOOL, 'color': (COLORS["purple_400"], COLORS["purple_600"])},
            {'key': 'coaches', 'name': 'مربی‌ها', 'icon': ft.Icons.SPORTS_KABADDI, 'color': (COLORS["purple_500"], COLORS["purple_700"])},
            {'key': 'counselors', 'name': 'مشاوران', 'icon': ft.Icons.PSYCHOLOGY, 'color': (COLORS["teal_400"], COLORS["teal_600"])},
            {'key': 'services', 'name': 'خدمتگزاران', 'icon': ft.Icons.CLEANING_SERVICES, 'color': (COLORS["yellow_400"], COLORS["yellow_600"])}
        ]
        
        # ایجاد کارت‌های سمت اصلی
        position_cards = []
        for position in main_positions:
            card = ft.Container(
                width=320,
                height=160,  # ارتفاع کمتر
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=20,  # padding کمتر
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, pos=position['key']: show_salary_employee_list(pos),
                content=ft.Column(
                    [
                        ft.Container(
                            width=56,  # سایز کمتر
                            height=56,
                            border_radius=28,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[position['color'][0], position['color'][1]]
                            ),
                            content=ft.Icon(
                                name=position['icon'],
                                color=COLORS["white"],
                                size=24  # آیکون کوچکتر
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=8),  # فاصله کمتر
                        ft.Text(
                            position['name'],
                            size=18,  # فونت کوچکتر
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            position_cards.append(card)
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(position_cards), 2):
            row_cards = position_cards[i:i+2]
            
            # اگر ردیف آخر فقط ۱ کارت داشت، یه کارت خالی اضافه کن
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=280, height=140))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=8)
                )
            )
        
        # محتوای اصلی
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=64,
                                    height=64,
                                    border_radius=32,
                                    bgcolor=COLORS["green_100"],
                                    content=ft.Icon(ft.Icons.ATTACH_MONEY, color=COLORS["green_600"], size=24),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("انتخاب سمت برای حقوق", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=32,  # padding کمتر
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("سمت کارکنان را انتخاب کنید", size=32, weight=ft.FontWeight.BOLD, color=COLORS["white"], text_align=ft.TextAlign.CENTER),
                                        ft.Text("حقوق کارکنان - انتخاب سمت", size=18, color=COLORS["blue_100"], text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # ردیف‌های ۲ در ۲
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=8,
                                    ),
                                    width=600,  # عرض کمتر برای ۲ در ۲
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_salary_employee_list_page(category):
        """صفحه لیست کارکنان یک دسته سمت خاص"""
        
        # گرفتن کارکنان این دسته
        employees = get_employees_by_category(category)
        
        # نام فارسی دسته
        category_names = {
            'managers': 'مدیران',
            'assistants': 'معاونان', 
            'teachers': 'معلم‌ها',
            'coaches': 'مربی‌ها',
            'counselors': 'مشاوران',
            'services': 'خدمتگزاران'
        }
        
        # ایجاد کارت‌های کارکنان (بزرگ)
        employee_cards = []
        for employee in employees:
            card = ft.Container(
                width=280,  # 🔼 بزرگ
                height=200, # 🔼 بزرگ 
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, emp=employee: show_salary_payment_page(emp),
                content=ft.Column([
                    ft.Container(
                        width=80,  # 🔼 بزرگ
                        height=80, # 🔼 بزرگ
                        border_radius=40,
                        bgcolor=COLORS["blue_100"],
                        content=ft.Icon(ft.Icons.PERSON, color=COLORS["blue_600"], size=36),  # 🔼 بزرگ
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        f"{employee['first_name']} {employee['last_name']}", 
                        size=18,  # 🔼 بزرگ
                        weight=ft.FontWeight.BOLD, 
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        f"{employee.get('position_display', employee['position'])}",
                        size=14,  # 🔼 بزرگ
                        color=COLORS["gray_600"],
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            employee_cards.append(card)
        
        # اگر کارمندی نبود
        if not employee_cards:
            employee_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF, size=64, color=COLORS["gray_400"]),  # 🔼 بزرگ
                        ft.Text("کارمندی یافت نشد", size=18, color=COLORS["gray_600"]),  # 🔼 بزرگ
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=60,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(employee_cards), 2):
            row_cards = employee_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=280, height=200))  # 🔼 بزرگ
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_salary_position_selection()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["green_100"],
                                    content=ft.Icon(ft.Icons.ATTACH_MONEY, color=COLORS["green_600"], size=24),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(f"لیست {category_names.get(category, category)}", 
                                    size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(f"لیست {category_names.get(category, category)}", 
                                            size=32, weight=ft.FontWeight.BOLD, color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text(f"تعداد: {len(employees)} نفر", 
                                            size=18, color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                                ),
                                
                                ft.Container(height=32),
                                
                                # لیست کارکنان (بزرگ)
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=700,  # 🔼 بزرگ
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_salary_payment_page():
        """صفحه پرداخت حقوق - با تم رنگی بر اساس سمت"""
        
        if not current_employee:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: کارمند انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_salary_employee_list(selected_category))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # تشخیص رنگ بر اساس سمت
        def get_position_color(position):
            color_map = {
                'manager': (COLORS["red_400"], COLORS["red_600"], COLORS["red_100"], COLORS["red_50"]),
                'assistant': (COLORS["blue_400"], COLORS["blue_600"], COLORS["blue_100"], COLORS["blue_50"]),
                'teacher': (COLORS["purple_400"], COLORS["purple_600"], COLORS["purple_100"], COLORS["purple_50"]),
                'counselor': (COLORS["teal_400"], COLORS["teal_600"], COLORS["teal_100"], COLORS["teal_50"]),
                'service': (COLORS["yellow_400"], COLORS["yellow_600"], COLORS["yellow_100"], COLORS["yellow_50"])
            }
            
            # تشخیص دسته سمت
            position_key = current_employee.get('position', '')
            if 'manager' in position_key:
                category = 'manager'
            elif 'assistant' in position_key:
                category = 'assistant'
            elif 'teacher' in position_key:
                category = 'teacher' 
            elif 'counselor' in position_key:
                category = 'counselor'
            else:
                category = 'service'
                
            return color_map.get(category, color_map['teacher'])
        
        # گرفتن رنگ‌های مربوط به سمت
        color_400, color_600, color_100, color_50 = get_position_color(current_employee.get('position', ''))
        
        # فیلدهای فرم با رنگ سمت
        amount_field = ft.TextField(
            label="مبلغ حقوق (تومان)",
            hint_text="مثال: 5000000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=color_600,  # 🔼 رنگ سمت
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=color_600,  # 🔼 رنگ سمت
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        method_dropdown = ft.Dropdown(
            label="نوع پرداخت",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=color_600,  # 🔼 رنگ سمت
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option(method['value'], method['label'])
                for method in get_payment_methods()
            ]
        )
        
        receipt_field = ft.TextField(
            label="شماره رسید/تراکنش",
            hint_text="شماره رسید یا تراکنش",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=color_600,  # 🔼 رنگ سمت
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد پرداخت حقوق...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=color_600,  # 🔼 رنگ سمت
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=color_50,  # 🔼 رنگ سمت
            border=ft.border.all(1, color_600),  # 🔼 رنگ سمت
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=color_600),  # 🔼 رنگ سمت
                ft.Column([
                    ft.Text("پرداخت حقوق با موفقیت ثبت شد!", color=color_600, weight=ft.FontWeight.BOLD),  # 🔼 رنگ سمت
                    ft.Text("جزئیات پرداخت در سیستم ذخیره گردید.", color=color_600, size=12),  # 🔼 رنگ سمت
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_salary(e):
            nonlocal success_banner
            
            print("🎯 شروع ثبت پرداخت حقوق...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # تبدیل تاریخ
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی payment_data
            payment_data = {
                'employee': current_employee['id'],  # ID کارمند
                'amount': int(amount_field.value),
                'payment_date': gregorian_date,
                'payment_method': method_dropdown.value,
                'description': notes_field.value,
                'receipt_number': receipt_field.value
            }
            
            print(f"🔍 payment_data: {payment_data}")
            
            # فراخوانی API
            success, message = create_salary_payment(payment_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "پرداخت حقوق با موفقیت ثبت شد!"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
                method_dropdown.value = None
                receipt_field.value = ""
                notes_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            # ... همان منطق قبلی
            success_banner.visible = False
            page.update()

        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_salary_employee_list(selected_category)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=color_100,  # 🔼 رنگ سمت
                                    content=ft.Icon(ft.Icons.ATTACH_MONEY, color=color_600, size=24),  # 🔼 رنگ سمت
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("پرداخت حقوق", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                # عنوان
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("پرداخت حقوق کارمند", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات پرداخت حقوق را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات کارمند
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=[color_50, color_100]  # 🔼 رنگ سمت
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=color_100,  # 🔼 رنگ سمت
                                                            content=ft.Icon(ft.Icons.PERSON, color=color_600, size=32),  # 🔼 رنگ سمت
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_employee['first_name']} {current_employee['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_employee['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                    
                                                    ft.Container(height=16),
                                                    
                                                    ft.Row([
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("سمت", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_employee.get('position_display', current_employee['position'])}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                    ], spacing=12)
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم پرداخت
                                            ft.Column([
                                                # ردیف اول
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ حقوق (تومان)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ پرداخت", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # ردیف دوم
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("نوع پرداخت", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        method_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("شماره رسید/تراکنش", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        receipt_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=color_600,  # 🔼 رنگ سمت
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت پرداخت حقوق", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_salary
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    # در بخش create_xxx_page functions اضافه کن:

    def create_extra_class_withdraw_grade_page():
        """صفحه انتخاب پایه برای هزینه کلاس تقویتی"""
        
        # پایه‌های تحصیلی
        grade_options = [
            ("پایه اول", "1", COLORS["red_600"], COLORS["red_100"], "هزینه کلاس تقویتی پایه اول"),
            ("پایه دوم", "2", COLORS["orange_600"], COLORS["orange_100"], "هزینه کلاس تقویتی پایه دوم"),
            ("پایه سوم", "3", COLORS["yellow_600"], COLORS["yellow_100"], "هزینه کلاس تقویتی پایه سوم"),
            ("پایه چهارم", "4", COLORS["green_600"], COLORS["green_100"], "هزینه کلاس تقویتی پایه چهارم"),
            ("پایه پنجم", "5", COLORS["blue_600"], COLORS["blue_100"], "هزینه کلاس تقویتی پایه پنجم"),
            ("پایه ششم", "6", COLORS["purple_600"], COLORS["purple_100"], "هزینه کلاس تقویتی پایه ششم")
        ]
        
        # ایجاد کارت‌های پایه (مشابه صفحه tuition_grade)
        option_rows = []
        for i in range(0, len(grade_options), 2):
            row_options = grade_options[i:i+2]
            row_cards = []
            
            for title, number, color, bg_color, description in row_options:
                card = ft.Container(
                    expand=True,
                    height=180,
                    bgcolor=COLORS["white"],
                    border_radius=16,
                    padding=32,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=lambda e, grade_num=number: show_teacher_list(grade_num),
                    content=ft.Row(
                        [
                            # دایره عددی
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                bgcolor=bg_color,
                                content=ft.Text(
                                    number,
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=color
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(width=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        title,
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLORS["gray_900"]
                                    ),
                                    ft.Container(height=8),
                                    ft.Text(
                                        description,
                                        size=14,
                                        color=COLORS["gray_600"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                expand=True
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
                row_cards.append(card)
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True, height=180))
            
            option_rows.append(
                ft.Container(
                    content=ft.Row(row_cards, spacing=24),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=show_withdraw_type
                                        ),
                                        create_icon(
                                            ft.Icons.SCHOOL,
                                            COLORS["indigo_600"],
                                            COLORS["indigo_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "انتخاب پایه تحصیلی",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "هزینه کلاس‌های تقویتی",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLORS["white"],
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Container(height=16),
                                            ft.Text(
                                                "پایه تحصیلی مورد نظر را انتخاب کنید",
                                                size=18,
                                                color=COLORS["blue_100"],
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    )
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Column(
                                        option_rows,
                                        spacing=16,
                                    ),
                                    width=900,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    def create_teacher_list_page():
        """صفحه نمایش لیست معلمان یک پایه"""
        
        # گرفتن معلمان این پایه
        teachers = get_teachers_by_grade(selected_grade)
        
        # نام فارسی پایه
        grade_names = {
            '1': 'اول', '2': 'دوم', '3': 'سوم',
            '4': 'چهارم', '5': 'پنجم', '6': 'ششم'
        }
        
        # ایجاد کارت‌های معلمان
        teacher_cards = []
        for teacher in teachers:
            card = ft.Container(
                width=300,
                height=220,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, t=teacher: show_extra_class_teacher_payment(t),
                content=ft.Column([
                    ft.Container(
                        width=64,
                        height=64,
                        border_radius=32,
                        bgcolor=COLORS["indigo_100"],
                        content=ft.Icon(ft.Icons.PERSON, color=COLORS["indigo_600"], size=32),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        f"{teacher['first_name']} {teacher['last_name']}", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        f"معلم پایه {grade_names.get(selected_grade, selected_grade)}",
                        size=14,
                        color=COLORS["gray_600"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        f"کد ملی: {teacher['national_code']}",
                        size=12,
                        color=COLORS["gray_500"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        bgcolor=COLORS["indigo_50"],
                        padding=ft.padding.symmetric(horizontal=16, vertical=6),
                        border_radius=8,
                        content=ft.Text(
                            "انتخاب برای پرداخت",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["indigo_600"]
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            teacher_cards.append(card)
        
        # اگر معلمی نبود
        if not teacher_cards:
            teacher_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF, size=64, color=COLORS["gray_400"]),
                        ft.Text("معلمی برای این پایه یافت نشد", size=18, color=COLORS["gray_600"]),
                        ft.Text("لطفاً از بخش کارکنان معلم اضافه کنید", size=14, color=COLORS["gray_500"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=60,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۲ تایی
        rows = []
        for i in range(0, len(teacher_cards), 2):  # 👈 تغییر به 2
            row_cards = teacher_cards[i:i+2]       # 👈 تغییر به 2
            
            # اگر ردیف آخر کمتر از ۲ تا بود، کارت خالی اضافه کن
            while len(row_cards) < 2:              # 👈 تغییر به 2
                row_cards.append(ft.Container(width=300, height=220))  # 👈 همون اندازه
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=8)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_extra_class_withdraw_grade()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["indigo_100"],
                                    content=ft.Icon(
                                        ft.Icons.SCHOOL,
                                        color=COLORS["indigo_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(
                                    f"لیست معلمان پایه {grade_names.get(selected_grade, selected_grade)}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"]
                                )
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            f"معلمان پایه {grade_names.get(selected_grade, selected_grade)}", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            "برای پرداخت هزینه کلاس تقویتی انتخاب کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"تعداد: {len(teachers)} نفر", 
                                            size=16, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                                ),
                                
                                ft.Container(height=48),
                                
                                # لیست معلمان
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=700,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_extra_class_teacher_payment_page():
        """صفحه ثبت هزینه کلاس تقویتی برای معلم"""
        
        if not current_teacher:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: معلم انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_teacher_list(selected_grade))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # فیلدهای فرم
        subject_dropdown = ft.Dropdown(
            label="نام درس *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("ریاضی", "ریاضی"),
                ft.dropdown.Option("علوم", "علوم"),
                ft.dropdown.Option("فارسی", "فارسی"),
            ]
        )
        
        amount_field = ft.TextField(
            label="مبلغ هزینه (تومان) *",
            hint_text="مثال: 500000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت *",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد کلاس تقویتی...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["indigo_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["indigo_50"],
            border=ft.border.all(1, COLORS["indigo_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["indigo_600"]),
                ft.Column([
                    ft.Text("هزینه کلاس تقویتی با موفقیت ثبت شد!", color=COLORS["indigo_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات پرداخت در سیستم ذخیره گردید.", color=COLORS["indigo_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_payment(e):
            """ثبت هزینه کلاس تقویتی - نسخه اصلاح شده با تاریخ"""
            nonlocal success_banner

            print("🎯 شروع ثبت هزینه کلاس تقویتی...")
            
            # اعتبارسنجی فرم
            if not subject_dropdown.value:
                show_alert("لطفاً درس مورد نظر را انتخاب کنید")
                return
                    
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                    
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # 🔼 **استفاده از سرویس تاریخ هوشمند (همانند بخش‌های دیگر)**
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            try:
                # تشخیص خودکار فرمت تاریخ
                try:
                    # اول سعی کن به عنوان تاریخ شمسی parse کن
                    gregorian_date = jdatetime.datetime.strptime(date_field.value, '%Y-%m-%d').togregorian()
                    print(f"📅 تشخیص تاریخ شمسی: {date_field.value} → {gregorian_date}")
                except ValueError:
                    try:
                        # اگر شمسی نبود، سعی کن به عنوان میلادی parse کن
                        from datetime import datetime
                        gregorian_date = datetime.strptime(date_field.value, '%Y-%m-%d').date()
                        print(f"📅 تشخیص تاریخ میلادی: {date_field.value} → {gregorian_date}")
                    except ValueError:
                        print(f"❌ فرمت تاریخ نامعتبر: {date_field.value}")
                        show_alert("فرمت تاریخ نامعتبر است!")
                        return
                
                # ✅ حالا از تاریخ میلادی استفاده کن
                payment_data = {
                    'teacher': current_teacher['id'],
                    'amount': int(amount_field.value),
                    'payment_date': gregorian_date.strftime("%Y-%m-%d"),  # 🔥 تاریخ میلادی
                    'subject': subject_dropdown.value,
                    'description': notes_field.value
                }
                
                print(f"🔍 داده‌های پرداخت نهایی: {payment_data}")
                
                # ارسال به API
                success, message = create_extra_class_teacher_payment(payment_data)
                
                if success:
                    print("✅ پرداخت با موفقیت ثبت شد")
                    success_banner.content.controls[1].controls[0].value = "هزینه کلاس تقویتی با موفقیت ثبت شد! 👨‍🏫"
                    success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                    success_banner.visible = True
                    
                    # بازنشانی فرم
                    subject_dropdown.value = None
                    amount_field.value = ""
                    date_field.value = DateService.get_current_jalali()
                    notes_field.value = ""
                    
                    page.update()
                    print("🔄 فرم بازنشانی شد")
                else:
                    show_alert(message)
                    
            except Exception as e:
                print(f"❌ خطای کلی در ثبت: {e}")
                show_alert(f"خطا در ثبت پرداخت: {str(e)}")
        
        def clear_form(e):
            """پاک کردن فرم"""
            subject_dropdown.value = None
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            notes_field.value = ""
            success_banner.visible = False
            page.update()

        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_teacher_list(selected_grade)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["indigo_100"],
                                    content=ft.Icon(ft.Icons.SCHOOL, color=COLORS["indigo_600"], size=24),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت هزینه کلاس تقویتی", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت هزینه کلاس تقویتی", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات هزینه کلاس تقویتی را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات معلم
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=["#f0f9ff", "#e0f2fe"]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["indigo_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["indigo_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_teacher['first_name']} {current_teacher['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_teacher['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                    
                                                    ft.Container(height=16),
                                                    
                                                    ft.Row([
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("پایه تدریس", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"پایه {selected_grade}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                        
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("سمت", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_teacher.get('position_display', 'معلم')}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                    ], spacing=12)
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # درس و مبلغ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("نام درس *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        subject_dropdown
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("مبلغ هزینه (تومان) *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # تاریخ
                                                ft.Column([
                                                    ft.Text("تاریخ پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    date_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    notes_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["indigo_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت هزینه کلاس", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_payment
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_insurance_position_selection_page():
        """صفحه انتخاب سمت برای بیمه - با تم آبی متفاوت"""
        
        # سمت‌های اصلی با تم آبی
        positions = [
            {'key': 'managers', 'name': 'مدیران', 'icon': ft.Icons.SUPERVISOR_ACCOUNT, 'color': (COLORS["blue_400"], COLORS["blue_600"])},
            {'key': 'assistants', 'name': 'معاونان', 'icon': ft.Icons.GROUP, 'color': (COLORS["teal_400"], COLORS["teal_600"])},
            {'key': 'teachers', 'name': 'معلم‌ها', 'icon': ft.Icons.SCHOOL, 'color': (COLORS["cyan_400"], COLORS["cyan_600"])},
            {'key': 'coaches', 'name': 'مربیان', 'icon': ft.Icons.SPORTS_KABADDI, 'color': (COLORS["orange_400"], COLORS["orange_600"])},
            {'key': 'counselors', 'name': 'مشاوران', 'icon': ft.Icons.PSYCHOLOGY, 'color': (COLORS["indigo_400"], COLORS["indigo_600"])},
            {'key': 'services', 'name': 'خدمتگزاران', 'icon': ft.Icons.CLEANING_SERVICES, 'color': (COLORS["light_blue_400"], COLORS["light_blue_600"])}
        ]
        
        # ایجاد کارت‌های سمت
        position_cards = []
        for position in positions:
            card = ft.Container(
                width=280,
                height=160,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=20,
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, pos=position['key']: show_insurance_employee_list(pos),
                content=ft.Column([
                    ft.Container(
                        width=56,
                        height=56,
                        border_radius=28,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[position['color'][0], position['color'][1]]
                        ),
                        content=ft.Icon(
                            name=position['icon'],
                            color=COLORS["white"],
                            size=24
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        position['name'],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "پرداخت بیمه",
                        size=12,
                        color=COLORS["gray_500"],
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            position_cards.append(card)
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(position_cards), 2):
            row_cards = position_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=280, height=160))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=8)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column([
                # هدر
                ft.Container(
                    bgcolor=COLORS["white"],
                    padding=ft.padding.symmetric(vertical=24, horizontal=32),
                    content=ft.Row([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=COLORS["gray_600"],
                                on_click=show_withdraw_type
                            ),
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=COLORS["light_blue_100"],
                                content=ft.Icon(
                                    ft.Icons.HEALTH_AND_SAFETY,
                                    color=COLORS["blue_600"],
                                    size=24
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Text("انتخاب سمت برای بیمه", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                        ], spacing=12)
                    ])
                ),
                
                # محتوای اصلی
                ft.Container(
                    expand=True,
                    padding=32,
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("پرداخت بیمه کارکنان", size=32, weight=ft.FontWeight.BOLD, color=COLORS["white"], text_align=ft.TextAlign.CENTER),
                                ft.Text("سمت مورد نظر را انتخاب کنید", size=18, color=COLORS["blue_100"], text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        ),
                        
                        ft.Container(height=32),
                        
                        ft.Container(
                            content=ft.Column(rows, spacing=8),
                            width=600,
                            alignment=ft.alignment.top_center
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                )
            ], scroll=ft.ScrollMode.ADAPTIVE)
        )
    
    def create_insurance_payment_page():
        """صفحه پرداخت بیمه - با تم آبی زیبا"""
        
        if not current_employee:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: کارمند انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_insurance_employee_list(selected_category))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # فیلدهای فرم با تم آبی
        amount_field = ft.TextField(
            label="مبلغ بیمه (تومان) *",
            hint_text="مثال: 450000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت *",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        insurance_type_dropdown = ft.Dropdown(
            label="نوع بیمه *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("تأمین اجتماعی", "تأمین اجتماعی"),
                ft.dropdown.Option("بیمه درمان", "بیمه درمان"),
                ft.dropdown.Option("بیمه تکمیلی", "بیمه تکمیلی"),
                ft.dropdown.Option("بیمه عمر", "بیمه عمر"),
            ]
        )
        
        payment_method_dropdown = ft.Dropdown(
            label="نوع پرداخت *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option(method['value'], method['label'])
                for method in get_payment_methods()
            ]
        )
        
        receipt_field = ft.TextField(
            label="شماره رسید/تراکنش",
            hint_text="شماره رسید یا تراکنش بانکی",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        description_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات مربوط به پرداخت بیمه...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["blue_50"],
            border=ft.border.all(1, COLORS["blue_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["blue_600"]),
                ft.Column([
                    ft.Text("پرداخت بیمه با موفقیت ثبت شد! 🛡️", color=COLORS["blue_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات پرداخت در سیستم ذخیره گردید.", color=COLORS["blue_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_insurance(e):
            nonlocal success_banner
            
            print("🎯 شروع ثبت پرداخت بیمه...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
                
            if not insurance_type_dropdown.value:
                show_alert("لطفاً نوع بیمه را انتخاب کنید")
                return
                
            if not payment_method_dropdown.value:
                show_alert("لطفاً نوع پرداخت را انتخاب کنید")
                return
            
            # تبدیل تاریخ
            gregorian_date = convert_jalali_to_gregorian(date_field.value)
            if not gregorian_date:
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی payment_data
            payment_data = {
                'employee': current_employee['id'],      # ID کارمند
                'amount': int(amount_field.value),
                'payment_date': gregorian_date,
                'payment_method': payment_method_dropdown.value,
                'insurance_type': insurance_type_dropdown.value,
                'description': description_field.value,
                'receipt_number': receipt_field.value
            }
            
            print(f"🔍 payment_data بیمه: {payment_data}")
            
            # فراخوانی API
            success, message = create_insurance_payment(payment_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "پرداخت بیمه با موفقیت ثبت شد! 🛡️"
                success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
                insurance_type_dropdown.value = None
                payment_method_dropdown.value = None
                receipt_field.value = ""
                description_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            insurance_type_dropdown.value = None
            payment_method_dropdown.value = None
            receipt_field.value = ""
            description_field.value = ""
            success_banner.visible = False
            page.update()

        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]] 
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_insurance_employee_list(selected_category)
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["light_blue_100"],
                                    content=ft.Icon(
                                        ft.Icons.HEALTH_AND_SAFETY,
                                        color=COLORS["blue_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("پرداخت بیمه", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("پرداخت بیمه کارمند", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات پرداخت بیمه را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # اطلاعات کارمند
                                            ft.Container(
                                                gradient=ft.LinearGradient(
                                                    begin=ft.alignment.center_left,
                                                    end=ft.alignment.center_right,
                                                    colors=[COLORS["blue_50"], COLORS["light_blue_100"]]
                                                ),
                                                border_radius=12,
                                                padding=24,
                                                content=ft.Column([
                                                    ft.Row([
                                                        ft.Container(
                                                            width=64,
                                                            height=64,
                                                            border_radius=32,
                                                            bgcolor=COLORS["light_blue_100"],
                                                            content=ft.Icon(ft.Icons.PERSON, color=COLORS["blue_600"], size=32),
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.Column([
                                                            ft.Text(f"{current_employee['first_name']} {current_employee['last_name']}", 
                                                                size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                            ft.Text(f"کد ملی: {current_employee['national_code']}", 
                                                                size=14, color=COLORS["gray_600"])
                                                        ], spacing=4)
                                                    ], spacing=16),
                                                    
                                                    ft.Container(height=16),
                                                    
                                                    ft.Row([
                                                        ft.Container(
                                                            expand=True,
                                                            bgcolor=COLORS["white"],
                                                            border_radius=8,
                                                            padding=16,
                                                            content=ft.Column([
                                                                ft.Text("سمت", size=12, color=COLORS["gray_500"]),
                                                                ft.Text(f"{current_employee.get('position_display', current_employee['position'])}", 
                                                                    size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                                        ),
                                                    ], spacing=12)
                                                ], spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم پرداخت
                                            ft.Column([
                                                # ردیف اول - مبلغ و نوع بیمه
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ بیمه (تومان) *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("نوع بیمه *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        insurance_type_dropdown
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # ردیف دوم - تاریخ و نوع پرداخت
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("تاریخ پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("نوع پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                        payment_method_dropdown
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # شماره رسید
                                                ft.Column([
                                                    ft.Text("شماره رسید/تراکنش", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    receipt_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                                    description_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["blue_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت پرداخت بیمه", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_insurance
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_insurance_employee_list_page(category):
        """صفحه لیست کارکنان برای بیمه"""
        
        # گرفتن کارکنان این دسته
        employees = get_employees_by_category(category)
        
        # نام فارسی دسته
        category_names = {
            'managers': 'مدیران',
            'assistants': 'معاونان', 
            'teachers': 'معلم‌ها',
            'counselors': 'مشاوران',
            'services': 'خدمتگزاران'
        }
        
        # ایجاد کارت‌های کارکنان با استایل آبی
        employee_cards = []
        for employee in employees:
            card = ft.Container(
                width=300,
                height=240,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(8),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, emp=employee: show_insurance_payment_page(emp),
                content=ft.Column([
                    ft.Container(
                        width=64,
                        height=64,
                        border_radius=32,
                        bgcolor=COLORS["blue_100"],
                        content=ft.Icon(ft.Icons.PERSON, color=COLORS["blue_600"], size=32),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        f"{employee['first_name']} {employee['last_name']}", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        f"{employee.get('position_display', employee['position'])}",
                        size=14,
                        color=COLORS["gray_600"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        f"کد ملی: {employee['national_code']}",
                        size=12,
                        color=COLORS["gray_500"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        bgcolor=COLORS["blue_50"],
                        padding=ft.padding.symmetric(horizontal=12, vertical=4),
                        border_radius=6,
                        content=ft.Text(
                            "پرداخت بیمه",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["blue_600"]
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            employee_cards.append(card)
        
        # اگر کارمندی نبود
        if not employee_cards:
            employee_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF, size=64, color=COLORS["gray_400"]),
                        ft.Text("کارمندی یافت نشد", size=18, color=COLORS["gray_600"]),
                        ft.Text("لطفاً از بخش کارکنان اضافه کنید", size=14, color=COLORS["gray_500"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=60,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۲ تایی
        rows = []
        for i in range(0, len(employee_cards), 2):
            row_cards = employee_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=300, height=200))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_insurance_page()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["blue_100"],
                                    content=ft.Icon(
                                        ft.Icons.HEALTH_AND_SAFETY,
                                        color=COLORS["blue_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(
                                    f"لیست {category_names.get(category, category)}", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"]
                                )
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            f"لیست {category_names.get(category, category)}", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            "برای پرداخت بیمه انتخاب کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            f"تعداد: {len(employees)} نفر", 
                                            size=16, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                                ),
                                
                                ft.Container(height=32),
                                
                                # لیست کارکنان
                                ft.Container(
                                    content=ft.Column(
                                        rows,
                                        spacing=16,
                                    ),
                                    width=700,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_petty_cash_page():
        """صفحه ثبت تنخواه با تم صورتی"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ تنخواه (تومان)",
            hint_text="مثال: 1000000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["pink_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ برداشت",
            value=DateService.get_current_jalali(), 
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["pink_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        description_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="علت برداشت تنخواه...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["pink_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["pink_50"],
            border=ft.border.all(1, COLORS["pink_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["pink_600"]),
                ft.Column([
                    ft.Text("تنخواه با موفقیت ثبت شد! 💰", 
                        color=COLORS["pink_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات برداشت در سیستم ذخیره گردید.", 
                        color=COLORS["pink_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_petty_cash(e):
            """ثبت تنخواه - نسخه اصلاح شده"""
            nonlocal success_banner
            
            print("🎯 شروع ثبت تنخواه...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # 🔼 استفاده از سرویس اعتبارسنجی تاریخ
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی داده‌ها - تاریخ شمسی می‌فرستیم (Backend هوشمند هست)
            petty_cash_data = {
                'amount': int(amount_field.value),
                'payment_date': date_field.value,  # 🔼 تاریخ شمسی خام
                'description': description_field.value
            }
            
            print(f"🔍 داده‌های تنخواه: {petty_cash_data}")
            
            # فراخوانی API
            success, message = create_petty_cash(petty_cash_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "تنخواه با موفقیت ثبت شد! 💰"
                success_banner.content.controls[1].controls[1].value = "جزئیات برداشت در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()  # 🔼 استفاده از سرویس تاریخ
                description_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            description_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["pink_100"],
                                    content=ft.Icon(
                                        ft.Icons.ACCOUNT_BALANCE_WALLET, 
                                        color=COLORS["pink_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت تنخواه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت برداشت تنخواه", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات برداشت تنخواه را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["pink_400"], COLORS["pink_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("برداشت تنخواه گردان", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("برداشت وجه برای مصارف جاری", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ تنخواه (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ برداشت", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    description_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["pink_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت تنخواه", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_petty_cash
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )
    
    def create_service_page():
        """صفحه ثبت هزینه سرویس"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ سرویس (تومان)",
            hint_text="مثال: 300000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ سرویس",
            value=DateService.get_current_jalali(),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        description_field = ft.TextField(
            label="توضیحات سرویس",
            hint_text="مثال: سرویس کولر، تعمیر درب، نظافت و...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["orange_50"],
            border=ft.border.all(1, COLORS["orange_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["orange_600"]),
                ft.Column([
                    ft.Text("سرویس با موفقیت ثبت شد! 🔧", 
                        color=COLORS["orange_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات سرویس در سیستم ذخیره گردید.", 
                        color=COLORS["orange_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_service(e):
            """ثبت سرویس"""
            nonlocal success_banner
            
            print("🎯 شروع ثبت سرویس...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # اعتبارسنجی تاریخ
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی داده‌ها
            service_data = {
                'amount': int(amount_field.value),
                'payment_date': date_field.value,
                'description': description_field.value
            }
            
            print(f"🔍 داده‌های سرویس: {service_data}")
            
            # فراخوانی API
            success, message = create_service_payment(service_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "سرویس با موفقیت ثبت شد! 🔧"
                success_banner.content.controls[1].controls[1].value = "جزئیات سرویس در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()
                description_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            description_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["orange_100"],
                                    content=ft.Icon(
                                        ft.Icons.CAR_REPAIR, 
                                        color=COLORS["orange_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت هزینه سرویس", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت هزینه سرویس", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات سرویس را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["orange_400"], COLORS["orange_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.CAR_REPAIR,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("ثبت هزینه سرویس", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("هزینه خدمات و سرویس‌های مدرسه", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ سرویس (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ سرویس", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات سرویس", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    description_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["orange_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت سرویس", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_service
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )

    def create_rent_type_selection_page():
        """صفحه انتخاب نوع کرایه"""
        
        rent_options = [
            {
                "type": "building",
                "title": "ساختمان",
                "icon": ft.Icons.HOME_WORK,
                "color": COLORS["yellow_600"],
                "bg_color": COLORS["yellow_100"],
                "gradient_start": COLORS["yellow_400"],
                "gradient_end": COLORS["yellow_600"],
                "description": "کرایه ساختمان مدرسه"
            },
            {
                "type": "gym", 
                "title": "باشگاه",
                "icon": ft.Icons.SPORTS_GYMNASTICS,
                "color": COLORS["orange_600"],
                "bg_color": COLORS["orange_100"],
                "gradient_start": COLORS["orange_400"],
                "gradient_end": COLORS["orange_600"],
                "description": "کرایه باشگاه ورزشی"
            }
        ]
        
        option_cards = []
        for rent in rent_options:
            card = ft.Container(
                width=300,
                height=280,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=32,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                # 🔥 اینجا مهمه - دکمه‌ها مستقیماً به توابع show وصل میشن
                on_click=lambda e, r=rent: show_rent_page() if r["type"] == "building" else show_gym_rent_page(),
                content=ft.Column(
                    [
                        ft.Container(
                            width=80,
                            height=80,
                            border_radius=40,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[rent["gradient_start"], rent["gradient_end"]]
                            ),
                            content=ft.Icon(
                                rent["icon"],
                                color=COLORS["white"],
                                size=40
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=24),
                        ft.Text(
                            rent["title"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gray_900"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            rent["description"],
                            size=14,
                            color=COLORS["gray_600"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=24),
                        ft.Container(
                            bgcolor=rent["bg_color"],
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=8,
                            content=ft.Text(
                                "انتخاب کنید",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=rent["color"]
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                )
            )
            option_cards.append(card)
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_withdraw_type()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["yellow_100"],
                                    content=ft.Icon(
                                        ft.Icons.HOME_WORK,
                                        color=COLORS["yellow_600"],
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("انتخاب نوع کرایه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("نوع کرایه را انتخاب کنید", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("ساختمان یا باشگاه ورزشی", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=48),
                                
                                ft.Container(
                                    content=ft.Row(
                                        option_cards,
                                        spacing=48,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )

    def select_rent_type(rent_type):
        """انتخاب نوع کرایه و هدایت به صفحه مربوطه"""
        if rent_type["type"] == "building":
            show_rent_page()  # صفحه کرایه ساختمان (همون صفحه فعلی)
        elif rent_type["type"] == "gym":
            show_gym_rent_page()  # صفحه کرایه باشگاه

    def create_gym_rent_page():
        """صفحه ثبت کرایه باشگاه"""
        
        # فیلدهای فرم
        amount_field = ft.TextField(
            label="مبلغ کرایه باشگاه (تومان)",
            hint_text="مثال: 800000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ کرایه",
            value=DateService.get_current_jalali(),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        description_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات مربوط به کرایه باشگاه...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["orange_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["orange_50"],
            border=ft.border.all(1, COLORS["orange_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["orange_600"]),
                ft.Column([
                    ft.Text("کرایه باشگاه با موفقیت ثبت شد! 🏋️", 
                        color=COLORS["orange_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات کرایه در سیستم ذخیره گردید.", 
                        color=COLORS["orange_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_gym_rent(e):
            """ثبت کرایه باشگاه"""
            nonlocal success_banner
            
            print("🎯 شروع ثبت کرایه باشگاه...")
            
            # اعتبارسنجی فیلدها
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # اعتبارسنجی تاریخ
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            # آماده‌سازی داده‌ها
            rent_data = {
                'amount': int(amount_field.value),
                'payment_date': date_field.value,
                'month': "باشگاه",  # ✅ این خط رو اضافه کن
                'description': f"کرایه باشگاه - {description_field.value}"
            }
            
            print(f"🔍 داده‌های کرایه باشگاه: {rent_data}")
            
            # فراخوانی API (همان تابع کرایه ولی با توضیحات متفاوت)
            success, message = create_rent(rent_data)
            
            if success:
                print("✅ موفقیت - نمایش بنر")
                success_banner.content.controls[1].controls[0].value = "کرایه باشگاه با موفقیت ثبت شد! 🏋️"
                success_banner.content.controls[1].controls[1].value = "جزئیات کرایه در سیستم ذخیره گردید."
                success_banner.visible = True
                page.update()
                
                # فقط فیلدها رو پاک کن
                amount_field.value = ""
                date_field.value = DateService.get_current_jalali()
                description_field.value = ""
            else:
                show_alert(message)
        
        def clear_form(e):
            """پاک کردن فرم"""
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            description_field.value = ""
            success_banner.visible = False
            page.update()
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                [
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=24, horizontal=32),
                        content=ft.Row([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=COLORS["gray_600"],
                                    on_click=lambda e: show_rent_type_selection()
                                ),
                                ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=20,
                                    bgcolor=COLORS["orange_100"],
                                    content=ft.Icon(
                                        ft.Icons.SPORTS_GYMNASTICS, 
                                        color=COLORS["orange_600"], 
                                        size=24
                                    ),
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("ثبت کرایه باشگاه", 
                                    size=24, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["gray_900"])
                            ], spacing=12)
                        ])
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=48,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("ثبت کرایه باشگاه", 
                                            size=32, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER),
                                        ft.Text("اطلاعات کرایه باشگاه را وارد کنید", 
                                            size=18, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # کارت اصلی
                                ft.Container(
                                    width=800,
                                    bgcolor=COLORS["white"],
                                    border_radius=16,
                                    padding=32,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 10)
                                    ),
                                    content=ft.Column(
                                        [
                                            # آیکون و عنوان
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Container(
                                                        width=80,
                                                        height=80,
                                                        border_radius=40,
                                                        gradient=ft.LinearGradient(
                                                            begin=ft.alignment.top_left,
                                                            end=ft.alignment.bottom_right,
                                                            colors=[COLORS["orange_400"], COLORS["orange_600"]]
                                                        ),
                                                        content=ft.Icon(
                                                            ft.Icons.SPORTS_GYMNASTICS,
                                                            color=COLORS["white"],
                                                            size=40
                                                        ),
                                                        alignment=ft.alignment.center
                                                    ),
                                                    ft.Container(height=16),
                                                    ft.Text("کرایه باشگاه ورزشی", 
                                                        size=24, 
                                                        weight=ft.FontWeight.BOLD, 
                                                        color=COLORS["gray_900"],
                                                        text_align=ft.TextAlign.CENTER),
                                                    ft.Text("کرایه سالن ورزشی و باشگاه", 
                                                        size=14, 
                                                        color=COLORS["gray_600"],
                                                        text_align=ft.TextAlign.CENTER)
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                                            ),
                                            
                                            ft.Container(height=32),
                                            
                                            # فرم
                                            ft.Column([
                                                # مبلغ و تاریخ
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Text("مبلغ کرایه (تومان)", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        amount_field
                                                    ], expand=True, spacing=8),
                                                    
                                                    ft.Container(width=24),
                                                    
                                                    ft.Column([
                                                        ft.Text("تاریخ کرایه", 
                                                            size=14, 
                                                            weight=ft.FontWeight.W_500, 
                                                            color=COLORS["gray_700"]),
                                                        date_field
                                                    ], expand=True, spacing=8),
                                                ], spacing=0),
                                                
                                                ft.Container(height=24),
                                                
                                                # توضیحات
                                                ft.Column([
                                                    ft.Text("توضیحات (اختیاری)", 
                                                        size=14, 
                                                        weight=ft.FontWeight.W_500, 
                                                        color=COLORS["gray_700"]),
                                                    description_field
                                                ], spacing=8),
                                                
                                                ft.Container(height=32),
                                                
                                                # پیام موفقیت
                                                success_banner,
                                                
                                                ft.Container(height=24),
                                                
                                                # دکمه‌ها
                                                ft.Row([
                                                    ft.Container(
                                                        expand=True,
                                                        height=52,
                                                        bgcolor=COLORS["orange_600"],
                                                        border_radius=8,
                                                        content=ft.Row([
                                                            ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                            ft.Text("ثبت کرایه باشگاه", 
                                                                size=16, 
                                                                weight=ft.FontWeight.W_500, 
                                                                color=COLORS["white"])
                                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                        on_click=submit_gym_rent
                                                    ),
                                                    
                                                    ft.Container(width=16),
                                                    
                                                    ft.Container(
                                                        height=52,
                                                        bgcolor=COLORS["gray_500"],
                                                        border_radius=8,
                                                        padding=ft.padding.symmetric(horizontal=24),
                                                        content=ft.Text("پاک کردن فرم", 
                                                                    size=16, 
                                                                    weight=ft.FontWeight.W_500, 
                                                                    color=COLORS["white"]),
                                                        on_click=clear_form
                                                    ),
                                                ], spacing=0)
                                            ], spacing=0)
                                        ], spacing=0
                                    )
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            spacing=0,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            )
        )

    def create_gifted_class_withdraw_grade_page():
        """صفحه انتخاب پایه برای هزینه کلاس تیزهوشان به معلم"""
        
        # فقط پایه‌های مجاز تیزهوشان (۳, ۴, ۵, ۶)
        gifted_grades = get_gifted_grades()
        grade_choices = get_grade_choices()
        
        # فیلتر کردن فقط پایه‌های مجاز
        gifted_grade_options = [
            grade for grade in grade_choices 
            if grade[0] in gifted_grades
        ]
        
        # ایجاد کارت‌های پایه
        grade_cards = []
        for grade in gifted_grade_options:
            grade_number = grade[0]
            grade_persian = grade[1]
            
            # رنگ‌های مختلف برای هر پایه
            colors = {
                '3': (COLORS["yellow_600"], COLORS["yellow_100"], COLORS["yellow_400"]),
                '4': (COLORS["green_600"], COLORS["green_100"], COLORS["green_400"]),
                '5': (COLORS["purple_600"], COLORS["purple_100"], COLORS["purple_400"]),
                '6': (COLORS["violet_600"], COLORS["violet_100"], COLORS["violet_400"])
            }
            
            color, bg_color, gradient_color = colors.get(grade_number, (COLORS["indigo_600"], COLORS["indigo_100"], COLORS["indigo_400"]))
            
            card = ft.Container(
                width=280,
                height=220,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=32,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, g=grade_number: show_gifted_class_teacher_list(g),
                content=ft.Column([
                    ft.Container(
                        width=80,
                        height=80,
                        border_radius=40,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[gradient_color, color]
                        ),
                        content=ft.Text(
                            grade_number,
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["white"]
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        f"پایه {grade_persian} تیزهوشان",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "هزینه به معلم تیزهوشان",
                        size=14,
                        color=COLORS["gray_600"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        bgcolor=bg_color,
                        padding=ft.padding.symmetric(horizontal=16, vertical=6),
                        border_radius=8,
                        content=ft.Text(
                            "انتخاب معلم",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=color
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            grade_cards.append(card)
        
        # ایجاد ردیف‌های ۲ در ۲
        rows = []
        for i in range(0, len(grade_cards), 2):
            row_cards = grade_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=280, height=220))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=12)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column([
                # هدر
                ft.Container(
                    bgcolor=COLORS["white"],
                    padding=ft.padding.symmetric(vertical=24, horizontal=32),
                    content=ft.Row([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=COLORS["gray_600"],
                                on_click=lambda e: show_withdraw_type()
                            ),
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=COLORS["violet_100"],
                                content=ft.Icon(
                                    ft.Icons.EMOJI_EVENTS,
                                    color=COLORS["violet_600"],
                                    size=24
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Text(
                                "انتخاب پایه تیزهوشان", 
                                size=24, 
                                weight=ft.FontWeight.BOLD, 
                                color=COLORS["gray_900"]
                            )
                        ], spacing=12)
                    ])
                ),
                
                # محتوای اصلی
                ft.Container(
                    expand=True,
                    padding=48,
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    "هزینه کلاس تیزهوشان", 
                                    size=32, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["white"],
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "پایه مورد نظر را برای پرداخت به معلم انتخاب کنید", 
                                    size=18, 
                                    color=COLORS["blue_100"],
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        ),
                        
                        ft.Container(height=48),
                        
                        ft.Container(
                            content=ft.Column(
                                rows,
                                spacing=16,
                            ),
                            width=700,
                            alignment=ft.alignment.top_center
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                )
            ], scroll=ft.ScrollMode.ADAPTIVE)
        )

    def create_gifted_class_teacher_list_page():
        """صفحه نمایش لیست معلمان تیزهوشان یک پایه"""
        
        # گرفتن معلمان این پایه
        teachers = get_teachers_by_grade(selected_grade)
        
        # نام فارسی پایه
        grade_names = {
            '3': 'سوم', '4': 'چهارم', '5': 'پنجم', '6': 'ششم'
        }
        
        # ایجاد کارت‌های معلمان
        teacher_cards = []
        for teacher in teachers:
            card = ft.Container(
                width=300,
                height=240,
                bgcolor=COLORS["white"],
                border_radius=16,
                padding=24,
                margin=ft.margin.all(12),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda e, t=teacher: show_gifted_class_teacher_payment(t),
                content=ft.Column([
                    ft.Container(
                        width=64,
                        height=64,
                        border_radius=32,
                        bgcolor=COLORS["violet_100"],
                        content=ft.Icon(ft.Icons.PERSON, color=COLORS["violet_600"], size=32),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        f"{teacher['first_name']} {teacher['last_name']}", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["gray_900"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        f"معلم تیزهوشان پایه {grade_names.get(selected_grade, selected_grade)}",
                        size=14,
                        color=COLORS["gray_600"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        f"کد ملی: {teacher['national_code']}",
                        size=12,
                        color=COLORS["gray_500"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        bgcolor=COLORS["violet_50"],
                        padding=ft.padding.symmetric(horizontal=16, vertical=6),
                        border_radius=8,
                        content=ft.Text(
                            "انتخاب برای پرداخت",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["violet_600"]
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
            teacher_cards.append(card)
        
        # اگر معلمی نبود
        if not teacher_cards:
            teacher_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF, size=64, color=COLORS["gray_400"]),
                        ft.Text("معلم تیزهوشانی برای این پایه یافت نشد", size=18, color=COLORS["gray_600"]),
                        ft.Text("لطفاً از بخش کارکنان معلم تیزهوشان اضافه کنید", size=14, color=COLORS["gray_500"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=60,
                    alignment=ft.alignment.center
                )
            )
        
        # ایجاد ردیف‌های ۲ تایی
        rows = []
        for i in range(0, len(teacher_cards), 2):
            row_cards = teacher_cards[i:i+2]
            
            if len(row_cards) == 1:
                row_cards.append(ft.Container(width=300, height=240))
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        row_cards,
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=8)
                )
            )
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column([
                # هدر
                ft.Container(
                    bgcolor=COLORS["white"],
                    padding=ft.padding.symmetric(vertical=24, horizontal=32),
                    content=ft.Row([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=COLORS["gray_600"],
                                on_click=lambda e: show_gifted_class_withdraw_grade()
                            ),
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=COLORS["violet_100"],
                                content=ft.Icon(
                                    ft.Icons.EMOJI_EVENTS,
                                    color=COLORS["violet_600"],
                                    size=24
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Text(
                                f"لیست معلمان تیزهوشان پایه {grade_names.get(selected_grade, selected_grade)}", 
                                size=24, 
                                weight=ft.FontWeight.BOLD, 
                                color=COLORS["gray_900"]
                            )
                        ], spacing=12)
                    ])
                ),
                
                # محتوای اصلی
                ft.Container(
                    expand=True,
                    padding=48,
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    f"معلمان تیزهوشان پایه {grade_names.get(selected_grade, selected_grade)}", 
                                    size=32, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["white"],
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "برای پرداخت هزینه کلاس تیزهوشان انتخاب کنید", 
                                    size=18, 
                                    color=COLORS["blue_100"],
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    f"تعداد: {len(teachers)} نفر", 
                                    size=16, 
                                    color=COLORS["blue_100"],
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
                        ),
                        
                        ft.Container(height=48),
                        
                        # لیست معلمان
                        ft.Container(
                            content=ft.Column(
                                rows,
                                spacing=16,
                            ),
                            width=700,
                            alignment=ft.alignment.top_center
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, scroll=ft.ScrollMode.ADAPTIVE)
                )
            ], scroll=ft.ScrollMode.ADAPTIVE)
        )

    def create_gifted_class_teacher_payment_page():
        """صفحه ثبت هزینه کلاس تیزهوشان برای معلم"""
        
        if not current_teacher:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=48),
                    ft.Text("خطا: معلم انتخاب نشده است", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("بازگشت", on_click=lambda e: show_gifted_class_teacher_list(selected_grade))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        
        # فیلدهای فرم
        subject_dropdown = ft.Dropdown(
            label="نام درس *",
            hint_text="انتخاب کنید",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["violet_600"],
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"],
            options=[
                ft.dropdown.Option("ریاضی تیزهوشان", "ریاضی تیزهوشان"),
                ft.dropdown.Option("علوم تیزهوشان", "علوم تیزهوشان"),
                ft.dropdown.Option("فارسی تیزهوشان", "فارسی تیزهوشان"),
                ft.dropdown.Option("هوش و استعداد", "هوش و استعداد"),
            ]
        )
        
        amount_field = ft.TextField(
            label="مبلغ هزینه (تومان) *",
            hint_text="مثال: 800000",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["violet_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.only(left=80, right=16, top=12, bottom=12),
            bgcolor=COLORS["white"],
            text_align=ft.TextAlign.LEFT,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="تومان "
        )
        
        date_field = ft.TextField(
            label="تاریخ پرداخت *",
            value=DateService.get_current_jalali(),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["violet_600"],
            height=52,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        notes_field = ft.TextField(
            label="توضیحات (اختیاری)",
            hint_text="توضیحات اضافی در مورد کلاس تیزهوشان...",
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["violet_600"],
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=COLORS["white"]
        )
        
        success_banner = ft.Container(
            bgcolor=COLORS["violet_50"],
            border=ft.border.all(1, COLORS["violet_600"]),
            border_radius=8,
            padding=16,
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=COLORS["violet_600"]),
                ft.Column([
                    ft.Text("هزینه کلاس تیزهوشان با موفقیت ثبت شد!", color=COLORS["violet_600"], weight=ft.FontWeight.BOLD),
                    ft.Text("جزئیات پرداخت در سیستم ذخیره گردید.", color=COLORS["violet_600"], size=12),
                ], spacing=2)
            ], spacing=12),
            visible=False
        )
        
        def submit_payment(e):
            """ثبت هزینه کلاس تیزهوشان"""
            nonlocal success_banner

            print("🎯 شروع ثبت هزینه کلاس تیزهوشان...")
            
            # اعتبارسنجی فرم
            if not subject_dropdown.value:
                show_alert("لطفاً درس مورد نظر را انتخاب کنید")
                return
                    
            if not amount_field.value or not amount_field.value.isdigit():
                show_alert("لطفاً مبلغ معتبر وارد کنید")
                return
                    
            if not date_field.value:
                show_alert("لطفاً تاریخ را وارد کنید")
                return
            
            # اعتبارسنجی تاریخ
            if not DateService.validate_jalali_date(date_field.value):
                show_alert("تاریخ وارد شده معتبر نیست!")
                return
            
            try:
                # تشخیص خودکار فرمت تاریخ
                try:
                    gregorian_date = jdatetime.datetime.strptime(date_field.value, '%Y-%m-%d').togregorian()
                    print(f"📅 تشخیص تاریخ شمسی: {date_field.value} → {gregorian_date}")
                except ValueError:
                    try:
                        from datetime import datetime
                        gregorian_date = datetime.strptime(date_field.value, '%Y-%m-%d').date()
                        print(f"📅 تشخیص تاریخ میلادی: {date_field.value} → {gregorian_date}")
                    except ValueError:
                        print(f"❌ فرمت تاریخ نامعتبر: {date_field.value}")
                        show_alert("فرمت تاریخ نامعتبر است!")
                        return
                
                payment_data = {
                    'teacher': current_teacher['id'],
                    'amount': int(amount_field.value),
                    'payment_date': gregorian_date.strftime("%Y-%m-%d"),
                    'subject': subject_dropdown.value,
                    'description': notes_field.value
                }
                
                print(f"🔍 داده‌های پرداخت نهایی: {payment_data}")
                
                # ارسال به API
                success, message = create_gifted_class_teacher_payment(payment_data)
                
                if success:
                    print("✅ پرداخت با موفقیت ثبت شد")
                    success_banner.content.controls[1].controls[0].value = "هزینه کلاس تیزهوشان با موفقیت ثبت شد! 🏆"
                    success_banner.content.controls[1].controls[1].value = "جزئیات پرداخت در سیستم ذخیره گردید."
                    success_banner.visible = True
                    
                    # بازنشانی فرم
                    subject_dropdown.value = None
                    amount_field.value = ""
                    date_field.value = DateService.get_current_jalali()
                    notes_field.value = ""
                    
                    page.update()
                    print("🔄 فرم بازنشانی شد")
                else:
                    show_alert(message)
                    
            except Exception as e:
                print(f"❌ خطای کلی در ثبت: {e}")
                show_alert(f"خطا در ثبت پرداخت: {str(e)}")
        
        def clear_form(e):
            """پاک کردن فرم"""
            subject_dropdown.value = None
            amount_field.value = ""
            date_field.value = DateService.get_current_jalali()
            notes_field.value = ""
            success_banner.visible = False
            page.update()

        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column([
                # هدر
                ft.Container(
                    bgcolor=COLORS["white"],
                    padding=ft.padding.symmetric(vertical=24, horizontal=32),
                    content=ft.Row([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=COLORS["gray_600"],
                                on_click=lambda e: show_gifted_class_teacher_list(selected_grade)
                            ),
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=COLORS["violet_100"],
                                content=ft.Icon(ft.Icons.EMOJI_EVENTS, color=COLORS["violet_600"], size=24),
                                alignment=ft.alignment.center
                            ),
                            ft.Text("ثبت هزینه کلاس تیزهوشان", size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                        ], spacing=12)
                    ])
                ),
                
                # محتوای اصلی
                ft.Container(
                    expand=True,
                    padding=48,
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("ثبت هزینه کلاس تیزهوشان", 
                                    size=32, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=COLORS["white"],
                                    text_align=ft.TextAlign.CENTER),
                                ft.Text("اطلاعات هزینه کلاس تیزهوشان را وارد کنید", 
                                    size=18, 
                                    color=COLORS["blue_100"],
                                    text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                        ),
                        
                        ft.Container(height=32),
                        
                        # کارت اصلی
                        ft.Container(
                            width=800,
                            bgcolor=COLORS["white"],
                            border_radius=16,
                            padding=32,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=25,
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                offset=ft.Offset(0, 10)
                            ),
                            content=ft.Column([
                                # اطلاعات معلم
                                ft.Container(
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.center_left,
                                        end=ft.alignment.center_right,
                                        colors=[COLORS["violet_50"], COLORS["violet_100"]]
                                    ),
                                    border_radius=12,
                                    padding=24,
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Container(
                                                width=64,
                                                height=64,
                                                border_radius=32,
                                                bgcolor=COLORS["violet_100"],
                                                content=ft.Icon(ft.Icons.PERSON, color=COLORS["violet_600"], size=32),
                                                alignment=ft.alignment.center
                                            ),
                                            ft.Column([
                                                ft.Text(f"{current_teacher['first_name']} {current_teacher['last_name']}", 
                                                    size=24, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"]),
                                                ft.Text(f"کد ملی: {current_teacher['national_code']}", 
                                                    size=14, color=COLORS["gray_600"])
                                            ], spacing=4)
                                        ], spacing=16),
                                        
                                        ft.Container(height=16),
                                        
                                        ft.Row([
                                            ft.Container(
                                                expand=True,
                                                bgcolor=COLORS["white"],
                                                border_radius=8,
                                                padding=16,
                                                content=ft.Column([
                                                    ft.Text("پایه تدریس", size=12, color=COLORS["gray_500"]),
                                                    ft.Text(f"پایه {selected_grade} تیزهوشان", 
                                                        size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                            ),
                                            
                                            ft.Container(
                                                expand=True,
                                                bgcolor=COLORS["white"],
                                                border_radius=8,
                                                padding=16,
                                                content=ft.Column([
                                                    ft.Text("سمت", size=12, color=COLORS["gray_500"]),
                                                    ft.Text(f"{current_teacher.get('position_display', 'معلم تیزهوشان')}", 
                                                        size=16, weight=ft.FontWeight.BOLD, color=COLORS["gray_900"])
                                                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                            ),
                                        ], spacing=12)
                                    ], spacing=0)
                                ),
                                
                                ft.Container(height=32),
                                
                                # فرم
                                ft.Column([
                                    # درس و مبلغ
                                    ft.Row([
                                        ft.Column([
                                            ft.Text("نام درس *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                            subject_dropdown
                                        ], expand=True, spacing=8),
                                        
                                        ft.Container(width=24),
                                        
                                        ft.Column([
                                            ft.Text("مبلغ هزینه (تومان) *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                            amount_field
                                        ], expand=True, spacing=8),
                                    ], spacing=0),
                                    
                                    ft.Container(height=24),
                                    
                                    # تاریخ
                                    ft.Column([
                                        ft.Text("تاریخ پرداخت *", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                        date_field
                                    ], spacing=8),
                                    
                                    ft.Container(height=24),
                                    
                                    # توضیحات
                                    ft.Column([
                                        ft.Text("توضیحات (اختیاری)", size=14, weight=ft.FontWeight.W_500, color=COLORS["gray_700"]),
                                        notes_field
                                    ], spacing=8),
                                    
                                    ft.Container(height=32),
                                    
                                    # پیام موفقیت
                                    success_banner,
                                    
                                    ft.Container(height=24),
                                    
                                    # دکمه‌ها
                                    ft.Row([
                                        ft.Container(
                                            expand=True,
                                            height=52,
                                            bgcolor=COLORS["violet_600"],
                                            border_radius=8,
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.CHECK, color=COLORS["white"], size=20),
                                                ft.Text("ثبت هزینه کلاس", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"])
                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                            on_click=submit_payment
                                        ),
                                        
                                        ft.Container(width=16),
                                        
                                        ft.Container(
                                            height=52,
                                            bgcolor=COLORS["gray_500"],
                                            border_radius=8,
                                            padding=ft.padding.symmetric(horizontal=24),
                                            content=ft.Text("پاک کردن فرم", size=16, weight=ft.FontWeight.W_500, color=COLORS["white"]),
                                            on_click=clear_form
                                        ),
                                    ], spacing=0)
                                ], spacing=0)
                            ], spacing=0)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, scroll=ft.ScrollMode.ADAPTIVE)
                )
            ], scroll=ft.ScrollMode.ADAPTIVE)
        )

    def create_ledger_page():
        # گرفتن داده‌ها از API
        global filter_results_container
        grade_choices = get_grade_choices()
        transaction_categories = get_transaction_categories()
        operation_types = get_operation_types()
        
        # جدا کردن دسته‌بندی‌های واریز و برداشت
        deposit_categories = [cat for cat in transaction_categories if cat[0] in ['tuition', 'buffet', 'breakfast', 'extra_class_income', 'gifted_class', 'exam']]
        withdraw_categories = [cat for cat in transaction_categories if cat[0] in ['salary', 'insurance', 'purchase', 'rent', 'utilities', 'extra_class_cost', 'petty_cash', 'service']] 

        def on_exam_changed(e):
            """وقتی نوع آزمون تغییر میکنه"""
            print(f"🎯 نوع آزمون انتخاب شده: {exam_type_dropdown.value}")
            
            if exam_type_dropdown.value:
                grade_dropdown.visible = True
                
                exam_names = {
                    'gifted': 'تیزهوشان',
                    'advanced': 'پیشرفته', 
                    'remedial': 'تقویتی',
                    'classroom': 'کلاسی',
                    'preparation': 'آمادگی',
                    'prerequisite': 'پیش نیاز'
                }
                
                exam_name = exam_names.get(exam_type_dropdown.value, exam_type_dropdown.value)
                
                if exam_type_dropdown.value == "gifted":
                    gifted_grades = get_gifted_grades()
                    grade_choices = get_grade_choices()
                    grade_dropdown.options = [
                        ft.dropdown.Option(key="", text=f"همه {exam_name}")
                    ] + [
                        ft.dropdown.Option(key=grade[0], text=grade[1]) 
                        for grade in grade_choices
                        if grade[0] in gifted_grades
                    ]
                else:
                    grade_choices = get_grade_choices()
                    grade_dropdown.options = [
                        ft.dropdown.Option(key="", text=f"همه {exam_name}")
                    ] + [
                        ft.dropdown.Option(key=grade[0], text=grade[1]) 
                        for grade in grade_choices
                    ]
            else:
                grade_dropdown.visible = False
                classroom_dropdown.visible = False
                student_dropdown.visible = False
                
            page.update()

        def on_print_click(e):
            """هنگام کلیک روی دکمه چاپ - نسخه HTML"""
            nonlocal transactions_current
            
            try:
                print("🎯 دکمه پرینت کلیک شد!")
                
                if not filter_results_container.visible:
                    show_alert("لطفاً ابتدا فیلتر اعمال کنید")
                    return
                    
                if not transactions_current or len(transactions_current) == 0:
                    show_alert("هیچ تراکنشی برای چاپ وجود ندارد")
                    return
                
                # نمایش loading
                filter_results_container.content = ft.Container(
                    content=ft.Column([
                        ft.ProgressRing(color=COLORS["green_600"], width=32, height=32),
                        ft.Text("در حال ایجاد گزارش...", 
                            size=16, 
                            color=COLORS["gray_600"],
                            weight=ft.FontWeight.W_500)
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=16),
                    padding=40,
                    alignment=ft.alignment.center
                )
                page.update()
                
                # فراخوانی تابع پرینت
                success, message = print_transactions_pdf(transactions_current)
                
                if success:
                    show_alert("✅ گزارش با موفقیت ایجاد شد و در مرورگر باز شد")
                else:
                    show_alert(f"❌ {message}")
                    
                # بازگرداندن نمایش قبلی
                on_filter_click(e)
                
            except Exception as ex:
                show_alert(f"خطا در ایجاد گزارش: {str(ex)}")
                print(f"❌ خطا در پرینت: {ex}")

        # فیلدهای فیلتر تاریخ
        start_date_field = ft.TextField(
            label="از تاریخ",
            value=jdatetime.datetime.now().replace(day=1).strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            height=44,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            bgcolor=COLORS["white"],
            width=140
        )
        
        end_date_field = ft.TextField(
            label="تا تاریخ",
            value=jdatetime.datetime.now().strftime("%Y-%m-%d"),
            border_radius=8,
            border_color=COLORS["gray_300"],
            focused_border_color=COLORS["blue_600"],
            height=44,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            bgcolor=COLORS["white"],
            width=140
        )

        # Dropdown نوع عملیات
        operation_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع عملیات",
            options=[
                ft.dropdown.Option(key="", text="همه عملیات")  # گزینه پیش‌فرض
            ] + [
                ft.dropdown.Option(key=op[0], text=op[1]) for op in operation_types  # 🔼 از مدل میاد
            ],
        )
        
        # Dropdown نوع تراکنش برای واریز
        transaction_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع تراکنش", 
            options=[
                ft.dropdown.Option(key=cat[0], text=cat[1]) 
                for cat in deposit_categories
            ],
            visible=False
        )

        def load_deposit_categories():
            categories = get_deposit_categories()
            if categories:
                transaction_type_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه واریزی‌ها")  # 🆕 این خط رو اضافه کن
                ] + [
                    ft.dropdown.Option(key=cat[0], text=cat[1]) 
                    for cat in categories
                ]

        load_deposit_categories()
        
        withdraw_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع تراکنش",
            options=[],  # اول خالی
            visible=False
        )
        

        # موقع تعریف یا لود صفحه  
        def load_withdraw_categories():
            categories = get_withdraw_categories()
            if categories:
                withdraw_type_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه برداشت‌ها")
                ] + [
                    ft.dropdown.Option(key=cat[0], text=cat[1]) 
                    for cat in categories
                ]

        load_withdraw_categories()

        # Dropdown پایه تحصیلی
        grade_dropdown = ft.Dropdown(
            width=150,
            label="پایه تحصیلی",
            options=[
                ft.dropdown.Option(key=grade[0], text=grade[1]) 
                for grade in grade_choices
            ],
            visible=False
        )
        
        # Dropdown کلاس‌ها
        classroom_dropdown = ft.Dropdown(
            width=150,
            label="کلاس",
            options=[],  # اول خالی باشه
            visible=False
        )

        # Dropdown دانش‌آموزان
        student_dropdown = ft.Dropdown(
            width=180,
            label="دانش‌آموز", 
            options=[],  # اول خالی باشه
            visible=False
        )

        # Dropdown نوع آزمون
        exam_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع آزمون",
            options=[],  # اول خالی باشه
            visible=False
        )

        exam_type_dropdown.on_change = on_exam_changed

        # Dropdown دسته‌بندی
        category_dropdown = ft.Dropdown(
            width=180,
            label="دسته‌بندی",
            options=[],  # اول خالی باشه
            visible=False
        )

        # Dropdown سمت‌ها
        position_dropdown = ft.Dropdown(
            width=180,
            label="سمت",
            options=[],  # اول خالی باشه
            visible=False
        )

        # Dropdown افراد
        employee_dropdown = ft.Dropdown(
            width=200,
            label="فرد مورد نظر",
            options=[],  # اول خالی باشه
            visible=False
        )

        utility_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع قبض",
            options=[],  # اول خالی
            visible=False
        )

        rent_type_dropdown = ft.Dropdown(
            width=180,
            label="نوع کرایه",
            options=[], 
            visible=False
        )

        # Dropdown معلم‌ها
        teacher_dropdown = ft.Dropdown(
            width=200,
            label="معلم مورد نظر",
            options=[],  # اول خالی باشه
            visible=False
        )

        def load_utility_types():
            utility_types = get_utility_types()
            print(f"🔧 دریافت انواع قبض از API: {utility_types}")
            
            if utility_types:
                utility_type_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه قبوض")  # 🔥 key خالی برای "همه"
                ] + [
                    ft.dropdown.Option(key=util[0], text=util[1]) 
                    for util in utility_types
                ]
                print(f"✅ dropdown قبوض آپدیت شد")
        
        # تابع برای نمایش/مخفی کردن Dropdownها
        def on_operation_changed(e):
            # اول همه dropdownها رو مخفی کن
            transaction_type_dropdown.visible = False
            withdraw_type_dropdown.visible = False
            grade_dropdown.visible = False
            classroom_dropdown.visible = False
            student_dropdown.visible = False
            exam_type_dropdown.visible = False
            category_dropdown.visible = False
            position_dropdown.visible = False
            employee_dropdown.visible = False
            utility_type_dropdown.visible = False
            teacher_dropdown.visible = False
            
            # ریست کردن همه مقادیر
            transaction_type_dropdown.value = None
            withdraw_type_dropdown.value = None
            grade_dropdown.value = None
            classroom_dropdown.value = None
            student_dropdown.value = None
            exam_type_dropdown.value = None
            category_dropdown.value = None
            position_dropdown.value = None
            employee_dropdown.value = None
            utility_type_dropdown.value = None
            teacher_dropdown.value = None

            if operation_type_dropdown.value == "deposit":
                transaction_type_dropdown.visible = True
                withdraw_type_dropdown.visible = False
                
                # لود کردن دسته‌بندی‌های واریز
                load_deposit_categories()
                
            elif operation_type_dropdown.value == "withdraw":
                transaction_type_dropdown.visible = False
                withdraw_type_dropdown.visible = True
                
                # لود کردن دسته‌بندی‌های برداشت
                load_withdraw_categories()
                
            else:
                # برای "همه عملیات"
                transaction_type_dropdown.visible = False
                withdraw_type_dropdown.visible = False
                
            page.update()
        
        # تابع برای نمایش پایه وقتی شهریه انتخاب شد
        def on_transaction_changed(e):
            # اول همه dropdownهای وابسته رو مخفی کن
            grade_dropdown.visible = False
            classroom_dropdown.visible = False
            student_dropdown.visible = False
            exam_type_dropdown.visible = False
            category_dropdown.visible = False
            position_dropdown.visible = False
            employee_dropdown.visible = False
            utility_type_dropdown.visible = False
            teacher_dropdown.visible = False
            
            # ریست کردن مقادیر
            grade_dropdown.value = None
            classroom_dropdown.value = None
            student_dropdown.value = None
            exam_type_dropdown.value = None
            category_dropdown.value = None
            position_dropdown.value = None
            employee_dropdown.value = None
            utility_type_dropdown.value = None
            teacher_dropdown.value = None

            if transaction_type_dropdown.value == "tuition":
                # بخش شهریه مدرسه
                grade_dropdown.visible = True
                
                # آپدیت options های Dropdown پایه
                grade_choices = get_grade_choices()
                grade_dropdown.options = [
                    ft.dropdown.Option(key="", text="کل شهریه واریزی")  # 🆕 این خط رو اضافه کن
                ] + [
                    ft.dropdown.Option(key=grade[0], text=grade[1]) 
                    for grade in grade_choices
                ]
                
            elif transaction_type_dropdown.value == "extra_class_income":
                # بخش شهریه کلاس تقویتی
                grade_dropdown.visible = True
                
                # آپدیت options های Dropdown پایه
                grade_choices = get_grade_choices()
                grade_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه کلاس‌های تقویتی")  
                ] + [
                    ft.dropdown.Option(key=grade[0], text=grade[1]) 
                    for grade in grade_choices
                ]
            elif transaction_type_dropdown.value == "gifted_class":
                # بخش کلاس تیزهوشان
                grade_dropdown.visible = True
                
                # فقط پایه‌های مجاز تیزهوشان
                gifted_grades = get_gifted_grades()
                grade_choices = get_grade_choices()
                
                grade_dropdown.options = [
                    ft.dropdown.Option(key="", text="🎯 همه کلاس‌های تیزهوشان") 
                ] + [
                    ft.dropdown.Option(key=grade[0], text=grade[1]) 
                    for grade in grade_choices
                    if grade[0] in gifted_grades
                ]
                
            elif transaction_type_dropdown.value == "exam":
                # بخش آزمون
                exam_type_dropdown.visible = True
                
                # آپدیت options های Dropdown آزمون
                exam_types = get_exam_types()
                
                
                exam_type_dropdown.options = [
                    ft.dropdown.Option(key="", text="📝 همه آزمون‌ها") 
                ] + [
                    ft.dropdown.Option(key=exam[0], text=exam[1]) 
                    for exam in exam_types
                ]
                
            elif transaction_type_dropdown.value == "buffet":
                # بخش بوفه - هیچ dropdown اضافی نیاز نیست
                pass
                
            elif transaction_type_dropdown.value == "breakfast":
                # بخش صبحانه - هیچ dropdown اضافی نیاز نیست
                pass

            else:
                # برای بقیه انواع واریز
                grade_dropdown.visible = False
                classroom_dropdown.visible = False
                student_dropdown.visible = False
                exam_type_dropdown.visible = False
                
            page.update()
        
        # تابع برای وقتی که پایه تغییر میکنه
        def on_grade_changed(e):
            """وقتی پایه تغییر میکنه - نسخه کامل اصلاح شده با پشتیبانی از کلاس تیزهوشان"""
            # اول dropdownهای وابسته رو مخفی کن
            classroom_dropdown.visible = False
            student_dropdown.visible = False
            teacher_dropdown.visible = False
            
            # ریست کردن مقادیر
            classroom_dropdown.value = None
            student_dropdown.value = None
            teacher_dropdown.value = None

            if grade_dropdown.value:
                # پیدا کردن نام پایه انتخاب شده
                grade_name = "نامشخص"
                for option in grade_dropdown.options:
                    if option.key == grade_dropdown.value:
                        grade_name = option.text
                        break
                
                print(f"پایه انتخاب شده: {grade_dropdown.value} - نام: {grade_name}")

                # هزینه کلاس تقویتی به معلم (برداشت)
                if (withdraw_type_dropdown.value == "extra_class_cost" and
                    operation_type_dropdown.value == "withdraw"):
                    
                    print("حالت: هزینه کلاس تقویتی به معلم")
                    # بخش هزینه به معلم هست - معلم‌ها رو نشون بده
                    teacher_dropdown.visible = True
                    
                    # فیلتر معلمان بر اساس پایه
                    try:
                        all_teachers = get_employees()
                        print(f"تعداد کل معلمان: {len(all_teachers)}")
                        
                        teachers = [
                            teacher for teacher in all_teachers
                            if teacher.get('position') == f'teacher_grade{grade_dropdown.value}'
                        ]
                        
                        print(f"تعداد معلمان پایه {grade_dropdown.value}: {len(teachers)}")
                        
                        for teacher in teachers:
                            print(f"   {teacher['first_name']} {teacher['last_name']} - سمت: {teacher.get('position')}")
                        
                        if teachers:
                            teacher_dropdown.options = [
                                ft.dropdown.Option(key="", text=f"همه معلم‌های پایه {grade_name}")
                            ] + [
                                ft.dropdown.Option(
                                    key=str(teacher['id']),
                                    text=f"{teacher['first_name']} {teacher['last_name']}"
                                )
                                for teacher in teachers
                            ]
                            print(f"dropdown معلمان با {len(teachers)} معلم آپدیت شد")
                        else:
                            teacher_dropdown.options = [
                                ft.dropdown.Option(key="", text="معلمی برای این پایه یافت نشد")
                            ]
                            print("معلمی برای این پایه یافت نشد")
                            
                    except Exception as error:
                        print(f"خطا در دریافت معلمان: {error}")
                        teacher_dropdown.options = [
                            ft.dropdown.Option(key="", text="خطا در دریافت معلمان")
                        ]

                # هزینه کلاس تیزهوشان به معلم (برداشت) - دقیقاً مثل کلاس تقویتی
                elif (withdraw_type_dropdown.value == "gifted_class_cost" and
                    operation_type_dropdown.value == "withdraw"):
                    
                    print("حالت: هزینه کلاس تیزهوشان به معلم")
                    teacher_dropdown.visible = True
                    
                    try:
                        all_teachers = get_employees()
                        print(f"تعداد کل معلمان: {len(all_teachers)}")
                        
                        # فقط معلمان پایه فعلی (مثلاً چهارم)
                        teachers = [
                            teacher for teacher in all_teachers
                            if teacher.get('position') == f'teacher_grade{grade_dropdown.value}'
                        ]
                        
                        print(f"تعداد معلمان پایه {grade_dropdown.value}: {len(teachers)}")
                        
                        for teacher in teachers:
                            print(f"   {teacher['first_name']} {teacher['last_name']} - پایه {grade_dropdown.value}")
                        
                        if teachers:
                            teacher_dropdown.options = [
                                ft.dropdown.Option(key="", text=f"همه معلم‌های پایه {grade_name}")
                            ] + [
                                ft.dropdown.Option(
                                    key=str(teacher['id']),
                                    text=f"{teacher['first_name']} {teacher['last_name']}"
                                )
                                for teacher in teachers
                            ]
                            # اگر قبلاً "همه" انتخاب شده بود، دوباره انتخابش کن
                            if teacher_dropdown.value == "" or teacher_dropdown.value is None:
                                teacher_dropdown.value = ""
                            print(f"dropdown معلمان فقط با معلم‌های پایه {grade_name} آپدیت شد")
                        else:
                            teacher_dropdown.options = [
                                ft.dropdown.Option(key="", text="معلمی برای این پایه یافت نشد")
                            ]
                            teacher_dropdown.value = ""
                            print("معلمی برای این پایه یافت نشد")
                            
                    except Exception as error:
                        print(f"خطا در دریافت معلمان: {error}")
                        teacher_dropdown.options = [ft.dropdown.Option(key="", text="خطا در دریافت معلمان")]
                        teacher_dropdown.value = ""

                # اگر از بخش کلاس تیزهوشان اومده (واریز)
                elif (transaction_type_dropdown.value == "gifted_class" and
                    operation_type_dropdown.value == "deposit"):
                    
                    print("حالت: کلاس تیزهوشان")
                    classroom_dropdown.visible = True
                    
                    classrooms = get_classrooms(grade=grade_dropdown.value)
                    
                    if classrooms:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text=f"همه کلاس‌های تیزهوشان پایه {grade_name}")
                        ] + [
                            ft.dropdown.Option(key=str(cls['id']), text=f"کلاس {cls['class_number']}")
                            for cls in classrooms
                        ]
                        print(f"تعداد کلاس‌ها: {len(classrooms)}")
                    else:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text="کلاسی یافت نشد")
                        ]
                        print("کلاسی یافت نشد")

                # اگر از بخش شهریه مدرسه اومده
                elif (transaction_type_dropdown.value == "tuition" and
                    operation_type_dropdown.value == "deposit"):
                    
                    print("حالت: شهریه مدرسه")
                    classroom_dropdown.visible = True
                    
                    classrooms = get_classrooms(grade=grade_dropdown.value)
                    
                    if classrooms:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text=f"همه کلاس‌های پایه {grade_name}")
                        ] + [
                            ft.dropdown.Option(key=str(cls['id']), text=f"کلاس {cls['class_number']}")
                            for cls in classrooms
                        ]
                        print(f"تعداد کلاس‌ها: {len(classrooms)}")
                    else:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text="کلاسی یافت نشد")
                        ]
                        print("کلاسی یافت نشد")

                # اگر از بخش شهریه کلاس تقویتی اومده
                elif (transaction_type_dropdown.value == "extra_class_income" and
                    operation_type_dropdown.value == "deposit"):
                    
                    print("حالت: شهریه کلاس تقویتی")
                    classroom_dropdown.visible = True
                    
                    classrooms = get_classrooms(grade=grade_dropdown.value)
                    
                    if classrooms:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text=f"همه کلاس‌های تقویتی پایه {grade_name}")
                        ] + [
                            ft.dropdown.Option(key=str(cls['id']), text=f"کلاس {cls['class_number']}")
                            for cls in classrooms
                        ]
                        print(f"تعداد کلاس‌ها: {len(classrooms)}")
                    else:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text="کلاسی یافت نشد")
                        ]
                        print("کلاسی یافت نشد")

                # اگر از بخش آزمون اومده
                elif (exam_type_dropdown.value and
                    operation_type_dropdown.value == "deposit"):
                    
                    print("حالت: آزمون")
                    classroom_dropdown.visible = True
                    
                    classrooms = get_classrooms(grade=grade_dropdown.value)
                    
                    if classrooms:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text=f"همه آزمون‌های پایه {grade_name}")
                        ] + [
                            ft.dropdown.Option(key=str(cls['id']), text=f"کلاس {cls['class_number']}")
                            for cls in classrooms
                        ]
                        print(f"تعداد کلاس‌ها: {len(classrooms)}")
                    else:
                        classroom_dropdown.options = [
                            ft.dropdown.Option(key="", text="کلاسی یافت نشد")
                        ]
                        print("کلاسی یافت نشد")
                
                else:
                    print("حالت: نامشخص - هیچ dropdownی نمایش داده نمی‌شود")

            else:
                # اگر پایه انتخاب نشده، همه رو مخفی کن
                classroom_dropdown.visible = False
                student_dropdown.visible = False
                teacher_dropdown.visible = False
                print("پایه انتخاب نشده - همه dropdownها مخفی شدند")
            
            page.update()

        # تابع برای وقتی که کلاس تغییر میکنه
        def on_classroom_changed(e):
            """وقتی کلاس تغییر میکنه - نسخه اصلاح شده"""
            print(f"🎯 کلاس انتخاب شده: {classroom_dropdown.value}")
            
            # 🔼 این بخش رو اضافه کن - اگر "همه" انتخاب شده، دانش‌آموزان رو مخفی کن
            if classroom_dropdown.value == "" or classroom_dropdown.value is None:
                print("🎯 حالت 'همه کلاس‌ها' انتخاب شد")
                student_dropdown.visible = False
                student_dropdown.value = None
                student_dropdown.options = []
                page.update()
                return
            
            if classroom_dropdown.value:
                # پیدا کردن نام کلاس انتخاب شده
                classroom_name = "نامشخص"
                for option in classroom_dropdown.options:
                    if option.key == classroom_dropdown.value:
                        classroom_name = option.text
                        break
                
                # گرفتن دانش‌آموزان این کلاس از API
                students = get_students(classroom_id=classroom_dropdown.value)
                print(f"✅ تعداد دانش‌آموزان دریافت شده: {len(students)}")
                
                # آپدیت options های Dropdown دانش‌آموز
                if students:
                    student_dropdown.options = [
                        ft.dropdown.Option(key="", text=f"👥 همه دانش‌آموزان {classroom_name}")
                    ] + [
                        ft.dropdown.Option(
                            key=str(std['id']), 
                            text=f"{std['first_name']} {std['last_name']}"
                        )
                        for std in students
                    ]
                    student_dropdown.visible = True
                    print(f"🎯 dropdown دانش‌آموزان با {len(students)} دانش‌آموز آپدیت شد")
                else:
                    student_dropdown.options = [
                        ft.dropdown.Option(key="", text="❌ دانش‌آموزی یافت نشد")
                    ]
                    student_dropdown.visible = True
                    print("❌ دانش‌آموزی یافت نشد")
            else:
                student_dropdown.visible = False
                student_dropdown.value = None
                student_dropdown.options = []
                print("🎯 کلاس انتخاب نشده - dropdown دانش‌آموزان مخفی شد")
                
            page.update()


        def on_withdraw_changed(e):
            print(f"withdraw_type تغییر کرد به: {withdraw_type_dropdown.value}")
            # اول همه dropdownهای وابسته رو مخفی کن
            category_dropdown.visible = False
            position_dropdown.visible = False
            employee_dropdown.visible = False
            exam_type_dropdown.visible = False
            grade_dropdown.visible = False
            classroom_dropdown.visible = False
            student_dropdown.visible = False
            utility_type_dropdown.visible = False
            teacher_dropdown.visible = False
            rent_type_dropdown.visible = False  # جدید
            
            # ریست کردن مقادیر
            category_dropdown.value = None
            position_dropdown.value = None
            employee_dropdown.value = None
            exam_type_dropdown.value = None
            grade_dropdown.value = None
            classroom_dropdown.value = None
            student_dropdown.value = None
            utility_type_dropdown.value = None
            teacher_dropdown.value = None
            rent_type_dropdown.value = None  # جدید

            if withdraw_type_dropdown.value == "salary":
                # بخش حقوق
                category_dropdown.visible = True
                
                # آپدیت options های Dropdown دسته‌بندی
                category_choices = get_category_choices()
                category_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه حقوق‌ها")
                ] + [
                    ft.dropdown.Option(key=cat[0], text=cat[1])
                    for cat in category_choices
                ]
                
            elif withdraw_type_dropdown.value == "insurance":
                # بخش بیمه
                category_dropdown.visible = True
                
                # آپدیت options های Dropdown دسته‌بندی
                category_choices = get_category_choices()
                category_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه بیمه‌ها")
                ] + [
                    ft.dropdown.Option(key=cat[0], text=cat[1])
                    for cat in category_choices
                ]
                
            elif withdraw_type_dropdown.value == "extra_class_cost":
                # هزینه کلاس تقویتی - با گزینه "همه پایه‌ها"
                grade_dropdown.visible = True
                
                # گرفتن همه پایه‌ها
                grade_choices = get_grade_choices()
                
                # اضافه کردن گزینه "همه پایه‌ها" در بالای لیست
                grade_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه پایه‌ها"),
                ] + [
                    ft.dropdown.Option(key=grade[0], text=grade[1])
                    for grade in grade_choices
                ]
                
                print("هزینه کلاس تقویتی → پایه‌ها با گزینه 'همه پایه‌ها' نمایش داده شد")
                
            elif withdraw_type_dropdown.value == "gifted_class_cost":
                # بخش هزینه کلاس تیزهوشان - فقط پایه‌های ۳، ۴، ۵، ۶
                grade_dropdown.visible = True
                
                # همه پایه‌ها رو می‌گیریم
                all_grades = get_grade_choices()  # مثلاً: [(1, "اول"), (2, "دوم"), ...]
                
                # فقط پایه‌های ۳ تا ۶ رو نگه می‌داریم
                gifted_grades = [grade for grade in all_grades if int(grade[0]) >= 3]
                
                # آپدیت dropdown با گزینه "همه پایه‌های تیزهوشان" + پایه‌های ۳ تا ۶
                grade_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه پایه‌های تیزهوشان")  # گزینه اول: همه
                ] + [
                    ft.dropdown.Option(key=grade[0], text=grade[1])
                    for grade in gifted_grades
                ]
                
                print("فقط پایه‌های ۳، ۴، ۵، ۶ برای کلاس تیزهوشان نمایش داده شد")

            elif withdraw_type_dropdown.value == "utilities":
                # بخش قبوض - dropdown نوع قبض نیاز داره
                utility_type_dropdown.visible = True
                load_utility_types()
                
            elif withdraw_type_dropdown.value == "purchase":
                # بخش خرید - هیچ dropdown اضافی نیاز نیست
                pass
                
            elif withdraw_type_dropdown.value == "rent":
                # بخش کرایه - dropdown نوع کرایه نیاز داره
                rent_type_dropdown.visible = True
                
                # آپدیت options های Dropdown نوع کرایه
                rent_type_dropdown.options = [
                    ft.dropdown.Option(key="", text="همه کرایه‌ها"),
                    ft.dropdown.Option(key="building", text="کرایه ساختمان"),
                    ft.dropdown.Option(key="gym", text="کرایه باشگاه")
                ]
                
            elif withdraw_type_dropdown.value == "petty_cash":
                # بخش تنخواه - هیچ dropdown اضافی نیاز نیست
                pass
                
            elif withdraw_type_dropdown.value == "service":
                # بخش سرویس - هیچ dropdown اضافی نیاز نیست
                pass
            
            page.update()

        def on_category_changed(e):
            # اول همه رو مخفی و ریست کن
            position_dropdown.visible = False
            employee_dropdown.visible = False
            position_dropdown.value = None
            employee_dropdown.value = None

            if category_dropdown.value and category_dropdown.value != '':
                print(f"دسته‌بندی انتخاب شد: {category_dropdown.value}")

                # اگر دسته‌بندی "مربی‌ها" بود (مثلاً keyش "coaches" هست)
                if category_dropdown.value == "coaches":  # ← اینو چک کن با مدلت، احتمالاً همینه
                    position_dropdown.visible = True
                    position_dropdown.label = "نوع مربی"

                    # این دقیقاً همون چیزیه که می‌خواستی:
                    position_dropdown.options = [
                        ft.dropdown.Option("__ALL__", "همه مربی‌ها"),           # گزینه اول
                        ft.dropdown.Option("sport_teacher", "مربی تربیت بدنی"),
                        ft.dropdown.Option("art_teacher", "مربی هنر")
                    ]

                else:
                    # برای بقیه دسته‌بندی‌ها (مدیران، معلم‌ها و ...) مثل قبل
                    position_dropdown.visible = True
                    position_dropdown.label = "سمت"

                    positions = get_positions_by_category(category_dropdown.value)
                    print(f"تعداد سمت‌های دریافت شده: {len(positions)}")

                    position_dropdown.options = [
                        ft.dropdown.Option("__ALL__", "همه سمت‌ها")
                    ] + [
                        ft.dropdown.Option(pos['value'], pos['label'])
                        for pos in positions
                    ]

            page.update()

        def on_position_changed(e):
            # اول همه چیز رو ریست کن
            employee_dropdown.visible = False
            employee_dropdown.options = []
            employee_dropdown.value = None

            selected_position = position_dropdown.value

            # اگر هیچی انتخاب نشده باشه
            if not selected_position:
                page.update()
                return

            # اگر "همه مربی‌ها" یا "همه سمت‌ها" انتخاب شده باشه → دیگه کارمند نمی‌خوایم
            if selected_position == "__ALL__":
                print("همه انتخاب شد — نیازی به انتخاب کارمند نیست")
                employee_dropdown.visible = False
                page.update()
                return

            # اگر در بخش مربی‌ها هستیم (دسته‌بندی = coaches)
            if category_dropdown.value == "coaches":
                employee_dropdown.visible = True
                employee_dropdown.label = "انتخاب مربی"

                # این دو تا سمت جدید رو مثل بقیه با تابع خودت بگیر
                employees = get_employees_by_position(selected_position)

                if employees:
                    employee_dropdown.options = [
                        ft.dropdown.Option(str(emp['id']), f"{emp['first_name']} {emp['last_name']}")
                        for emp in employees
                    ]
                else:
                    employee_dropdown.options = [ft.dropdown.Option("", "مربی‌ای یافت نشد")]

            # برای همه سمت‌های دیگه (مدیران، معلمان، معاونان و ...)
            else:
                employee_dropdown.visible = True
                employee_dropdown.label = "کارمند"

                employees = get_employees_by_position(selected_position)

                if employees:
                    employee_dropdown.options = [
                        ft.dropdown.Option(str(emp['id']), f"{emp['first_name']} {emp['last_name']}")
                        for emp in employees
                    ]

            page.update()
        
        # Event رو به Dropdownها وصل کن
        operation_type_dropdown.on_change = on_operation_changed
        transaction_type_dropdown.on_change = on_transaction_changed
        grade_dropdown.on_change = on_grade_changed
        classroom_dropdown.on_change = on_classroom_changed
        exam_type_dropdown.on_change = on_exam_changed
        withdraw_type_dropdown.on_change = on_withdraw_changed
        category_dropdown.on_change = on_category_changed
        position_dropdown.on_change = on_position_changed
        # دکمه اعمال فیلتر
        apply_filter_btn = ft.Container(
            height=44,
            bgcolor=COLORS["blue_600"],
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=20),
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH, color=COLORS["white"], size=20),
                ft.Text("اعمال فیلتر", size=14, weight=ft.FontWeight.W_500, color=COLORS["white"])
            ], spacing=8),
        )

        # ایجاد کانتینر برای نمایش نتایج
        filter_results_container = ft.Container(
            visible=False,
            margin=ft.margin.only(top=20)
        )

        # دکمه پرینت - این رو اضافه کن
        print_btn = ft.Container(
            height=44,
            bgcolor=COLORS["green_600"],
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=20),
            content=ft.Row([
                ft.Icon(ft.Icons.PRINT, color=COLORS["white"], size=20),
                ft.Text("چاپ گزارش", size=14, weight=ft.FontWeight.W_500, color=COLORS["white"])
            ], spacing=8),
            on_click=on_print_click
        )

        
        # به جای اون Row ساده، این رو اضافه کن:
        ft.Container(
            content=ft.Row([
                ft.Text("بازه زمانی:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(width=12),
                start_date_field,
                ft.Text("تا", size=14),
                end_date_field,
                ft.Container(expand=True),
                apply_filter_btn,
                ft.Container(width=8),
                print_btn 
            ], alignment=ft.MainAxisAlignment.START)
        )

        def on_filter_click(e):
            """هنگام کلیک روی دکمه فیلتر - نسخه نهایی، بدون باگ، عاشقانه و حرفه‌ای"""
            try:
                print("دکمه فیلتر کلیک شد!")
                print("وضعیت dropdownها قبل از ارسال:")
                print(f"   operation_type: '{operation_type_dropdown.value}'")
                print(f"   withdraw_type: '{withdraw_type_dropdown.value}'")
                print(f"   grade: '{grade_dropdown.value}'")
                print(f"   teacher: '{teacher_dropdown.value}'")

                # اعتبارسنجی تاریخ‌ها (بدون تغییر)
                validation_errors = []
                
                if not start_date_field.value:
                    validation_errors.append("• تاریخ شروع را وارد کنید")
                else:
                    if not DateService.validate_jalali_date(start_date_field.value):
                        validation_errors.append("• تاریخ شروع نامعتبر است")
                
                if not end_date_field.value:
                    validation_errors.append("• تاریخ پایان را وارد کنید")
                else:
                    if not DateService.validate_jalali_date(end_date_field.value):
                        validation_errors.append("• تاریخ پایان نامعتبر است")
                
                if start_date_field.value and end_date_field.value:
                    try:
                        start = jdatetime.datetime.strptime(start_date_field.value, '%Y-%m-%d')
                        end = jdatetime.datetime.strptime(end_date_field.value, '%Y-%m-%d')
                        if start > end:
                            validation_errors.append("• تاریخ شروع نمی‌تواند از تاریخ پایان بزرگتر باشد")
                    except ValueError:
                        pass
                
                if validation_errors:
                    error_message = "لطفاً موارد زیر را اصلاح کنید:\n\n" + "\n".join(validation_errors)
                    show_alert(error_message(error_message))
                    return
                
                print("تمام validation ها passed شد")

                # نمایش loading
                filter_results_container.content = ft.Container(
                    content=ft.Column([
                        ft.ProgressRing(color=COLORS["blue_600"], width=32, height=32),
                        ft.Text("در حال دریافت داده‌ها...", size=16, color=COLORS["gray_600"], weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                    padding=40, alignment=ft.alignment.center
                )
                filter_results_container.visible = True
                page.update()

                def clean_filter_value(value):
                    if value is None:
                        return None
                    if isinstance(value, str):
                        value = value.strip()
                        if value.lower() in ['none', 'null', ''] or value == '':
                            return None
                    return value

                # جمع‌آوری فیلترهای خام
                filters = {
                    'operation_type': clean_filter_value(operation_type_dropdown.value),
                    'transaction_type': clean_filter_value(transaction_type_dropdown.value),
                    'withdraw_type': clean_filter_value(withdraw_type_dropdown.value),
                    'grade': clean_filter_value(grade_dropdown.value),
                    'classroom': clean_filter_value(classroom_dropdown.value),
                    'student': clean_filter_value(student_dropdown.value),
                    'start_date': clean_filter_value(start_date_field.value),
                    'end_date': clean_filter_value(end_date_field.value),
                    'exam_type': clean_filter_value(exam_type_dropdown.value),
                    'position': clean_filter_value(position_dropdown.value),
                    'employee': clean_filter_value(employee_dropdown.value),
                    'utility_type': clean_filter_value(utility_type_dropdown.value),
                    'teacher': clean_filter_value(teacher_dropdown.value),
                    'rent_type': clean_filter_value(rent_type_dropdown.value),
                }

                # منطق ویژه برای هزینه کلاس تقویتی و تیزهوشان (اصلاح اصلی!)
                if (operation_type_dropdown.value == 'withdraw' and
                    withdraw_type_dropdown.value in ['extra_class_cost', 'gifted_class_cost'] and
                    grade_dropdown.value):

                    print(f"حالت هزینه کلاس {'تقویتی' if withdraw_type_dropdown.value == 'extra_class_cost' else 'تیزهوشان'} فعال - پایه: {grade_dropdown.value}")

                    # اگر معلم خاصی انتخاب شده → teacher رو بفرست
                    if (teacher_dropdown.value and 
                        teacher_dropdown.value != '' and 
                        not str(teacher_dropdown.value).startswith("همه معلم")):

                        filters['teacher'] = teacher_dropdown.value
                        print(f"معلم خاص انتخاب شده: {teacher_dropdown.value}")

                    else:
                        # اگر "همه معلم‌های پایه ..." انتخاب شده → teacher رو حذف کن + position رو ست کن
                        if 'teacher' in filters:
                            del filters['teacher']
                        filters['position'] = f"teacher_grade{grade_dropdown.value}"
                        print(f"همه معلم‌های پایه {grade_dropdown.value} → استفاده از position: {filters['position']}")

                # منطق قبوض، کرایه، بیمه، حقوق → بدون تغییر (همون قبلی‌ها خوبه)
                # (می‌تونی همون کدهای قبلی رو نگه داری، فقط این بخش جدید رو جایگزین کن)

                # اصلاح خاص برای "همه عملیات" و "همه دانش‌آموزان"
                if filters.get('operation_type') == '':
                    filters['operation_type'] = None
                if filters.get('student') == '':
                    filters['student'] = None

                print("فیلترهای نهایی")
                for key, value in filters.items():
                    print(f"   {key}: {value}")

                # پاکسازی فیلترهای None
                clean_filters = {k: v for k, v in filters.items() if v is not None}

                print(f"ارسال درخواست به API با فیلترها: {clean_filters}")

                # ارسال به API
                result = fetch_filtered_transactions(clean_filters)

                if result.get('success'):
                    transactions = result.get('transactions', [])
                    nonlocal transactions_current
                    transactions_current = transactions
                    count = result.get('count', 0)
                    print(f"تعداد تراکنش‌های دریافت شده: {count}")

                    if count > 0:
                        table = create_dynamic_table(transactions, page, on_filter_click)

                        # خلاصه مالی — با فیلترهای درست
                        summary_filters = clean_filters.copy()
                        financial_summary = create_financial_summary(
                            filters.get('operation_type'),
                            summary_filters
                        )

                        filter_results_container.content = ft.Column([table, financial_summary], spacing=20)
                        print("خلاصه مالی با موفقیت ایجاد شد")
                    else:
                        # بدون نتیجه
                        filter_results_container.content = ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=COLORS["gray_400"]),
                                ft.Text("هیچ تراکنشی یافت نشد", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text("لطفاً فیلترهای دیگری را امتحان کنید", size=14, color=COLORS["gray_500"]),
                                ft.Container(height=16),
                                ft.FilledButton("بازنشانی فیلترها", icon=ft.Icons.REFRESH, on_click=lambda e: reset_filters())
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                            padding=60, alignment=ft.alignment.center
                        )

                else:
                    error_msg = result.get('error', 'خطای ناشناخته')
                    # نمایش خطا...

            except Exception as ex:
                print(f"خطای غیرمنتظره: {ex}")
                # نمایش خطا...

            finally:
                page.update()
                print("صفحه آپدیت شد")


        def reset_filters():
            """بازنشانی تمام فیلترها"""
            operation_type_dropdown.value = None
            transaction_type_dropdown.value = None
            withdraw_type_dropdown.value = None
            grade_dropdown.value = None
            classroom_dropdown.value = None
            student_dropdown.value = None
            start_date_field.value = jdatetime.datetime.now().replace(day=1).strftime("%Y-%m-%d")
            end_date_field.value = jdatetime.datetime.now().strftime("%Y-%m-%d")
            exam_type_dropdown.value = None
            category_dropdown.value = None
            position_dropdown.value = None
            employee_dropdown.value = None
            utility_type_dropdown.value = None
            teacher_dropdown.value = None
            
            filter_results_container.visible = False
            page.update()
            print("🔄 فیلترها بازنشانی شدند")

        # وصل کردن تابع به دکمه فیلتر
        apply_filter_btn.on_click = on_filter_click
        print_btn.on_click = on_print_click
        
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS["gradient_start"], COLORS["gradient_end"]]
            ),
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                controls=[
                    # هدر
                    ft.Container(
                        bgcolor=COLORS["white"],
                        padding=ft.padding.symmetric(vertical=20, horizontal=32),
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=COLORS["gray_600"],
                                            on_click=show_main
                                        ),
                                        create_icon(
                                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                                            COLORS["blue_600"],
                                            COLORS["blue_100"],
                                            24
                                        ),
                                        ft.Text(
                                            "حساب کتاب",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLORS["gray_900"]
                                        )
                                    ],
                                    spacing=12
                                )
                            ]
                        )
                    ),
                    
                    # محتوای اصلی
                    ft.Container(
                        expand=True,
                        padding=32,
                        content=ft.Column(
                            [
                                # عنوان و فیلترها
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            "گزارش‌های مالی", 
                                            size=28, 
                                            weight=ft.FontWeight.BOLD, 
                                            color=COLORS["white"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Text(
                                            "مشاهده تراکنش‌ها و آمار مالی", 
                                            size=16, 
                                            color=COLORS["blue_100"],
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        
                                        ft.Container(height=24),
                                        # فیلترها
                                            ft.Container(
                                                bgcolor=COLORS["white"],
                                                border_radius=12,
                                                padding=20,
                                                content=ft.Column([
                                                    # ردیف اول - فیلترهای آبشاری
                                                    ft.Row([
                                                        operation_type_dropdown,
                                                        ft.Container(width=8),
                                                        transaction_type_dropdown,
                                                        ft.Container(width=8),
                                                        withdraw_type_dropdown,
                                                        ft.Container(width=8),
                                                        grade_dropdown,
                                                        ft.Container(width=8),
                                                        classroom_dropdown,
                                                        ft.Container(width=8),
                                                        student_dropdown,
                                                        ft.Container(width=8),
                                                        exam_type_dropdown,
                                                        ft.Container(width=8),
                                                        category_dropdown,
                                                        ft.Container(width=8),
                                                        position_dropdown,
                                                        ft.Container(width=8),
                                                        employee_dropdown,
                                                        ft.Container(width=8),
                                                        utility_type_dropdown,
                                                        ft.Container(width=8),
                                                        rent_type_dropdown,  # 🔥 اینجا اضافه شد
                                                        ft.Container(width=8),
                                                        teacher_dropdown,
                                                    ], alignment=ft.MainAxisAlignment.START),
                                                    
                                                    ft.Container(height=12),
                                                    
                                                    # ردیف دوم - فیلترهای تاریخ
                                                    ft.Row([
                                                        ft.Text("بازه زمانی:", size=14, weight=ft.FontWeight.W_500),
                                                        ft.Container(width=12),
                                                        start_date_field,
                                                        ft.Text("تا", size=14),
                                                        end_date_field,
                                                        ft.Container(expand=True),
                                                        apply_filter_btn,
                                                        ft.Container(width=8),
                                                        print_btn  # ✅ اینجا دکمه پرینت اضافه شد
                                                    ], alignment=ft.MainAxisAlignment.START)
                                                ])
                                            )
                                    ], spacing=0)
                                ),
                                
                                ft.Container(height=32),

                                filter_results_container,
                                
                                ft.Container(height=32),
                                
                            ],
                            spacing=0
                        )
                    )
                ]
            )
        )

    # تابع به‌روزرسانی نمایش
    def update_display():
        page.clean()
        if current_page == "login":
            page.add(create_login_page())
        elif current_page == "main":
            page.add(create_main_page())
        elif current_page == "deposit_type":
            page.add(create_deposit_type_page())
        elif current_page == "withdraw_type":
            page.add(create_withdraw_type_page())
        elif current_page == "tuition_grade":
            page.add(create_tuition_grade_page())
        elif current_page == "class_selection":
            page.add(create_class_selection_page())
        elif current_page == "student_list":
            page.add(create_student_list_page())
        elif current_page == "tuition_payment":
            page.add(create_tuition_payment_page())
        elif current_page == "ledger":
            page.add(create_ledger_page())
        elif current_page == "cafeteria_sales":  
            page.add(create_cafeteria_sales_page()) 
        elif current_page == "breakfast_sales":
            page.add(create_breakfast_sales_page())
        elif current_page == "purchase":
            page.add(create_purchase_page())
        elif current_page == "rent":
            page.add(create_rent_page())
        elif current_page == "utility_type_selection":
            page.add(create_utility_type_selection_page())
        elif current_page == "utility_bill":
            page.add(create_utility_bill_page())
        elif current_page == "extra_class_grade":
            page.add(create_tuition_grade_page())
        elif current_page == "extra_class_selection":
            page.add(create_class_selection_page())
        elif current_page == "extra_class_student_list":
            page.add(create_student_list_page()) 
        elif current_page == "extra_class_payment":
            print("🎯 وارد case extra_class_payment شدیم")
            page.add(create_extra_class_payment_page())
        elif current_page == "gifted_class_grade":
            page.add(create_gifted_class_grade_page())
        elif current_page == "gifted_class_selection":
            page.add(create_class_selection_page()) 
        elif current_page == "gifted_class_student_list":
            page.add(create_student_list_page())
        elif current_page == "gifted_class_payment":
            page.add(create_gifted_class_payment_page())
        elif current_page == "exam_type":
            page.add(create_exam_type_page())
        elif current_page == "salary_position_selection":
            page.add(create_salary_position_selection_page())
        elif current_page == "salary_employee_list":
            page.add(create_salary_employee_list_page(selected_category))
        elif current_page == "salary_payment":
            page.add(create_salary_payment_page())
        elif current_page == "exam_grade_selection":
            page.add(create_exam_grade_selection_page(selected_exam_type))
        elif current_page == "exam_class_selection":
            page.add(create_exam_class_selection_page(selected_exam_type, selected_grade))
        elif current_page == "exam_student_list":
            page.add(create_exam_student_list_page(selected_exam_type, selected_grade, selected_classroom))
        elif current_page == "extra_class_withdraw_grade":
            page.add(create_extra_class_withdraw_grade_page())
        elif current_page == "teacher_list":
            page.add(create_teacher_list_page())
        elif current_page == "extra_class_teacher_payment":
            page.add(create_extra_class_teacher_payment_page())
        elif current_page == "insurance":
            page.add(create_insurance_position_selection_page())
        elif current_page == "insurance_employee_list":
            page.add(create_insurance_employee_list_page(selected_category))
        elif current_page == "insurance_payment":
            page.add(create_insurance_payment_page())
        elif current_page == "exam_payment":
            page.add(create_exam_payment_page())
        elif current_page == "petty_cash":
            page.add(create_petty_cash_page())
        elif current_page == "service":
            page.add(create_service_page())
        elif current_page == "rent_type_selection":
            page.add(create_rent_type_selection_page())
        elif current_page == "gym_rent":
            page.add(create_gym_rent_page())
        elif current_page == "gifted_class_withdraw_grade":
            page.add(create_gifted_class_withdraw_grade_page())
        elif current_page == "gifted_class_teacher_list":
            page.add(create_gifted_class_teacher_list_page())
        elif current_page == "gifted_class_teacher_payment":
            page.add(create_gifted_class_teacher_payment_page())
        page.update()

    # شروع برنامه
    update_display()

# اجرای برنامه
ft.app(target=main)