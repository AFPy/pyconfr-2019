from urllib.request import urlopen
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_frozen import Freezer
from markdown2 import Markdown
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


@app.route('/2019/<lang>/talks/<category>.html')
def talks(lang, category):
    talks = []
    with urlopen('https://cfp-2019.pycon.fr/schedule/xml/') as fd:
        tree = ElementTree.fromstring(fd.read().decode('utf-8'))
    for day in tree.findall('.//day'):
        for event in day.findall('.//event'):
            talk = {child.tag: child.text for child in event}
            talk['person'] = ', '.join(
                person.text for person in event.findall('.//person'))
            talk['id'] = event.attrib['id']
            talk['day'] = day.attrib['date']
            if talk['type'] != category:
                continue
            if 'description' in talk:
                talk['description'] = Markdown().convert(talk['description'])
            talks.append(talk)
    return render_template(
        '{lang}/talks.html.jinja2'.format(lang=lang),
        category=category, talks=talks, lang=lang)


@app.route('/2019/schedule.html')
def schedule():
    with urlopen('https://cfp-2019.pycon.fr/schedule/html/') as fd:
        data = fd.read().decode('utf-8')
        # Delete extra cells for sprints
        data = (
            data
            .replace('colspan="9"', '')
            .replace('<td colspan="8"></td>', ''))

    # insert link in the table
    soup = BeautifulSoup(data, 'html.parser')
    conf_colors = {
        '#ff7373': 'keynote',
        '#73cbef': 'workshop',
        '#e9b96e': 'conference',
    }
    for color, kind in conf_colors.items():
        for td in soup.find_all('td', attrs={'bgcolor': color}):
            title = list(td.children)[0]
            href = '/2019/fr/talks/{}.html#{}'.format(
                kind, str(title).lower()
            )
            link = soup.new_tag('a', href=href)
            title.wrap(link)
    data = str(soup)

    return render_template('schedule.html.jinja2', data=data)


@app.cli.command('freeze')
def freeze():
    Freezer(app).freeze()
