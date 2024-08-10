from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    document_type = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    received_date = models.DateField()
    deadline = models.DateField()

    def __str__(self):
        return self.name