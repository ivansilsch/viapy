class RouterBaseClass:
	def __init__(self) -> None:
		pass


class DinamicRouteBuilder:

	def __init__(self):
		pass

	def extract_route( self, routes: dict, name: str, RouterClassContainer: iter = None):

		content = routes[name]
		
		base_route_handler = "GET_root" if name == "GET /" else name.replace("/", "_")
		base_route_handler = base_route_handler.replace(" ", "")
		base_route_handler = base_route_handler.replace(":", "")

		# Extracts a router and updates it with a new function of the route 
		RouterClass, _ = RouterClassContainer
		RouterClass = type("Router", (RouterClass,), {
			base_route_handler: lambda _: content
		})
		RouterClassContainer[0] = RouterClass


	def build(self, routes: dict, RouterClassContainer: iter = None):

		print("Creating the router...")
		RouterClass = type("Router", (RouterBaseClass,), {})
		RouterClassContainer = [RouterClass, None]

		for name in routes.keys():
			self.extract_route(routes, name, RouterClassContainer=RouterClassContainer)

		RouterClass, _ = RouterClassContainer
		
		return RouterClass
		