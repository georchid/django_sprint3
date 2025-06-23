from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Добавлено")
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано",
                                       help_text=(
                                           "Снимите галочку, "
                                           "чтобы скрыть публикацию."
                                       ))

    class Meta:
        abstract = True


User = get_user_model()


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=64, unique=True,
                            verbose_name="Идентификатор",
                            help_text=(
                                "Идентификатор страницы для URL; "
                                "разрешены символы латиницы, цифры, "
                                "дефис и подчёркивание."
                            )
                            )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Post(BaseModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(verbose_name="Дата и время публикации",
                                    help_text=(
                                        "Если установить дату и время в "
                                        "будущем — можно делать отложенные "
                                        "публикации.")
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name="Автор публикации")
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='posts',
                                 verbose_name='Местоположение')
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 on_delete=models.SET_NULL,
                                 related_name='posts',
                                 null=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
