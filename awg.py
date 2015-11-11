import requests
import os
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache
from json import load
from os import makedirs
from os.path import dirname, isfile, exists
import shutil


if not exists('repos'):
        makedirs('repos')

if not isfile('settings.json'):
    origin = dirname(__file__)+ "/" + "awg-data" + "/"
    if not exists('main.css'):
        shutil.copy(origin + 'main.css', 'main.css')
    if not exists('settings.json'):
        shutil.copy(origin + 'settings.json', 'settings.json')
    if not exists('default_template'):
        for f in ['default_template']:
            shutil.copytree(origin + f, f)

settings = load(open('settings.json'))
bcc = FileSystemBytecodeCache(settings['jinjacache'], '%s.cache')
jinja2_env = Environment(
    loader=FileSystemLoader(settings['template']), bytecode_cache=bcc)


def draw_template(name, totemplate):
    t = jinja2_env.get_template(name)
    return t.render(totemplate)


class Generate:

    def __init__(self):
        self.username = settings['username']
        self.api = settings['api']
        self.kwargs = {}
        if 'GH_TOKEN' in os.environ:
            self.kwargs = {'headers': {'Authorization': 'token ' + os.environ["GH_TOKEN"]}}

        self.info = requests.get("%susers/%s" % (self.api,
                                                 self.username),
                                 **self.kwargs).json()
        self.repos = requests.get("%susers/%s/repos" % (self.api,
                                                        self.username),
                                  **self.kwargs).json()
        if len(self.info) == 2:
            exit(self.info['message'])  # pragma: no cover

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
            # x = self.get_params_repo(repo, ['name', 'html_url', 'description'])
            totemplate['repos'][repo['name']] = repo
        f = open('index.html', 'wb')
        f.write(draw_template('index.tpl', totemplate).encode("utf-8"))
        f.close()

    def generate_specific_pages(self):
        totemplate = {'info': {}}
        totemplate['info'] = self.get_info()
        for repo in self.repos:
            # x = self.get_params_repo(repo, ['name', 'html_url', 'description'])
            totemplate['repo'] = repo
            if self.kwargs != {}:
                self.kwargs['headers']['Accept'] =  'application/vnd.github.v3.html'
            else:
                self.kwargs['headers'] = {'Accept': 'application/vnd.github.v3.html'}
            r = requests.get("%srepos/%s/%s/readme" % (self.api,
                                                       self.username,
                                                       repo['name']),
                             **self.kwargs)
            if r.ok:
                html_readme = r.text
            else:
                html_readme = ""

            totemplate['repo']['html'] = html_readme
            f = open('repos/%s.html' % repo['name'], 'wb')
            f.write(draw_template('repo.tpl', totemplate).encode("utf-8"))
            f.close()


def generate():
    g = Generate()
    # import time
    # while True:
    #    time.sleep(30)
    #    g.generate_main_page()
    g.generate_main_page()
    g.generate_specific_pages()

if __name__ == "__main__":
    generate()  # pragma: no cover
