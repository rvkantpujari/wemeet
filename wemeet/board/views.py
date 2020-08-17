from django.shortcuts import render
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Board as BoardModel, BoardMembers, BoardMemberStatus
from .models import Poll, Choices, MemberPollChoice, BoardInvitation,BoardMembersAccessRights
from post.models import Post 
from globaltables.models import BoardType, Role, DefaultRole, AccessRights
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
		pendingInvitations = BoardInvitation.objects.filter(Q(user=curr_user),
			Q(status='pending'))
		
		return render(request ,'board/index.html', {'boardsCreated':created,
			'boardsJoined':joined, 'user': request.user,
			'pendingInvitations': pendingInvitations})



@method_decorator(login_required, name='dispatch')
class CreateBoard(View):

	def post(self, request):
		boardTitle = request.POST['boardTitle']
		boardDescription = request.POST['boardDescription']
		boardTypeId = request.POST['boardType']
		curr_user = request.user

		boardType = BoardType.objects.get(pk = boardTypeId)
		createdBy = curr_user
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

		role = Role.objects.filter(Q(boardTypeId=boardType), Q(role="Admin")).first()
		status = BoardMemberStatus.objects.get(status = 'active')

		joinBoard = BoardMembers(
				addedOn = datetime.now(),
				statusId =  status
			)

		joinBoard.save()
		joinBoard.boardId.add(newBoard)
		joinBoard.user.add(curr_user)
		joinBoard.roleId.add(role)

		for access in AccessRights.objects.all():
			giveAccessRight = BoardMembersAccessRights(boardMember = joinBoard)
			giveAccessRight.save()
			giveAccessRight.accessRight.add(access)

		return redirect('home')


	def generate_token(self, size):
		while(1):
			token = ''.join([random.choice(string.ascii_lowercase)for n in range(size)])                
			b = BoardModel.objects.filter(token = token)
			if not b:
				return token


@method_decorator(login_required, name='dispatch')
class JoinBoard(View):
	defaultAccessRights = []

	def __init__(self):
		defaultAccessCodes = ['VIEW_POST', 'GIVE_VOTE', 'VIEW_POLL_RESULT', 'POST_COMMENT']

		for code in defaultAccessCodes:
			accessRight = AccessRights.objects.get(accessRightCode = code)
			self.defaultAccessRights.append(accessRight)

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

		role = DefaultRole.objects.filter(boardType = board.boardType).first()
		
		status = BoardMemberStatus.objects.get(status = 'active')

		joinBoard = BoardMembers(
				addedOn = datetime.now(),
				statusId =  status
			)
		
		joinBoard.save()
		joinBoard.boardId.add(board)
		joinBoard.user.add(curr_user)
		joinBoard.roleId.add(role)

		for access in self.defaultAccessRights:
			giveAccessRight = BoardMembersAccessRights(boardMember = joinBoard)
			giveAccessRight.save()
			giveAccessRight.accessRight.add(access)

		return redirect(request.META['HTTP_REFERER'])


@method_decorator(login_required, name='dispatch')
class BoardDetails(View):

	def get(self ,request, boardId):

		print("boardId: ", boardId)
		board = BoardModel.objects.filter(boardId = boardId).first()
		curr_user = request.user
		if not board:
			return render(request, "404.html")

		members = BoardMembers.objects.filter(boardId = board)
		notMember = 1
		for mem in members:
			if mem.user.first() == request.user:
				notMember = 0

		if (board.createdBy != curr_user) and notMember:
			return render(request, "404.html")

		isOwner = 0
		if board.createdBy == curr_user:
			isOwner = 1

		polls = Poll.objects.filter(boardId = board)
		roles = Role.objects.filter(boardTypeId = board.boardType)
		posts = Post.objects.filter(boardId = board)
		
		return render(request, 'board/boardDetails.html',
			{'board':board, 'members':members, 'user': curr_user,'polls':polls,
			'isOwner': isOwner,'posts':posts, 'roles': roles})


@method_decorator(login_required, name='dispatch')
class CreatePoll(View):

	def post(self, request, boardId):
		pollQuestion = request.POST['pollQuestion']
		deadlineDate = request.POST['deadlineDate']
		deadlineTime = request.POST['deadlineTime']

		year,month,day = deadlineDate.split('-')
		hour, minute = deadlineTime.split(':')

		deadLine = datetime.combine(date(int(year),int(month),int(day)), 
                          time(int(hour), int(minute)))
		curr_user = request.user
		board = BoardModel.objects.get(boardId = boardId)

		poll = Poll(
				pollQuestion = pollQuestion,
				createdOn = datetime.now(),
				deadLine = deadLine,
				createdBy = curr_user,
				boardId = board
			)
		poll.save()

		i=1
		while(1):
			ch = str("choice"+str(i))
			if request.POST.get(ch):
				ch = request.POST.get(ch)
				choice = Choices(
						choice = ch,
						pollId=  poll,
					)
				choice.save()
			else:
				break
			i += 1

		return redirect(request.META['HTTP_REFERER'])


