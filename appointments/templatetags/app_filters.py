from django import template
import datetime as datetime

register = template.Library()

@register.filter
def is_past(self):
    print(self.date())
    print(datetime.datetime.today().date())
    return self.date() <= datetime.datetime.today().date()
