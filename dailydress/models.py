from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Style(models.Model):
    id_style = models.AutoField(primary_key=True, null=False, unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_for_style = models.DateField(null=False, default=(timezone.now().date()))


    class Meta:
        managed = True
        db_table = 'style'

class Cloth(models.Model):
    id_cloth = models.AutoField(primary_key=True, null=False, unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(null=False, max_length=50)
    sub_type = models.CharField(null=True, max_length=50)
    color = models.CharField(null=False, max_length=20)
    temp_range = ArrayField(models.IntegerField(), blank=True, default=list, size=2)
    weather = models.CharField(null=False, max_length=20)
    like_rate = models.IntegerField(default=3)
    picture_url = models.CharField(null=True, max_length=50)


    class Meta:
        managed = True
        db_table = 'cloth'

class StyleCloth(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='style_cloth')
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='cloth')

    class Meta:
        managed = True
        db_table = 'style_cloth'
        constraints = [
            models.UniqueConstraint(fields=['id_style', 'id_cloth'], name='unique_style_cloth')
        ]
