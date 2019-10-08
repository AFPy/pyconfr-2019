from urllib.request import urlopen

from flask import Flask, abort, render_template
from flask_frozen import Freezer
from sassutils.wsgi import SassMiddleware

app = Flask(__name__, static_url_path='/2019/static')
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'pyconfr': {
        'sass_path': 'static/sass',
        'css_path': 'static/css',
        'wsgi_path': '/2019/static/css',
        'strip_extension': True}})


@app.route('/')
@app.route('/2019/')
@app.route('/2019/<lang>/<name>.html')
def page(name='index', lang='fr'):
    return render_template(
        '{lang}/{name}.html.jinja2'.format(name=name, lang=lang),
        page_name=name, lang=lang)


@app.route('/2019/schedule.html')
def schedule():
    with urlopen('https://cfp-2019.pycon.fr/schedule/html/') as fd:
        data = fd.read().decode('utf-8')
        # Delete extra cells for sprints
        data = (
            data
            .replace('colspan="9"', '')
            .replace('<td colspan="8"></td>', ''))
    return render_template('schedule.html.jinja2', data=data)


@app.cli.command('freeze')
def freeze():
    Freezer(app).freeze()
