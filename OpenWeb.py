import sublime, sublime_plugin, urllib2, StringIO

class OpenWebCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("URL:", "", self.on_done, None, None)
        pass

    def on_done(self, url):
        view = None
        try:
            localfile = StringIO.StringIO()
            remotefile = urllib2.urlopen(url)
            sublime.status_message("Loading " + url + "...")
            localfile.write(remotefile.read())
            if (remotefile.headers['content-type']):
                encoding=remotefile.headers['content-type'].split('charset=')[-1] 
            else:
                encoding="utf-8"
            view = self.window.new_file()
            edit = view.begin_edit()
            view.insert(edit, 0, unicode(localfile.getvalue(), encoding))
            localfile.close()
            remotefile.close()
            view.end_edit(edit)
            sublime.status_message("")
        except urllib2.URLError as e:
            sublime.error_message("Loading '{0}' url error: {1}".format(url, e))
        except urllib2.HTTPError as e:
            sublime.error_message("Loading '{0}' error: {1}".format(url, e))
        finally:
            if view:
                view.end_edit(edit)