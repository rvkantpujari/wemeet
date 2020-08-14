from .models import BoardType

def sections_processor(request):
    boardTypes = BoardType.objects.all()
    return {'boardTypes':boardTypes}