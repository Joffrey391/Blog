from django.contrib.admin import SimpleListFilter
from .models import Post

class PostTitleFilter(SimpleListFilter):
    title = 'Post Titles'
    parameter_name = 'post_title'
    related_filter_parameter = 'post__title__id__exact'

    def lookups(self, request, model_admin):
        list_of_questions = []
        queryset = Post.objects.order_by('title')
        if self.related_filter_parameter in request.GET:
            queryset = queryset.filter(title=request.GET[self.related_filter_parameter])
        for post in queryset:
            list_of_questions.append(
                (str(post.id), post.title)
            )
        return sorted(list_of_questions, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(post_id=self.value())
        return queryset
