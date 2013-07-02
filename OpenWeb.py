import sublime, sublime_plugin, urllib2, StringIO, base64
from urlparse import urlparse, urlunsplit

class OpenWebCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("URL:", "", self.on_done, None, None)
        pass

    def on_done(self, url):
        view = None
        try:
            url = url.strip()
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("ftp://")) :
                url = "http://" + url
            print "loading " + url + " ..."

            # getting username passwords
            url_components = urlparse(url)
            if (url_components.username):
                # trim username/password from url
                host = url_components.hostname
                if url_components.port is not None:
                    host += ":" + str(url_components.port)
                url = urlunsplit((url_components.scheme, host, url_components.path, url_components.query, url_components.fragment))
                # re
                base64string = base64.encodestring('%s:%s' % (url_components.username, url_components.password)).replace('\n', '')
                request = urllib2.Request(url) 
                request.add_header("Authorization", "Basic %s" % base64string)  
            else:
                request = urllib2.Request(url) 
            
            remotefile = urllib2.urlopen(request)     
            localfile = StringIO.StringIO()
            sublime.status_message("Loading " + url + "...")
            localfile.write(remotefile.read())
            defaultEncoding="utf-8"
            if (remotefile.headers['content-type']):
                encoding=remotefile.headers['content-type'].split('charset=')
                if len(encoding) > 1:
                    encoding = encoding[1]
                else:
                   encoding=defaultEncoding
            else:
                encoding=defaultEncoding
            view = self.window.new_file()
            view.set_name(url)
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
        #except ValueError as e:
            #sublime.error_message("Loading '{0}' error: {1}".format(url, e))
        finally:
            if view:
                view.end_edit(edit)