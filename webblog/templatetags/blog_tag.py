from markdown import Markdown
from django import template

register = template.Library()


@register.filter(name='markdown')
def markdown_to_html(text):
    md = Markdown()
    return md.convert(text)
