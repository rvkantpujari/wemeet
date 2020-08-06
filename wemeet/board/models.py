from django.db import models
from django.contrib.auth.models import User
from globaltables.models import BoardType


class Board(models.Model):
	boardId = models.AutoField(primary_key=True)
	boardTitle = models.CharField(max_length=50)
	boardDescription = models.CharField(max_length=1000)
	boardImage = models.CharField(max_length=1000)
	createdBy = models.ForeignKey(User,
		on_delete=models.CASCADE)
	createdOn = models.DateTimeField()
	boardType = models.ForeignKey(BoardType,
		on_delete=models.CASCADE)
	isDeleted = models.BooleanField(default=0)

	def __str__(self):
		return self.boardTitle