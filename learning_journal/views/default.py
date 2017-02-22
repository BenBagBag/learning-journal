from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models.mymodel import Entry, DBSession, User
from .forms import EntryCreateForm, LoginForm

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid, forget, remember


@view_config(route_name='home', renderer='templates/list.jinja2', permission='view')
def index_page(request):
    entries = Entry.all()
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
    return {'entries': entries, 'login_form': form}


@view_config(route_name='detail', renderer='templates/detail.jinja2', permission='view')
def view(request):
    this_id = request.matchdict.get('id', -1)
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry, 'id': this_id}


@view_config(route_name='action', match_param='action=create', renderer='templates/edit.jinja2', permission='create')
def create(request):
    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='action', match_param='action=edit', renderer='templates/edit.jinja2', permission='edit')
def update(request):
    this_id = request.matchdict['id']
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    form = EntryCreateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('detail', id=request.matchdict.get('id', -1)))
    return {'form': form, 'action': request.matchdict.get('action'), 'id': this_id}


@view_config(route_name='auth', match_param='action=in', renderer='string',
     request_method='POST')
def sign_in(request):
    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
