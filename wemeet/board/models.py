from django.db import models
from django.contrib.auth.models import User
from globaltables.models import BoardType, Role


class Board(models.Model):
	boardId = models.AutoField(primary_key=True)
	boardTitle = models.CharField(max_length=50)
	boardDescription = models.CharField(max_length=1000)
	createdBy = models.ForeignKey(User,
		on_delete=models.CASCADE)
	createdOn = models.DateTimeField()
	boardType = models.ForeignKey(BoardType,
		on_delete=models.CASCADE)
	isDeleted = models.BooleanField(default=0)
	token = models.CharField(max_length=6, default='')

	def __str__(self):
		return self.boardTitle


class BoardMemberStatus(models.Model):
	statusId = models.AutoField(primary_key=True)
	status = models.CharField(max_length=20, null=False)

	def __str__(self):
		return self.status

class BoardMembers(models.Model):
	boardId = models.ManyToManyField(Board)
	user = models.ManyToManyField(User)
	addedOn = models.DateTimeField()
	roleId = models.ForeignKey(Role, on_delete=models.PROTECT)
	statusId = models.ForeignKey(BoardMemberStatus, on_delete=models.PROTECT)


	def __str__(self):
		return str(self.boardId) + " " + str(self.user)




