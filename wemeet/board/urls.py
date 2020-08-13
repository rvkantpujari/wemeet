from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBoard.as_view(), name='create_board'),
    path('join_board/', views.JoinBoard.as_view(), name='join_board'),
    path('board_details/<int:boardId>', views.BoardDetails.as_view(), name='board_details'),
]