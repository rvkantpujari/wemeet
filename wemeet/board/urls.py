from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBoard.as_view(), name='create_board'),
    path('join_board/', views.JoinBoard.as_view(), name='join_board'),
    path('board_details/<int:boardId>', views.BoardDetails.as_view(), name='board_details'),
	path('create_poll/<int:boardId>', views.CreatePoll.as_view(), name='create_poll'),
	path('save_poll_vote', views.SavePollVote.as_view(), name='save_poll_vote'),
	path('invite_people', views.InvitePeople.as_view(), name='invite_people'),
	path('board_invitation/accept/<int:boardInvitationId>', views.AcceptBoardInvitation.as_view(),
		name='accept_invitation'),
	path('board_invitation/reject/<int:boardInvitationId>', views.RejectBoardInvitation.as_view(),
		name='reject_invitation'),
    # path('edit/<int:boardId>', views.EditBoard.as_view(), name='edit_board'),
]