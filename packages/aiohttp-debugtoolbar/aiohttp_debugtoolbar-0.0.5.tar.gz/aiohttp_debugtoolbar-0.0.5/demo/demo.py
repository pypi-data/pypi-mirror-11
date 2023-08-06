import asyncio
import json
import logging
import os
import sys

from pathlib import Path

import jinja2
import aiohttp_debugtoolbar
import aiohttp_jinja2
from aiohttp import web

try:
    import aiohttp_mako
except ImportError:
    aiohttp_mako = None


parent = Path('.').parent
parent = str(parent.absolute())
sys.path.insert(0, parent)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(PROJECT_ROOT, 'templates')


def json_renderer(func):
    assert asyncio.iscoroutinefunction(func), func

    @asyncio.coroutine
    def wrapper(request):
        response = web.HTTPOk()
        context = yield from func(request)
        try:
            text = json.dumps(context)
        except TypeError:
            raise RuntimeError("{!r} result {!r} is not serializable".format(
                func, context))
        response.content_type = 'application/json'
        response.text = text
        return response

    return wrapper


@asyncio.coroutine
def exc(request):
    log.error('NotImplementedError exception handler')
    raise NotImplementedError


@aiohttp_jinja2.template('ajax.jinja2')
def test_ajax(request):
    return {'app': request.app}


@json_renderer
@asyncio.coroutine
def call_ajax(request):
    log.info('call_ajax handler')
    return {'ajax': 'success'}


@asyncio.coroutine
def test_redirect(request):
    log.info('redirect handler')
    raise web.HTTPSeeOther(location='/')


@aiohttp_jinja2.template('index.jinja2')
@asyncio.coroutine
def test_page(request):
    title = 'Aiohttp Debugtoolbar'

    log.info('Info logger fon index page')
    log.debug('Debug logger fon index page')
    log.critical('Critical logger fon index page')

    return {
        'title': title,
        'show_jinja2_link': True,
        'show_sqla_link': False,
        'app': request.app,
        'aiohttp_mako': aiohttp_mako}


@aiohttp_jinja2.template('error.jinja2')
def test_jinja2_exc(request):
    return {'title': 'Test jinja2 template exceptions'}


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop,
                          middlewares=[aiohttp_debugtoolbar.middleware])

    aiohttp_debugtoolbar.setup(app, intercept_exc='debug')
    loader = jinja2.FileSystemLoader([templates])
    aiohttp_jinja2.setup(app, loader=loader)

    if aiohttp_mako:
        aiohttp_mako.setup(app, input_encoding='utf-8',
                           output_encoding='utf-8',
                           default_filters=['decode.utf8'],
                           directories=[templates])

        @aiohttp_mako.template('error.mako')
        def test_mako_exc(request):
            return {'title': 'Test Mako template exceptions'}

        app.router.add_route('GET', '/mako_exc', test_mako_exc,
                             name='test_mako_exc')

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates))

    # static view
    app.router.add_static('/static', os.path.join(PROJECT_ROOT, 'static'))

    app.router.add_route('GET', '/redirect', test_redirect,
                         name='test_redirect')
    app.router.add_route('GET', '/', test_page, name='test_page')
    app.router.add_route('GET', '/exc', exc, name='test_exc')

    # ajax handlers
    app.router.add_route('GET', '/ajax', test_ajax, name='test_ajax')
    app.router.add_route('GET', '/call_ajax', call_ajax, name='call_ajax')

    # templates error handlers
    app.router.add_route('GET', '/jinja2_exc', test_jinja2_exc,
                         name='test_jinja2_exc')

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '127.0.0.1', 9000)
    log.debug("Server started at http://127.0.0.1:9000")
    return srv, handler


loop = asyncio.get_event_loop()
srv, handler = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(handler.finish_connections())
