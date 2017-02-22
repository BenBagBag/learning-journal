import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models.mymodel import (
    DBSession,
    Base,
    User, # <-- new
    password_context, # <-- new
)

from sqlalchemy import engine_from_config

# don't need this, it will just cause an error since MyModel doens't exist anymore
# from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    # engine = get_engine(settings)
    Base.metadata.create_all(engine)
    with transaction.manager:
        password = os.environ.get('ADMIN_PASSWORD', 'admin')
        encrypted = password_context.encrypt(password)
        admin = User(name=u'admin', password=encrypted)
        DBSession.add(admin)

    # session_factory = get_session_factory(engine)

    # need to get rid of this, it just adds stuff to MyModel which no longer exists
    # with transaction.manager:
    #     dbsession = get_tm_session(session_factory, transaction.manager)
    #
    #     model = MyModel(name='one', value=1)
    #     dbsession.add(model)
