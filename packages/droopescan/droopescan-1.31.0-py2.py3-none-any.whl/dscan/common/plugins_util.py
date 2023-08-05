from cement.core import handler
from common import file_len, VersionsFile
from plugins.internal.base_plugin import BasePlugin
import subprocess

def plugins_get():
    plugins = plugins_base_get()

    return_plugins = []
    for p in plugins:
        plugin = Plugin(p)
        return_plugins.append(plugin)

    return return_plugins

def plugins_base_get():
    controllers = handler.list('controller')
    plugins = []

    for c in controllers:
        is_base_scan = c.__name__.lower() == 'scan'
        if issubclass(c, BasePlugin) and not is_base_scan:
            plugins.append(c)

    return plugins

class Plugin(object):
    plugin = None
    name = None

    plugins_can_enumerate = False
    plugins_wordlist_size = None
    plugins_mtime = None

    themes_can_enumerate = False
    themes_wordlist_size = None
    themes_mtime = None

    interesting_can_enumerate = False
    interesting_urls_size = None

    version_can_enumerate = False
    version_highest = None

    def __init__(self, PluginClass=None):
        """
            @param PluginClass: as returned by handler.list('controller'). Must
                extend BasePlugin.
        """
        plugin = PluginClass()
        if plugin:

            self.name = plugin._meta.label

            if plugin.can_enumerate_plugins:
                self.plugins_can_enumerate = True
                self.plugins_wordlist_size = file_len(plugin.plugins_file)

            if plugin.can_enumerate_themes:
                self.themes_can_enumerate = True
                self.themes_wordlist_size = file_len(plugin.themes_file)

            if plugin.can_enumerate_interesting:
                self.interesting_can_enumerate = True
                self.interesting_url_size = len(plugin.interesting_urls)

            if plugin.can_enumerate_version:
                versions_file = VersionsFile(plugin.versions_file)

                self.version_can_enumerate = True
                hvm = versions_file.highest_version_major(plugin.update_majors)
                self.version_highest = ', '.join(hvm.values())

    def file_mtime(self, file_path):
        out = subprocess.check_output(['git', 'log', '-1', '--format=%cr',
            file_path]).strip()

        return out

