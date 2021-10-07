from django.core.paginator import Paginator, Page


class SwipingPaginator(Paginator):
    def _get_page(self, *args, **kwargs):
        return SwipingPage(*args, **kwargs)

class SwipingPage(Page):
    """
    Not a ideal but a temporary hack to always display ?page=1 in the url
    """
    def next_page_number(self):
        return 1
