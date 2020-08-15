from django import template
from board.models import BoardMembersAccessRights
from globaltables.models import AccessRights
from django.db.models import Q

register = template.Library()

@register.filter(name='hasAccess')
def hasAccess(currentAccesses, right):
	for accesse in currentAccesses:
		if accesse.accessRight.first().accessRightCode == right.accessRightCode:
			return True
	return False


@register.filter(name='currentAccesses')
def currentAccesses(boardMember):
	return BoardMembersAccessRights.objects.filter(boardMember = boardMember.id)


