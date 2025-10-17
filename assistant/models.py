from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=128)
    limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.username
    

class Order(models.Model):
    Type_choices = (
        ('prestation', 'prezentatsiya'),
        ('referat', 'referat')
    )
    Status_choices = (
        ('process', 'jarayonda'),
        ('done', 'tayyorlangan'),
        ('canceled', 'bekor qilingan')
    )
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='user_orders')
    subject = models.CharField(max_length=128)
    theme = models.CharField(max_length=256)
    doc_type = models.CharField(max_length=12, choices=Type_choices)
    status = models.CharField(max_length=15, choices=Status_choices, default='progcess')

    def __str__(self):
        return f"{self.id} - {self.user}"


