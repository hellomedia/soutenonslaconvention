from slc.templating import piglet
from slc import options


def homepage(request):
    return piglet.render(
        "default/index.html",
        {"days_left": (request.now.date() - options.CONVENTION_DATE).days},
    )


def templated_page(request, template):
    return piglet.render(template, {})
