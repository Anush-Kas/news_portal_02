from django import forms
from django_filters import CharFilter, ChoiceFilter, DateTimeFilter, FilterSet

from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', label='Title')
    category = CharFilter(lookup_expr='exact', label='Category')
    created_at = DateTimeFilter(lookup_expr='gt', label='Date',
                                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    kind = ChoiceFilter(label='Type', choices=Post.KINDS_CHOICES)

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'created_at',
            'kind'
        ]
