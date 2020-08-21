from django import template
from board.models import BoardMembers, MemberPollChoice
from django.db.models import Count
from django.db.models import Q

register = template.Library()

@register.filter(name='totalBoardMembers')
def totalBoardMembers(board):
	members = BoardMembers.objects.filter(boardId = board).count()
	# print("count: ",str(members))
	return members



@register.filter(name='memberRole')
def memberRole(board, user):
	role = BoardMembers.objects.get(boardId = board, user = user).role
	print("role: ",role)
	return role



@register.filter(name='votedFor')
def votedFor(choice, user):
	isVoted = MemberPollChoice.objects.filter(Q(choiceId = choice), Q(user = user)).first()
	if isVoted:
		return 1
	else:
		return 0



@register.filter(name='isUserNotAdmin')
def isUserNotAdmin(board, user):
	try:
		boardMember = BoardMembers.objects.filter(Q(boardId=board),
			Q(user=user), Q(isAdmin=True)).first()
	except:
		print("user not found in boardMember!!")
		return True
	if boardMember:
		return False
	else:
		return True
