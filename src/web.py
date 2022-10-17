from time import localtime

from microdot import send_file
from microdot_asyncio import Microdot


def web_server() -> Microdot:
    app = Microdot()

    @app.route("/")
    async def index(request):
        now = localtime()
        return f"Hello World! It is now {now[3]}:{now[4]}:{now[5]}"

    @app.route("/<path:path>")
    async def html(request, path):
        if ".." in path:
            return "Not found", 404
        return send_file("html/" + path)

    return app
