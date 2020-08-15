from board.models import BoardMembers, BoardMembersAccessRights, Board
from django import template
from django.db.models import Count
from django.db.models import Q
from globaltables.models import AccessRights

register = template.Library()

@register.filter(name='getUsersAccessRights')
def getUsersAccessRights(board, user):
	usersRights = {}
	boardMember = BoardMembers.objects.filter(Q(boardId=board.boardId), Q(user=user.id)).first()
	
	currentRights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
	allRights = AccessRights.objects.all()
	for right in allRights:
		usersRights[right.accessRightCode] = 0
	
	for right in currentRights:
		usersRights[right.accessRight.first().accessRightCode] = 1

	return usersRights


@register.filter(name='setBoardMember')
def setBoardMember(board, user):

	return BoardMembers.objects.filter(Q(boardId=board), Q(user=user)).first()


# @register.filter(name='canCreatePost')
# def canCreatePost(boardMember):
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "CREATE_POST":
# 			return True
# 	return False


# @register.filter(name='canViewPost')
# def canViewPost(boardMember):
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "VIEW_POST":
# 			return True
# 	return False


# @register.filter(name='canCreatePoll')
# def canCreatePoll(boardMember):
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "CREATE_POLL":
# 			return True
# 	return False


# @register.filter(name='canGiveVote')
# def canGiveVote(boardMember, isOwner):
# 	if isOwner:
# 		return False
# 	print(boardMember)
# 	print(isOwner)
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "GIVE_VOTE":
# 			return True
# 	return False


# @register.filter(name='canViewPollResult')
# def canViewPollResult(boardMember, isOwner):
# 	if isOwner:
# 		return True
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "VIEW_POLL_RESULT":
# 			return True
# 	return False


# @register.filter(name='canInvitePeople')
# def canInvitePeople(boardMember):
# 	rights = BoardMembersAccessRights.objects.filter(boardMember=boardMember.id)
# 	for right in rights:
# 		if right.accessRight.first().accessRightCode == "INVITE_PEOPLE":
# 			return True
# 	return False

