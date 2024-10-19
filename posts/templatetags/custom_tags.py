from django import template

register = template.Library()

bad_words = ['f[ae]y?g+[oeiu]+t+s?', 'даунская', 'пидорасы', 'n󠀡󠀡iggers', 'nigga',
             'моноспектакля', 'обстрела', 'рецензента']


@register.filter()
def censor(text):
    text = text.split()
    for i in range(len(text)):
        if text[i].lower() in bad_words:
            if text[i].istitle() or text[i].islower():
                text[i] = text[i][0] + '*' * (len(text[i]) - 1)
    return ' '.join(text)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
