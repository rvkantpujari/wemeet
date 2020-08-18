from django.db import models
from django.contrib.auth.models import User
from globaltables.models import BoardType, Role
from board.models import Board, BoardMembers,BoardMemberStatus
from datetime import datetime

class Post(models.Model):
	postId = models.AutoField(primary_key=True)
	postTitle = models.CharField(max_length=50)
	postDescription = models.CharField(max_length=1000)
	createdOn = models.DateTimeField(default = datetime.now)
	createdBy = models.ForeignKey(User,
		on_delete=models.CASCADE)
	boardId = models.ForeignKey(Board,
		on_delete=models.CASCADE)

	# def __str__(self):
	# 	return self.boardTitlefrom django.db import models

# Create your models here.

class Post_Attachments(models.Model):
	postId = models.ForeignKey(Post,
		on_delete=models.CASCADE)
	postAttachment = models.CharField(max_length=1000, null=True)

# Create your models here.

class Post_Comment(models.Model):
	postCommentId = models.AutoField(primary_key=True)
	commentDescription = models.CharField(max_length=1000)
	createdOn = models.DateTimeField(default = datetime.now)
	createdBy = models.ForeignKey(User,
		on_delete=models.CASCADE)
	postId = models.ForeignKey(Post,
		on_delete=models.CASCADE)