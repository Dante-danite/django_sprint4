from django.conf import settings
from django.core.paginator import Paginator

def paginate_list(objects, page):
    paginator = Paginator(objects, settings.POSTS_LIMIT)
    page_obj = paginator.get_page(page)
    return page_obj