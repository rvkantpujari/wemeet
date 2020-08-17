from django.urls import path
from . import views

urlpatterns = [
    path('create_post/<int:boardId>', views.CreatePost.as_view(), name='create_post'),
    path('view_post/<int:postId>', views.ViewPost.as_view(), name='view_post'),
	path('delete_post/<int:postId>', views.DeletePost.as_view(), name='delete_post'),
	path('add_comment/<int:postId>', views.AddComment.as_view(), name='add_comment'),
	path('edit_post/<int:postId>', views.EditPost.as_view(), name='edit_post'),
	path('edit_comment/<int:postCommentId>', views.EditComment.as_view(), name='edit_comment'),
	path('delete_comment/<int:postCommentId>', views.DeleteComment.as_view(), name='delete_comment'),

]

