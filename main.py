from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
import requests


class HexExtension(Extension):

    def __init__(self):
        super(HexExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()

        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Open Elixir docs',
                                    on_enter=OpenUrlAction('https://hexdocs.pm/elixir'))
            ])
        else:
            search_url = 'https://hex.pm/api/packages?search=%s&sort=recent_downloads'

            api_results = requests.get(search_url % query).json()

            result_items = list(map(self.build_result_item, api_results))

            return RenderResultListAction(result_items)

    def build_result_item(self, package):
        primary_action = OpenUrlAction(package['html_url'])

        if (package['docs_html_url'] != None):
            options = [
                ExtensionResultItem(icon='images/hex.png',
                                    name='View package',
                                    on_enter=OpenUrlAction(package['html_url'])),
                ExtensionResultItem(icon='images/hexdocs.png',
                                    name='View documentation',
                                    on_enter=OpenUrlAction(package['docs_html_url']))
            ]

            primary_action = RenderResultListAction(options)

        return ExtensionResultItem(icon='images/icon.png',
                                   name=package['name'],
                                   description=package['meta']['description'],
                                   on_enter=primary_action)


if __name__ == '__main__':
    HexExtension().run()
