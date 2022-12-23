from fileswitch.routes import Route, RouteController


class TestRouteControl:
    def test_defaultdict(self):
        controller = RouteController()
        controller.routes["hello"] = "abc"

        # controller.routes["asdasd"].append(22)
        # controller.routes["asdasd"].append(22)


