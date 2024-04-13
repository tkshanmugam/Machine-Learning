from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class onlineFoodPreModel(models.Model):

    Age    = models.IntegerField()
    Gender = models.IntegerField()
    Marital_Status = models.IntegerField()
    Monthly_Income = models.IntegerField()
    Educational_Qualification = models.IntegerField()
    Family_Size = models.IntegerField()
    Feedback    = models.IntegerField()
