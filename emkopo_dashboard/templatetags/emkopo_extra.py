from django import template
from django.conf import settings

from emkopo_dashboard.constants import DARK, DARK_THEME, LIGHT_THEME, LIGHT
from emkopo_dashboard.models import AppTheme

register = template.Library()


@register.inclusion_tag(
    f"emkopo_dashboard/bootstrap/scripts.html",
    takes_context=True,
)
def js_scripts(context):
    title = None
    return dict(
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_dashboard/bootstrap/buttons/theme_button.html",
    takes_context=True,
)
def theme_mode(context, url=None):
    title = None
    theme_mode = DARK
    theme_name = DARK_THEME
    current_usr = context.get('user')
    current_theme = AppTheme.objects.filter(theme_user=current_usr)
    if current_theme is None:
        theme_name = DARK_THEME
        theme_mode = theme_mode
    elif current_theme:
        thm = list(current_theme.values())[0]
        if thm['theme_mode'] == LIGHT:
            theme_name = DARK_THEME
            theme_mode = DARK
        else:
            theme_name = LIGHT_THEME
            theme_mode = LIGHT
    next = url_name(url)
    uri = f'?name={theme_name}&mode={theme_mode}&next={next}'
    return dict(
        title=title,
        theme_name=theme_name,
        theme_url=uri,
    )


def url_name(url):
    url_name = url.split('/')
    return url_name[-2]


@register.simple_tag(takes_context=True)
def get_theme(context, theme='light'):
    current_usr = context.get('user')
    if current_usr.is_authenticated:
        current_theme = AppTheme.objects.filter(theme_user=current_usr)
        theme = list(current_theme.values())[0]['theme_mode'] if current_theme else LIGHT
    return theme


@register.inclusion_tag(
    f"emkopo_dashboard/bootstrap/header/user_theme.html",
    takes_context=True,
)
def theme_user_mode(context):
    current_usr = context.get('user')
    current_theme = AppTheme.objects.filter(theme_user=current_usr)
    if current_theme:
        theme = list(current_theme.values())[0]['theme_mode']
        usr_theme = theme
    else:
        usr_theme = LIGHT

    return dict(
        usr_theme=usr_theme,
    )


@register.inclusion_tag(
    f"emkopo_dashboard/bootstrap/buttons/pagination.html",
    takes_context=True,
)
def pagination(context):
    page_obj = context.get("page_obj")
    num_pages = "a" * page_obj.paginator.num_pages if page_obj else 1
    show_pagination = True if page_obj.paginator.num_pages > settings.EMKOPO_PAGINATION else False

    return dict(
        page_obj=page_obj,
        pages=page_obj.paginator.num_pages,
        num_pages=num_pages,
        show_pagination=show_pagination,
    )
