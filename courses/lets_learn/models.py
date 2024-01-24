from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Course(models.Model):
    course_name = models.CharField(max_length = 200)
    course_description = RichTextField()
    is_premium = models.BooleanField(default = False)
    course_image = models.ImageField(upload_to = 'course')
    slug = models.SlugField(blank = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.course_name
    

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    course_module_name = models.CharField(max_length = 100)
    course_description = RichTextField()
    video_url = models.URLField(max_length = 300)
    can_view = models.BooleanField(default = False)