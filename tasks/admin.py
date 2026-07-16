from django.contrib import admin
from .models import Task

# Register your models here.
# class TaskAdmin(admin.ModelAdmin):
#   name = models.CharField(max_length=100)
#   about = models.TextField(null=True, blank=True)
#   quote_time = models.DurationField() #見積もり時間
#   deadline = models.DateTimeField()
#   accomplished = models.BooleanField(default=False)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)
admin.site.register(Task)