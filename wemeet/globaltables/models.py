from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class BoardType(models.Model):
	boardTypeId = models.IntegerField(primary_key=True, validators=[
            MaxValueValidator(9),
            MinValueValidator(1)
        ])
	boardType = models.CharField(max_length=50)

	def __str__(self):
		return str(self.boardType)


class Role(models.Model):
	boardTypeId = models.ForeignKey(BoardType, on_delete=models.CASCADE)
	roleId = models.IntegerField(primary_key=True, validators=[
            MaxValueValidator(99),
            MinValueValidator(1)
        ])
	role = models.CharField(max_length=20)
