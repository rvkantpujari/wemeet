from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class BoardType(models.Model):
	boardTypeId = models.AutoField(primary_key=True)
	boardType = models.CharField(max_length=50)

	def __str__(self):
		return str(self.boardType)


class Role(models.Model):
	boardTypeId = models.ForeignKey(BoardType, on_delete=models.CASCADE)
	roleId = models.AutoField(primary_key=True)
	role = models.CharField(max_length=20)

	def __str__(self):

		return self.role


class DefaultRole(models.Model):
	boardType = models.OneToOneField(BoardType, on_delete=models.CASCADE)
	role = models.OneToOneField(Role, on_delete=models.CASCADE)


