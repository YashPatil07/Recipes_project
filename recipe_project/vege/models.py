from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    # on_delete=cascade :- if incase user get deleted then delete relevant records of that user
    #on_delete =set_null :- if incase user get deleted then relevant records of that user get null
    # on_delete =set_default
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null= True,blank=True)
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.TextField()
    recipe_image=models.ImageField(upload_to="recipe_images")