from django.contrib import admin
from .models import Student, Order

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name', 'limit')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'theme', 'doc_type')