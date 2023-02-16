from django.db import models

# Create your models here.


class Detections(models.Model):
    detectionId = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    date_create = models.DateTimeField(auto_now_add=True)
    classification = models.CharField(max_length=50)
    mac = models.CharField(max_length=17)
    evidence = models.CharField(max_length=10485760)
