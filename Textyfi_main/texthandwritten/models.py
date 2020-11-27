from django.db import models
import os
# Create your models here.
class handwritten(models.Model):
    def update(instance,filename):
        PATH = 'media/text/boom.txt'
        # instance.inp_img.delete_all_created_images()
        os.remove(PATH)
        
        
        filename='{}.{}'.format('boom','txt')
        upload_to='text'
        
        # obj=OverwriteStorage;
        # obj.get_available_name(os.path.join(upload_to,filename))
        
        return os.path.join(upload_to,filename)
    textfile=models.FileField(upload_to=update)
class texthand(models.Model):
    sentence=models.CharField(max_length=10000)