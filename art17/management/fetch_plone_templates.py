import flask

from flask.ext.script import Manager, Option
from flask.ext.security.script import (
    CreateUserCommand as BaseCreateUserCommand
)
from bs4 import BeautifulSoup

import requests
import os

class FetchPloneTemplates(BaseCreateUserCommand):

    def prepare_html(self, html, PLONE_URL):
        html = html.replace('href="/', 'href="' + PLONE_URL + '/')
        html = html.replace('src="/', 'src="' + PLONE_URL + '/')
        html = html.replace('href="http://localhost:3080/', 'href="' + PLONE_URL + '/')
        # Replace site id for Matomo
        tracking_old = '_paq.push([\'setSiteId\', \'42\'])'
        tracking_new = '_paq.push([\'setSiteId\', \'38\'])'
        html = html.replace(tracking_old, tracking_new)
        return html.encode('utf-8').strip()

    def prepare_header(self, header_text):
        new_tag = header_text.new_tag("a", href="/auth/login", title="Log in")
        new_tag.string = "Log in"
        header_text.find("a", {"class": "pat-plone-modal"}).decompose()
        header_text.find("div", {"class": "login"}).find('ul').decompose()
        header_text.find('ol').find('li').decompose()
        return header_text

    def run(self, **kwargs):
        print("Fetching header and footer from plone..")

        plone_url_layout = flask.current_app.config['LAYOUT_PLONE_URL']
        auth_cookie = flask.request.cookies.get('__ac')
        resp = requests.get(
            plone_url_layout,
            cookies={'__ac': auth_cookie}
        )
        plone_path = os.path.join(
            flask.current_app.instance_path, 
            '..','art17', 'templates', 'plone'
        )

        header_files = [
            'head_cached.html',
            'before_login_cached.html',
            'before_breadcrumbs_cached.html',
            'header_cached.html',
            'header_before_container_cached.html',
            'header_after_container_cached.html',
            'footer_cached.html',
        ]
        if resp.status_code == 200:
            header_text = self.prepare_header(BeautifulSoup(self.prepare_html(resp.text, plone_url), features="html.parser"))
            head = header_text.find("head")
            HEAD = '{% raw %}' + head.prettify().encode('utf-8').replace('</head>', '') + '{% endraw %}'
            login = header_text.body.prettify().split('<div class="login">')
            BEFORE_LOGIN = '</head>' + login[0].encode('utf-8') + '<div class="login"><ul><li>'
            split_header_and_footer = login[1].split('<footer id="portal-footer-wrapper"')
            HEADER =  '</li></ul>' + split_header_and_footer[0].encode('utf-8')
            split_breadcrumbs = split_header_and_footer[0].encode('utf-8').split('<ol aria-labelledby="breadcrumbs-you-are-here">')
            BEFORE_BREADCRUMBS = split_breadcrumbs[0] + '<ol aria-labelledby="breadcrumbs-you-are-here">'
            split_before_and_after_container = split_breadcrumbs[1].split("</main>")
            HEADER_BEFORE_CONTAINER = split_before_and_after_container[0].encode('utf-8')
            HEADER_AFTER_CONTAINER = "</main>" + split_before_and_after_container[1].encode('utf-8')
            footer = BeautifulSoup(split_header_and_footer[1])
            footer.find("script", {"data-bundle": "production"}).decompose()
            FOOTER = '<footer id="portal-footer-wrapper"' + footer.prettify().encode('utf-8')
            templates = {
                'head.html': HEAD,
                'before_login.html': BEFORE_LOGIN,
                'before_breadcrumbs.html': BEFORE_BREADCRUMBS,
                'header.html': HEADER,
                'header_before_container.html': HEADER_BEFORE_CONTAINER,
                'header_after_container.html': HEADER_AFTER_CONTAINER,
                'footer.html': FOOTER,
            }
        else:
            files = [
                'head.html',
                'before_login.html',
                'before_breadcrumbs.html',
                'header.html',
                'header_before_container.html',
                'header_after_container.html',
                'footer.html',
            ]
            templates = {}
            for template, file_name in zip(files, header_files):
                with open(os.path.join(plone_path, file_name)) as f:
                    templates[template] = f.read()

        for template_name, content in templates.iteritems():
            template_path = os.path.join(plone_path, template_name)
            with open(template_path, 'w') as f:
                f.write(content)


fetch_plone_templates = Manager()
fetch_plone_templates.add_command('run', FetchPloneTemplates())