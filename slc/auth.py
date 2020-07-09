from functools import wraps
from fresco.exceptions import NotFound

from slc.supporters import get_supporter_by_id
from slc import options


def require_admin(view):
    @wraps(view)
    def require_admin(request, *args, **kwargs):
        user_id = request.get_user_id()
        if user_id is None:
            raise NotFound()
        user = get_supporter_by_id(request.getconn(), user_id)
        print(user.email)
        if user.email in options.ADMIN_USERS:
            return view(request, *args, **kwargs)
        raise NotFound()

    return require_admin
