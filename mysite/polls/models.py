"""Model:
- your database layout, with additional metadata
- contains the essential fields and behaviors of the data you're storing
- represented by a class that subclasses django.db.models.Model

Field:
- represented by an instance of a Field class, e.g., CharField and DateTimeField
- name of each Field instance (e.g. question_text or pub_date) is the field's name
  - used in Python code, and as the database table column name
- optional first positional argument to designate a human-readable name, e.g., "date
published"
  - used in a couple of introspective parts of Django, and doubles as documentation
- some Field classes have required arguments
  - CharField requires a `max_length`
  - used in the database schema, and in validation

Relationship:
- defined using `ForeignKey`
"""
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # To indicate the method represents the 'pub_date' field, which can then be used for
    # sorting on the admin page.
    was_published_recently.admin_order_field = "pub_date"
    # To display 'on' or 'off' icon instead of True or False on the admin page.
    was_published_recently.boolean = True
    # To customise the column's title on the admin page.
    was_published_recently.short_description = "Published recently?"

    def __str__(self):
        """Important to add `__str__()` methods to your models because objects'
        representations are used throughout Django's automatically-generated admin"""
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
