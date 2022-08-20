from fileswitch.providers import ActionProvider, get_print_action


def test_action_provider():
    provider = get_print_action()
    assert provider

    provider.action("MyFile.txt")
