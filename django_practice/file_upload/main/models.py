from django.db import models
from django.db.models.signals import post_delete


# Create your models here.
class UploadFile(models.Model):
    file = models.FileField(upload_to='files/')

#    def delete(self, *args, **kwargs):
#        # You have to prepare what you need before delete the model
#        storage, path = self.file.storage, self.file.path
#        # Delete the model before the file
#        super(UploadFile, self).delete(*args, **kwargs)
#        # Delete the file after the model
#        storage.delete(path)
