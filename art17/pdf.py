import os
import subprocess
import uuid
from path import path

from flask import current_app as app
from flask import Response, g

_PAGE_DEFAULT_MARGIN = {'top': '8mm', 'bottom': '8mm',
                        'left': '16mm', 'right': '16mm'}


def read_file(f):
    while True:
        data = f.read(131072)
        if data:
            yield data
        else:
            break
    f.close()


def stream_template(template_name, **context):
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    rv = template.stream(context)
    rv.enable_buffering(5)
    return rv


class PdfRenderer(object):
    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.title = kwargs.get('title', '')
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.margin = kwargs.get('margin', _PAGE_DEFAULT_MARGIN)
        self.orientation = kwargs.get('orientation', 'portrait')
        self.context = kwargs.get('context', {})

        dir = self._get_dir()
        self.template_path = (dir / (str(uuid.uuid4()) + '.html'))
        self.pdf_path = (dir / (str(uuid.uuid4()) + '.pdf'))
        g.is_pdf_process = True

    def _get_dir(self):
        return path(app.config['PDF_DESTINATION'])

    def _render_template(self):
        with open(self.template_path, 'w+') as f:
            for chunk in stream_template(self.template_name, **self.context):
                f.write(chunk.encode('utf-8'))

    def _generate_pdf(self):
        command = ['wkhtmltopdf', '-q',
                   '--encoding', 'utf-8',
                   '--page-height', self.height,
                   '--page-width', self.width,
                   '-B', self.margin['bottom'],
                   '-T', self.margin['top'],
                   '-L', self.margin['left'],
                   '-R', self.margin['right'],
                   '--orientation', self.orientation]
        if self.title:
            command += ['--title', self.title]

        command += [str(self.template_path), str(self.pdf_path)]

        FNULL = open(os.devnull, 'w')
        subprocess.check_call(command, stdout=FNULL, stderr=subprocess.STDOUT)

    def _generate(self):
        self._render_template()
        try:
            self._generate_pdf()
        finally:
            self.template_path.unlink_p()

    def as_attachement(self):
        return self._pdf_file()

    def as_response(self):
        return Response(read_file(self._pdf_file()),
                        mimetype='application/pdf')

    def _pdf_file(self):
        try:
            self._generate()
            pdf = open(self.pdf_path, 'rb')
        finally:
            self.pdf_path.unlink_p()
        return pdf
