from django.shortcuts import render
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Board as BoardModel




@method_decorator(login_required, name='dispatch')
class Home(View):
	
	def get(self, request):
		uid = request.user.id
		user = User.objects.get(pk=uid)
		uboards = BoardModel.objects.filter(createdBy=user)

		return render(request ,'board/index.html', {'boards':uboards})




@method_decorator(login_required, name='dispatch')
class CreateBoard(View):

	def get(self, request):
		fm = CreateBoardForm()
		boardTypes = BoardType.objects.all()

		return render(request, 'board/creatBoard.html', {'form':fm,
			'boardTypes': boardTypes})

	def post(self, request):
		boardTitle = request.POST['boardTitle']
		boardDescription = request.POST['boardDescription']
		boardTypeId = request.POST['boardType']

		boardType = BoardType.objects.get(pk = boardTypeId)
		createdBy = request.user
		createdOn = datetime.now()
		boardImage = str(boardType)+'.png'

		print(boardTitle)
		print(boardDescription)
		print(boardTypeId)

		newBoard = BoardModel(
				boardTitle = boardTitle,
				boardDescription = boardDescription,
				createdOn = createdOn,
				boardType = boardType,
				createdBy = createdBy,
				boardImage = boardImage,
			)
		newBoard.save()

		fm = CreateBoardForm()
		boardTypes = BoardType.objects.all()
		return render(request, 'board/creatBoard.html', {'form':fm,
			'boardTypes': boardTypes})		





