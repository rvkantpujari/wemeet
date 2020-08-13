from django.shortcuts import render
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Board as BoardModel, BoardMembers, BoardMemberStatus
from globaltables.models import BoardType, Role
from django.db.models import Q
from datetime import datetime, date, time
import random
import string




@method_decorator(login_required, name='dispatch')
class Home(View):
	
	def get(self, request):
		curr_user = request.user
		created = BoardModel.objects.filter(createdBy=curr_user)
		joined = BoardModel.objects.filter(boardmembers__user=curr_user)

		return render(request ,'board/index.html', {'boardsCreated':created,
			'boardsJoined':joined, 'user': curr_user,})



@method_decorator(login_required, name='dispatch')
class CreateBoard(View):

	def post(self, request):
		boardTitle = request.POST['boardTitle']
		boardDescription = request.POST['boardDescription']
		boardTypeId = request.POST['boardType']

		boardType = BoardType.objects.get(pk = boardTypeId)
		createdBy = request.user
		createdOn = datetime.now()

		token = self.generate_token(6)

		newBoard = BoardModel(
				boardTitle = boardTitle,
				boardDescription = boardDescription,
				createdOn = createdOn,
				boardType = boardType,
				createdBy = createdBy,
				token = token,
			)
		newBoard.save()

		return redirect('home')


	def generate_token(self, size):
		while(1):
			token = ''.join([random.choice(string.ascii_lowercase)for n in range(size)])                
			b = BoardModel.objects.filter(token = token)
			if not b:
				return token


@method_decorator(login_required, name='dispatch')
class JoinBoard(View):

	def post(self, request):
		token = request.POST['token']
		curr_user = request.user
		board = BoardModel.objects.filter(token = token).first()
		if board is None:
			print("board not found")
			return redirect('home') 
		if board.isDeleted:
			print("board not found")
			return redirect('home')
		if board.createdBy == curr_user:
			print("you cant join this board,your are the owner of this board")
			return redirect('home')

		isMember = BoardMembers.objects.filter(Q(user = curr_user),
				Q(boardId = board.boardId))

		if isMember:
			print("you have already joined this board.")
			return redirect('home')

		role = None
		if str(board.boardType) == 'Education':
			role = Role.objects.get(role = 'Student')
		else:
			role = Role.objects.get(role = 'Team Member')

		status = BoardMemberStatus.objects.get(status = 'active')

		joinBoard = BoardMembers(
				addedOn = datetime.now(),
				roleId = role,
				statusId =  status
			)
		
		joinBoard.save()
		joinBoard.boardId.add(board)
		joinBoard.user.add(curr_user)

		return redirect(request.META['HTTP_REFERER'])


@method_decorator(login_required, name='dispatch')
class BoardDetails(View):

	def get(self ,request, boardId):
		pass
		# print("boardId: ", boardId)
		# board = BoardModel.objects.filter(boardId = boardId).first()
		# curr_user = request.user
		# if not board:
		# 	return render(request, "404.html")

		# members = BoardMembers.objects.filter(boardId = board)
		# notMember = 1
		# for mem in members:
		# 	if mem.user.first() == request.user:
		# 		notMember = 0

		# if (board.createdBy != curr_user) and notMember:
		# 	return render(request, "404.html")

		# isOwner = 0
		# if board.createdBy == curr_user:
		# 	isOwner = 1
		# polls = Poll.objects.filter(boardId = board)
		# roles = Role.objects.filter(boardTypeId = board.boardType)
		# return render(request, 'board/boardDetails.html',
		# 	{'board':board, 'members':members, 'user': request.user,'polls':polls,
		# 	'isOwner': isOwner, 'roles': roles})



