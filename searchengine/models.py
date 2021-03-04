from django.db import models

# Create your models here.
class SearchInput(models.Model):
    job_search = models.CharField(max_length=100)
    location_search = models.CharField(max_length=50)
    def __str__(self):
            return self.question_text
        