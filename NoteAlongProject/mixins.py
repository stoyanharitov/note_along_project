from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect

class ReadOnlyMixin:
    read_only_fields = []

    def make_fields_readonly(self):
        for field_name in self.read_only_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_fields_readonly()



class PaginationMixin:
    def get(self, request, *args, **kwargs):
        # Get the page number from query parameters
        page_number = request.GET.get('page', 1)

        # Fetch the queryset
        queryset = self.get_queryset()

        # Initialize the paginator
        paginator = Paginator(queryset, self.paginate_by)

        try:
            # Validate the page number
            page_number = int(page_number)
            if page_number < 1:
                raise ValueError('Page number less than 1')
            elif page_number > paginator.num_pages:
                # Redirect to the last page if the number is too high
                return HttpResponseRedirect(f'?page={paginator.num_pages}')
        except (ValueError, PageNotAnInteger):
            # Redirect to the first page if the number is invalid
            return HttpResponseRedirect('?page=1')

        # Call the parent class's get method to continue
        return super().get(request, *args, **kwargs)