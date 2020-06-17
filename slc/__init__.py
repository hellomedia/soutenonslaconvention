from fresco import FrescoApp
import slc.request

__all__ = ["app", "options"]

app = FrescoApp()
app.request_class = slc.request.Request
options = app.options
queries = None
