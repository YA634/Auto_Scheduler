from django.db import models

# Create your models here.
class Task(models.Model):
  name = models.CharField(max_length=100)
  about = models.TextField(null=True, blank=True)
  quote_time = models.DurationField() #見積もり時間
  deadline = models.DateTimeField()
  accomplished = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name