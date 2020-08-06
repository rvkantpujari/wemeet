from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBoard.as_view(), name='create_board'),
    # path('show_all/', views.ShowBoards.as_view(), name='show_all_board'),
    # path('edit/<int:boardId>', views.EditBoard.as_view(), name='edit_board'),
]