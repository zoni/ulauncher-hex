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
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        else:
            search_url = "https://hex.pm/api/packages?search=%s&sort=recent_downloads"

            api_results = requests.get(search_url % query).json()

            result_items = list(map(self.build_result_item, api_results))

            return RenderResultListAction(result_items)

    def build_result_item(self, package):
        return ExtensionResultItem(icon='images/icon.png',
                                   name=package["name"],
                                   description=package["meta"]["description"],
                                   on_enter=OpenUrlAction(package["html_url"]))


if __name__ == '__main__':
    HexExtension().run()
