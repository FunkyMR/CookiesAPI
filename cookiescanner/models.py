from django.db import models

class CookieData(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    cookies = models.JSONField()
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
