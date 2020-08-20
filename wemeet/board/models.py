from django.db import models
from django.contrib.auth.models import User
from globaltables.models import BoardType, Role, AccessRights


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


class BoardMembers(models.Model):
	boardId = models.ManyToManyField(Board)
	user = models.ManyToManyField(User)
	addedOn = models.DateTimeField()
	role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
	isAdmin = models.BooleanField(default=False)
	isRemoved = models.BooleanField(default=False)
	isMuted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.boardId) + " " + str(self.user)


class Poll(models.Model):
	pollId = models.AutoField(primary_key=True)
	pollQuestion = models.CharField(max_length=200, null=False)
	createdOn = models.DateTimeField()
	deadLine = models.DateTimeField()
	createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	boardId = models.ForeignKey(Board, on_delete=models.CASCADE)
	isActive = models.BooleanField(default=1)

	def __str__(self):
		return self.pollQuestion

class Choices(models.Model):
	choiceId = models.AutoField(primary_key=True)
	choice = models.CharField(max_length=200, null=False)
	count = models.IntegerField(default=0)
	pollId = models.ForeignKey(Poll, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.pollId) + ": " + self.choice

class MemberPollChoice(models.Model):

	choiceId = models.ForeignKey(Choices, on_delete=models.CASCADE)
	pollId = models.ForeignKey(Poll, on_delete=models.CASCADE)
	user = models.ManyToManyField(User)


class BoardInvitation(models.Model):
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	user = models.ManyToManyField(User)
	status = models.CharField(max_length = 20)
	invitationTime = models.DateTimeField()
	responseTime = models.DateTimeField(null=True)


class BoardMembersAccessRights(models.Model):
	boardMember = models.ForeignKey(BoardMembers, on_delete=models.CASCADE)
	accessRight = models.ManyToManyField(AccessRights)

