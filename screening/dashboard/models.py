from django.db import models
from django.utils import timezone 

# Create your models here.
class Stock(models.Model): 
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(db_index=True,max_length=200)
    created_date = models.DateTimeField(auto_now_add=True) 
    published_date = models.DateTimeField(auto_now=True) 

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]
    def publish(self): 
        self.published_date = timezone.now() 
        self.save() 

    def __str__(self): 
        return self.title