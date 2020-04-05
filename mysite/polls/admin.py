from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """An 'InlineModelAdmin' object.
    StackedInLine lays out model objects top-down, whereas 'TabularInline' lays them out
    in a table.
    See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-objects"""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """`ModelAdmin` is the representation of a model in the admin interface. You can
    register the model class, `Question`, without defining a `ModelAdmin` object if you
    are happy with the default admin interface."""

    # Add a search box to enable search against the 'question_text' field. You can add
    # as many fields as you like, but because it uses a 'LIKE' query, limit the number
    # of search fields.
    # See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    search_fields = ["question_text"]

    # If you don't set list_display, the admin site will display a single column that
    # displays the __str__() representation.
    # See: method attributes in models.Question
    # See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = ("question_text", "pub_date", "was_published_recently")

    # Add a 'Filter' sidebar to filter the change list by the 'pub_date' field. The type
    # of filter displayed depends on the type of field.
    # See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ["pub_date"]

    # `fields` option make simple layout changes in the forms on the 'add' and 'change'
    # pages. This makes 'Publication date' come before the 'Question' field.
    # fields = ["pub_date", "question_text"]

    # For forms with dozens of fields, split the form up into fieldsets. fieldsets is
    # a list of two-tuples, each representing a <fieldset> (section) on the admin form
    # page. The two-tuples are in the format (name, field_options), where 'name' is the
    # title of the fieldset, and 'field_options' is a dictionary of information about
    # the fieldset.
    # See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    # Choice objects are edited on the Question admin page, with fields for 3 extra
    # choices.
    # 'inlines' enable editing of models on the same page as a parent model.
    inlines = [ChoiceInline]


# Register your models here.
# Tell the admin site that Question objects have an admin interface
# AdminSite.register(model_or_iterable, admin_class=None, **options)
# See: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.AdminSite.register
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
