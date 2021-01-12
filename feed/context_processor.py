from .my_forms import CreatePostForm
from django.contrib.auth.decorators import login_required


def add_context(request):
    form = None
    if request.user.is_authenticated:
        form = CreatePostForm()
    return {'post_form': form}
   