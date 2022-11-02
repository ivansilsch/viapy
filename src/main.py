from viapy import App
from builder import DinamicRouteBuilder
import json
from pathlib import Path


routes_file = Path.joinpath(Path.cwd(), "src", "routes_definition.json")
routes_definition = open(routes_file, "r").read()
routes_json = json.loads(routes_definition)

route_builder = DinamicRouteBuilder()
RouterClass = route_builder.build(routes=routes_json)

router = RouterClass()

app = App()
app.config(router=router)
app.run("127.0.0.1", 6677)