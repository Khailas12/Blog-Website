from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class TheBlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=120, blank=False)
    content = models.TextField(blank=False)
    author = models.TextField(blank=False)

    def __str__(self):
        return self.title