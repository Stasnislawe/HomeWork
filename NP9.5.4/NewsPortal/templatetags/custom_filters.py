from django import template


register = template.Library()

bad_words = [
   'Редиска', "редиска"
]

@register.filter()
def censor(text):
   a = text
   for word in bad_words:
      a = a.replace(word, word[:1] + "*" * (len(word)-1))
   return a




