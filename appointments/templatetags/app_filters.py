from django import template
import datetime as datetime

register = template.Library()

@register.filter
def is_past(self):
    return self.date() <= datetime.datetime.today().date()
