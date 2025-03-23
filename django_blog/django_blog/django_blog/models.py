from django.contrib import models
from .models import model_models

class model_models:

    title:modelsCharField(max_length=200)
    content:models.textfield()
    published_date: models.DateTmeFeld(auto_now_add=True)
    author:models.ForeignKey
