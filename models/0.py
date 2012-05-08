from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'mi nueva app'
settings.subtitle = 'powered by jorge'
settings.author = 'jorge a'
settings.author_email = 'jorge.agua@gmail.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Colorus'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '424482a4-38d6-466b-a70a-f1a4243045a1'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []