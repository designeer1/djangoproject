

# Create your models here.
from django.db import models

class UserQuery(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.query_text[:50]} - Response: {self.response_text[:50]}"

class ChatbotResponse(models.Model):
    intent = models.CharField(max_length=255)
    response_text = models.TextField()

    def __str__(self):
        return f"Intent: {self.intent}"

class SystemLog(models.Model):
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} - {self.status} at {self.timestamp}"
