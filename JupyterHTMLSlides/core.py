import random
import string
import os

from IPython.display import display, HTML
from .utils import html_loader
from .utils import get_content
from jinja2 import Template


class JupyterSlides:
    def __init__(
        self,
        content_path='./content.yaml',
        table_contents=False
    ):
        self.set_base_dirs()
        self.set_source_dirs()
        self.content = get_content(content_path)
        self.render_init_templates()
        if table_contents:
            self.render_table_contents()

    def set_base_dirs(self):
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.base_template_dir = f'{self.module_path}/src/templates'
        self.base_css_dir = f'{self.module_path}/src/assets/css'
        self.base_js_dir = f'{self.module_path}/src/js'

    def set_source_dirs(self):
        self.called_from_path = os.getcwd()
        folders = self.called_from_path.split('/')
        self.source_path = '/'.join(folders[:folders.index('talks')])
        self.template_dir = f'{self.source_path}/src/templates'
        self.css_dir = f'{self.source_path}/src/css'
        self.js_dir = f'{self.source_path}/src/js'

    def render_init_templates(self):
        self.render(
            template='init',
            data={'dir': self.module_path},
            template_dir=self.base_template_dir
        )

        if os.path.isfile(f'{self.template_dir}/init.html'):
            self.render(
                template=f'init',
                data=self.content.get('init_vars', {})
            )

        id = JupyterSlides.randomUUID()

        self.render(
            template='eye',
            data={'eye_id': id},
            template_dir=self.base_template_dir
        )

    def render_table_contents(self):
        if os.path.isfile(f'{self.template_dir}/table-contents.html'):
            contents_template_dir = self.template_dir
        else:
            contents_template_dir = self.base_template_dir

        self.render(
            template='table-contents',
            data=self.generate_table_contents(),
            template_dir=contents_template_dir,
            render_type='slide'
        )

    def parse_template(self, template=None, data={}, template_dir=None, render_type=None):
        if not template_dir:
            if os.path.isfile(f'{self.template_dir}/{template}.html'):
                html = html_loader(f'file:{self.template_dir}/{template}.html')
            else:
                template = 'basic-slide'
                html = html_loader(f'file:{self.base_template_dir}/{template}.html')
        else:
            if not os.path.isfile(f'{template_dir}/{template}.html'):
                template = 'basic-slide'
                template_dir = self.base_template_dir

            html = html_loader(
                f'file:{template_dir}/{template}.html')

        if render_type == 'slide':
            html = '<div id="{{ data["slide_id"] }}" class="slide-container">' + \
                html + '</div>'

        tm = Template(html)
        return tm.render(data=data)

    def render(self, template=None, data={}, navigation=False, template_dir=None, render_type=None):
        html = self.parse_template(
            template=template,
            data=data,
            template_dir=template_dir,
            render_type=render_type
        )
        if navigation:
            navigation_template = self.parse_template(
                template='navigation',
                template_dir=template_dir
            )
            html += navigation_template

        display(HTML(html))

    def render_content(self, key):
        data = self.content.get(key)
        id = JupyterSlides.randomUUID()
        self.render(
            template='eye',
            data={'eye_id': id},
            template_dir=self.base_template_dir
        )
        if data.get('slides'):
            for el in data.get('slides'):
                template = el.get('template')
                self.render(template=template, data=el, render_type='slide')

    @staticmethod
    def randomUUID(stringLength=20):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def generate_table_contents(self):
        table = {}
        items = []
        for _, item in self.content.items():
            for sub_item in item['slides']:
                sub_item['slide_id'] = \
                    str(item['indice']) + '.' + str(sub_item['indice']) +\
                    sub_item['content_title']
            item['slide_id'] = item['slides'][0]['slide_id']
            items.append(item)
        table['title'] = 'Table of Contents'
        table['eyebrow'] = 'Table of Contents'
        table['items'] = items
        return table
