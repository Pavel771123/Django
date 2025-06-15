from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model


def translit_to_eng(s: str)-> str:
    d = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
    'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
    'я': 'ya',}

    return "".join(map(lambda x:d[x] if d.get(x, False) else x , s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)
    


class Women(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255,verbose_name='Заголовок')
    content = models.TextField(blank=True,verbose_name='Биография')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", default=None,blank=True,null=True, verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True,verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True,verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]),x[1]), Status.choices)),
                                        default = Status.DRAFT,verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,related_name='posts',verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',verbose_name='Теги')
    husband= models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True,related_name='wuman',verbose_name='Супруг')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    # def save(self,*args,**kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args,**kwargs )


    class Meta:
        ordering = ['-time_create']  # сортировка по убыванию даты
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины" 

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,verbose_name='Slug')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug':self.slug})
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class TagPost(models.Model):
    tag = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':self.slug})
    

    def __str__(self):
        return self.tag


class Husband(models.Model):
    name= models.CharField(max_length=255)
    age= models.IntegerField(null=True)
    m_count = models.IntegerField(default=0,blank=True)
    def __str__(self):
        return self.name
    
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')



# women =['Анастасия Эшли',
# 'Шакира',
# 'Кэтти Перри',
# 'Бейонсе',
# 'Рианна',
# 'Ума Турман',
# 'Екатерина Гусева',
# 'Ариана Гранде',
# 'Дженнифер Лоуренс',
# 'Марго Робби',]