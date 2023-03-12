from django.db import models

from core.models import BaseModel


class Product(BaseModel):
    name = models.TextField(max_length=255)
