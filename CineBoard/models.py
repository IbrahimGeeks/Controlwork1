from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name="жанр")

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    release_date = models.DateField(verbose_name="дата выхода")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies', verbose_name="жанр")
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="рейтинг")
    release_year = models.IntegerField(validators=[MinValueValidator(1888)], verbose_name="год выпуска")
    duration = models.PositiveIntegerField(verbose_name="Длительность, мин")
    budget = models.CharField(max_length=50, verbose_name="Бюджет")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies', verbose_name="автор")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments', verbose_name="Фильм")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return f"Комментарий от {self.user.username} к фильму {self.movie.title}"


class VipBooking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vip_booking', verbose_name="Пользователь")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='vip_bookings', verbose_name="Фильм")
    seat_number = models.PositiveIntegerField(verbose_name="Номер VIP места")
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VIP Место {self.seat_number} для {self.user.username} на фильм {self.movie.title}"