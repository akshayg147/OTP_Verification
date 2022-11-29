from django.db import models

# Create your models here.
class Verify(models.Model):
    verified = models.BooleanField(default=False)
    otp = models.TextField(max_length=10)
    email = models.EmailField(default=None)

    def __str__(self):
        return self.email

