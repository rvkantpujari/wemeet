from django.views import View
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from .models import Board as BoardModel, BoardMembers, BoardMemberStatus
from board.models import Board as BoardModel, BoardMembers, BoardMembersAccessRights
from .models import Post as Post,Post_Attachments,Post_Comment
from globaltables.models import BoardType, Role, AccessRights
from django.db.models import Q
from datetime import datetime, date, time
import random
import string
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import generic



@method_decorator(login_required, name='dispatch')
class CreatePost(View):

	def post(self, request,boardId):
		bid = boardId
		print(bid)
		postTitle = request.POST.get('postTitle')
		postDescription = request.POST.get('postDescription')
		print(postTitle )
		print(postDescription)
		createdOn = datetime.now()
		createdBy = request.user
		boardId = BoardModel.objects.get(boardId = boardId)
		print(boardId)

		newPost = Post(
				postTitle = postTitle,
				postDescription = postDescription,
				createdOn = createdOn,
				createdBy = createdBy,
				boardId = boardId,
			)
		newPost.save()


		postId = newPost.postId

		
		request_file = request.FILES['postAttachment'] if 'postAttachment' in request.FILES else None
		if request_file:
			print(request_file)

			print(request.POST)

			postAttachment = str(postId) + "_" +request.FILES['postAttachment'].name
			# postAttachment = request.POST.get['postAttachment']

			
			
			postAttachmentPath = '/media/postattachment/'+ str(bid) + "/" + str(postAttachment)

			print(postAttachmentPath)


			newpath = 'media/postattachment/'+ str(bid) + "/" 
			#path = os.path.join(settings.STATIC_DIR, newpath) 
			print(settings.STATIC_DIR +"/" + newpath)
			try:
			# if not os.path.exists(settings.STATIC_DIR +"/" + newpath):
				os.makedirs(settings.STATIC_DIR +"/" + newpath)
			# else:
			except OSError as error: 
			# 	print("Directory '%s' can not be created" % directory)
				print("not created")
			
			

			storeAt = os.path.join(settings.STATIC_DIR, newpath)

			fs = FileSystemStorage(storeAt)

			file = fs.save(postAttachment, request_file)

			newPostAttachment = Post_Attachments(
				postId= newPost,
				postAttachment = postAttachmentPath,
			)
			newPostAttachment.save()

			

		return redirect(request.META['HTTP_REFERER'])

# Create your views here.

@method_decorator(login_required, name='dispatch')
class ViewPost(View):
	def get(self, request,postId):
		curr_user = request.user
		post = Post.objects.filter(postId = postId).first()
		board = BoardModel.objects.get(pk = post.boardId.boardId)
		boardMember = BoardMembers.objects.filter(
			Q(boardId=board.boardId), Q(user=curr_user.id)).first()
		viewRight = AccessRights.objects.get(accessRightCode='VIEW_POST')
		canVeiwPost = BoardMembersAccessRights.objects.filter(
			Q(boardMember=boardMember.id), Q(accessRight=viewRight.id))

		if not canVeiwPost:
			return render(request, "404.html")

		postAttachment = Post_Attachments.objects.filter(postId = postId).first()
		comments = Post_Comment.objects.filter(postId = postId)
		
		return render(request, 'board/postDetails.html',
			{'postobj':post , 'comments':comments,'postatt':postAttachment,
				'board': board, 'user': curr_user})

@method_decorator(login_required, name='dispatch')
class DeletePost(View):
	def get(self, request,postId):
		print(postId)
		u = Post.objects.get(pk=postId)
		boardId = u.boardId.boardId
		u.delete()
		# return ViewPost.as_view()(request,boardId)
		return redirect('board_details',boardId=boardId)


@method_decorator(login_required, name='dispatch')
class AddComment(View):

	def post(self, request,postId):
		commentDescription = request.POST.get('commentdes')
		createdOn = datetime.now()
		createdBy = request.user
		postId = Post.objects.get(postId = postId)
		
		newComment = Post_Comment(
				commentDescription = commentDescription,
				createdOn = createdOn,
				createdBy = createdBy,
				postId = postId,
			)
		newComment.save()
		return redirect(request.META['HTTP_REFERER'])

@method_decorator(login_required, name='dispatch')
class EditPost(View):
	def get(self, request,postId):
		# board = BoardModel.objects.filter(boardId = boardId).first()
		post = Post.objects.filter(postId = postId).first()
		postAttachment = Post_Attachments.objects.filter(postId = postId).first()
		# print(postAttachment);	
		
		return render(request, 'board/EditPost.html',{'postobj':post , 'postatt':postAttachment,})

	def post(self, request,postId):
		u = Post.objects.get(pk=postId)
		bid = u.boardId.boardId
		# q = Post.objects.get(pk=postId)
		# k = BoardModel.objects.get(boardTitle = q.boardId)
		# bid = k.pk
		# bid = q.boardId
		print(bid)
		# print(bid)
		postTitle = request.POST.get('postTitle')
		postDescription = request.POST.get('postDescription')
		print(postTitle)
		print(postDescription)
		Post.objects.filter(pk=postId).update(
				postTitle = postTitle,
				postDescription = postDescription,)

		request_file = request.FILES['postAttachment'] if 'postAttachment' in request.FILES else None
		if request_file:
			print(request_file)
			print(request.POST)
			postAttachment = str(postId) + "_" +request.FILES['postAttachment'].name
			postAttachmentPath = '/media/postattachment/'+ str(bid) + "/" + str(postAttachment)

			print(postAttachmentPath)


			newpath = 'media/postattachment/'+ str(bid) + "/" 
			print(settings.STATIC_DIR +"/" + newpath)
			try:
				os.makedirs(settings.STATIC_DIR +"/" + newpath)
			except OSError as error: 
				print("not created")
			
			

			storeAt = os.path.join(settings.STATIC_DIR, newpath)

			fs = FileSystemStorage(storeAt)

			file = fs.save(postAttachment, request_file)

			Post_Attachments.objects.filter(postId = postId).update(
				postAttachment = postAttachmentPath
				
				)
			
		return redirect(request.META['HTTP_REFERER'])

@method_decorator(login_required, name='dispatch')
class EditComment(View):
	def post(self, request,postCommentId):

		# c = Post_Comment.objects.get(pk=PostCommentId)
		commentDescription = request.POST.get('commentDescription')
		print(commentDescription)
		Post_Comment.objects.filter(pk=postCommentId).update(
				commentDescription = commentDescription,)
		return redirect(request.META['HTTP_REFERER'])

@method_decorator(login_required, name='dispatch')
class DeleteComment(View):
	def get(self, request,postCommentId):
		print(postCommentId)
		u = Post_Comment.objects.filter(pk=postCommentId).delete()

		return redirect(request.META['HTTP_REFERER'])