@method_decorator(login_required, name='dispatch')
class SavePollVote(View):

	def get(self, request):
		choiceId = request.GET.get('choiceId')
		choice = Choices.objects.get(pk = choiceId)
		poll = Poll.objects.get(pk = choice.pollId.pollId)
		curr_user = request.user
		votedFor = MemberPollChoice.objects.filter(Q(pollId = poll), Q(user = curr_user)).first()
		print(choice)
		print(poll)
		print(votedFor)

		if votedFor:
			oldChoice = votedFor.choiceId
			votedFor.choiceId = choice
			choice.count += 1
			oldChoice.count -= 1
			votedFor.save()
			oldChoice.save()
			choice.save()
			print(oldChoice)
		else:
			saveVote = MemberPollChoice(pollId = poll, choiceId = choice)
			saveVote.save()
			saveVote.user.add(curr_user)
			choice.count += 1
			choice.save()
			print("first vote")

		return HttpResponse("success")


@method_decorator(login_required, name='dispatch')
class InvitePeople(View):

	def post(self, request):
		email = request.POST.get('email')
		boardId = request.POST.get('boardId')
		curr_user = request.user
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		if not user:
			print("user DoesNotExist")
			return HttpResponse("success")
		board = BoardModel.objects.filter(pk = boardId).first()
		if board.createdBy == user:
			print("you cant join this board,your are the owner of this board")
			return HttpResponse("success")
		isMember = BoardMembers.objects.filter(Q(user = user),
				Q(boardId = boardId))
		if isMember:
			print("user has already joined this board.")
			return HttpResponse("success")
		print(board)
		roleId = request.POST.get('roleId')
		role = Role.objects.get(roleId = roleId)
		print(roleId)
		invite = BoardInvitation(
				board = board,
				role = role,
				status = 'pending',
				invitationTime = datetime.now()
			)
		invite.save()
		invite.user.add(user)
		invite.save()
		return HttpResponse("success")

@method_decorator(login_required, name='dispatch')
class AcceptBoardInvitation(View):

	def post(self, request, boardInvitationId):
		print(boardInvitationId)
		try:
			invitation = BoardInvitation.objects.get(pk = boardInvitationId)
		except invitation.DoesNotExist:
			invitation = None
		try:
			board = BoardModel.objects.get(pk = invitation.board.boardId)
		except board.DoesNotExist:
			board = None
		curr_user = request.user
		if board is None:
			print("board not found")
			return HttpResponse('success') 
		if board.isDeleted:
			print("board not found")
			return HttpResponse('success')

		isMember = BoardMembers.objects.filter(Q(user = curr_user),
				Q(boardId = board.boardId))

		if isMember:
			print("you have already joined this board.")
			invitation.status = 'accepted'
			invitation.save()
			return HttpResponse('success')

		role = Role.objects.get(pk = invitation.role.roleId)
		status = BoardMemberStatus.objects.get(status = 'active')

		joinBoard = BoardMembers(
				addedOn = datetime.now(),
				statusId =  status
			)
		
		joinBoard.save()
		joinBoard.boardId.add(board)
		joinBoard.user.add(curr_user)
		joinBoard.roleId.add(role)

		invitation.status = 'accepted'
		invitation.save()

		return HttpResponse('success')

@method_decorator(login_required, name='dispatch')
class RejectBoardInvitation(View):
	def post(self, request, boardInvitationId):
		print(boardInvitationId)
		try:
			invitation = BoardInvitation.objects.get(pk = boardInvitationId)
		except invitation.DoesNotExist:
			invitation = None
		try:
			board = BoardModel.objects.get(pk = invitation.board.boardId)
		except board.DoesNotExist:
			board = None
		curr_user = request.user
		if board is None:
			print("board not found")
			return HttpResponse('success')
		if board.isDeleted:
			print("board not found")
			return HttpResponse('success')

		invitation.status = 'rejected'
		invitation.save()

		return HttpResponse('success')


@method_decorator(login_required, name='dispatch')
class PeopleBoardDetails(View):
	def get(self, request, boardMemberId):
		try:
			boardMember = BoardMembers.objects.get(pk = boardMemberId)
		except boardMember.DoesNotExist:
			boardMember = None
		accessRights = AccessRights.objects.all()
		board = BoardModel.objects.filter(boardId = boardMember.boardId.first().boardId).first()
		curr_user = request.user
		return render(request, 'board/peopleBoardDetails.html',
			{'boardMember':boardMember, 'accessRights':accessRights,
			'board':board, 'user':curr_user})


@method_decorator(login_required, name='dispatch')
class RevokeAccessRight(View):

	def post(self, request):
		accessRightId = request.POST['accessRightId']
		boardMemberId = request.POST['boardMemberId']
		
		try:
			obj = BoardMembersAccessRights.objects.filter(
					boardMember = boardMemberId,
					accessRight = accessRightId
				).first().delete()

		except:
			return HttpResponse('success')
		return HttpResponse('success')


@method_decorator(login_required, name='dispatch')
class GrantAccessRight(View):

	def post(self, request):
		accessRightId = request.POST['accessRightId']
		boardMemberId = request.POST['boardMemberId']

		try:
			right = AccessRights.objects.get(pk = accessRightId)
			boardMember = BoardMembers.objects.get(pk = boardMemberId)

			giveAccessRight = BoardMembersAccessRights(boardMember = boardMember)
			giveAccessRight.save()
			giveAccessRight.accessRight.add(right)
		except BoardMembersAccessRights.DoesNotExist:
			return HttpResponse('success')
		return HttpResponse('success')



