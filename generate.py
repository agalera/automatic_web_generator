import requests
from markdown import markdown
import base64
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache

bcc = FileSystemBytecodeCache("/tmp", '%s.cache')
jinja2_env = Environment(
    loader=FileSystemLoader('templates/'), bytecode_cache=bcc)


def draw_template(name, totemplate):
    t = jinja2_env.get_template(name)
    return t.render(totemplate)


class Generate:

    def __init__(self):
        self.username = "kianxineki"
        self.api = "https://api.github.com/"
        self.auth = ('kianxineki',
                     base64.decodestring('fakepassword=\n'))
        self.info = requests.get("%susers/%s" % (self.api,
                                                 self.username)).json()
        self.repos = requests.get("%susers/kianxineki/repos" % self.api).json()
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

    def get_params_repo(self, repo, params):
        result = {}
        for param in params:
            if repo[param]:
                try:
                    result[param] = self.info[param]
                except:
                    result[param] = None
        return result

    def generate_main_page(self):
        totemplate = {'info': {}, 'repos': {}}

        totemplate['info'] = self.get_info()

        for repo in self.repos:
            x = self.get_params_repo(repo, ['name', 'html_url', 'description'])
            totemplate['repos'][repo['name']] = x

        f = open('index.html', 'wb')
        f.write(draw_template('index.tpl', totemplate).encode("utf-8"))
        f.close()

    def generate_specific_pages(self):
        totemplate = {'info': {}}
        totemplate['info'] = self.get_info()
        for repo in self.repos:
            x = self.get_params_repo(repo, ['name', 'html_url', 'description'])
            totemplate['repo'] = x
            r = requests.get("%srepos/%s/%s/readme" % (self.api,
                                                       self.username,
                                                       repo['name']))
            r = r.json()
            if "content" in r:
                s = unicode(base64.decodestring(r['content']), "utf-8")
                html_readme = markdown(s)
            else:
                html_readme = "not exist readme"
            totemplate['repo']['html'] = html_readme
            f = open('repos/%s.html' % repo['name'], 'wb')
            f.write(draw_template('repo.tpl', totemplate).encode("utf-8"))
            f.close()
g = Generate()
# g.generate_main_page()
g.generate_specific_pages()
