from fileswitch.routes import Route, get_console_route


def test_action_provider():
    provider = get_console_route()
    assert provider

    provider.action("MyFile.txt")
