from slc.templating import piglet
from slc import options


def homepage(request):
    return piglet.render(
        "default/index.html",
        {"days_left": (options.CONVENTION_DATE - request.now.date()).days - 1},
    )


def templated_page(request, template):
    return piglet.render(template, {})


def support_us(request):
    return piglet.render("default/support-us.html", {})
