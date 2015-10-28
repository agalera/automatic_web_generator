import requests
from markdown import markdown
import base64
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache

bcc = FileSystemBytecodeCache("/tmp", '%s.cache')
jinja2_env = Environment(
        loader=FileSystemLoader('templates/'), bytecode_cache=bcc)


def draw_template(name, totemplate):
    t = jinja2_env.get_template(name)
    try:
        print totemplate['info']
    except:
        pass
    return t.render(totemplate)


class Generate:
    def __init__(self):
        self.username = "kianxineki"
        self.api = "https://api.github.com/"
        self.auth = ('kianxineki',
                     base64.decodestring('cGF0cnlraWFuMzI=\n'))
        self.info = requests.get("%susers/%s" % (self.api,
                                                 self.username),
                                 auth=self.auth).json()
        self.repos = requests.get("%susers/kianxineki/repos" % self.api,
                                  auth=self.auth).json()
        if len(self.info) == 2:
            print self.info['message']
            exit("max ratelimit")

    def get_info(self):
        tmp = {}
        for param in ['avatar_url', 'created_at', 'email', 'html_url',
                      'location', 'name', 'public_gists', 'public_repos',
                      'updated_at']:

            tmp[param] = self.info[param]
        return tmp

    def generate_main_page(self):
        totemplate = {'info': {}, 'repos': {}}

        totemplate['info'] = self.get_info()

        for repo in self.repos:
            totemplate['repos'][repo['name']] = {}
            for param in ['name', 'html_url', 'description']:
                if repo[param]:
                    try:
                        totemplate['repos'][repo['name']][param] = self.info[param]
                    except:
                        totemplate['repos'][repo['name']][param] = None

        f = open('index.html', 'wb')
        f.write(draw_template('index.tpl', totemplate))
        f.close()

    def generate_specific_pages(self):
        totemplate = {'info': {}, 'repos': {}}
        totemplate['info'] = self.get_info()
        for repo in self.repos:
            totemplate['repos'][repo['name']] = {}
            r = requests.get("%srepos/%s/%s/readme" % (self.api,
                                                       self.username,
                                                       repo['name']),
                             auth=self.auth)
            r = r.json()
            if "content" in r:
                s = unicode(base64.decodestring(r['content']), "utf-8")
                html_readme = markdown(s)
            else:
                html_readme = "not exist readme"
            totemplate['repos'][repo['name']]['html'] = html_readme
            f = open('repos/%s.html' % repo['name'], 'wb')
            f.write(draw_template('repo.tpl', totemplate))
            f.close()
g = Generate()
g.generate_main_page()
g.generate_specific_pages()
