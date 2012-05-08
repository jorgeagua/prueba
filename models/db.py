# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
if 0:
    from gluon.sql import *
    from gluon.validators import *

    
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate, Mail
auth = Auth(globals(),db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables

########################################
db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(username)s',
    migrate=settings.migrate)

db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
auth.define_tables(migrate = settings.migrate)
auth.settings.actions_disabled=['register','request_reset_password','retrieve_username']

## configure email
mail=Mail()
mail=auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'jorge.agua@gmail.com'
mail.settings.login = 'jorge.agua@gmail.com:rahogimilmar'
#mail.settings.server = 'logging'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('cliente',
                Field('empresa','string',label=T('Empresa')),
                Field('contacto','string',label=T('Contacto')),
                Field('telefono','string',label=T('Telefono')),
                Field('correo',label=T('Correo')),
                Field('created_on','datetime',label=T('Creado en'),default=request.now)
                )
db.cliente.empresa.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,db.cliente.empresa)]
db.cliente.contacto.requires=[IS_NOT_EMPTY()]
db.cliente.correo.requires=[IS_EMAIL()]

db.define_table('categoria',
                Field('name',label=T('Categoria')),
                      format=lambda r:r.name
                )
db.categoria.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,db.categoria.name)]

iva=[0.21,0.105]
db.define_table('articulo',
                Field('descripcion','string',label=T('Descripcion')),
                Field('memo','text',label='Detalle Completo'),
                Field('link','string',label=T('enlace a:')),
                Field('iva','double',label=T('IVA')),
                Field('precio','double',label=T('Precio')),
                Field('categoria',db.categoria,label=T('Categoria'),
                      represent=lambda r:r.name)
                )
db.articulo.descripcion.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,db.articulo.descripcion)]
db.articulo.iva.requires=IS_IN_SET(iva)
db.articulo.precio.requires=IS_DECIMAL_IN_RANGE(0,200000)
db.articulo.categoria.requiers=IS_IN_DB(db,'categoria.name','%(name)s',
                                        zero=T('elija una'))
db.articulo.link.requires=IS_URL()


estado=["Parte En Poder de Técnico","Salida Con Remito","Salida Con Orden de Servicio","Devuelta a Deposito"]
concepto=["Alquiler","Venta"]
db.define_table('movimientos',
                Field('entregado_x','string',label=T('Entregado por')),
                Field('retirado_x','string',label=T('Retirado por'),default=request.now),
                Field('id_articulo','integer',label=T('Codigo de Articulo')),
                Field('cantidad','integer',label=T('Cantidad')),
                Field('fecha_pedido','datetime',label=T('Fecha de pedido'),default=request.now),
                Field('fecha_devuelta','datetime',label=T('Fecha de Cierre')),
                Field('estado','string',default='EN USO',label=T('Estado')),
                Field('Comprobante','string',default='0',label=T('Nro. de Comprobante')),
                Field('cliente','integer',label=T('Para uso en')),
                Field('concepto','string',default='Alquiler',label=T('Concepto'))
                )
# validadores
db.movimientos.id_articulo.represent = lambda id: db.articulo(id).descripcion
db.movimientos.cliente.represent = lambda id: db.cliente(id).empresa
db.movimientos.id_articulo.requires=IS_IN_DB(db,'articulo.id')
db.movimientos.entregado_x.requires=IS_IN_DB(db,'auth_user.username')
db.movimientos.retirado_x.requires=IS_IN_DB(db,'auth_user.username')
db.movimientos.estado.requires=IS_IN_SET(estado)
db.movimientos.cliente.requires=IS_IN_DB(db,'cliente.id')
db.movimientos.concepto.requires=IS_IN_SET(concepto)

# widgetss
db.movimientos.id_articulo.widget = SQLFORM.widgets.autocomplete(
    request, db.articulo.descripcion, id_field=db.articulo.id)
db.movimientos.cliente.widget = SQLFORM.widgets.autocomplete(
    request, db.cliente.empresa, id_field=db.cliente.id, min_length=1)

db.define_table('memomovi',
                Field('referencia','integer',label=T('Referencia')),
                Field('entregado_x','string',label=T('Entregado por')),
                Field('retirado_x','string',label=T('Retirado por'),default=request.now),
                Field('id_articulo','integer',label=T('Codigo de Articulo')),
                Field('cantidad','integer',label=T('Cantidad')),
                Field('fecha_pedido','datetime',label=T('Fecha de pedido'),default=request.now),
                Field('fecha_devuelta','datetime',label=T('Fecha de Cierre')),
                Field('estado','string',default='',label=T('Estado')),
                Field('Comprobante','string',default='0',label=T('Nro. de Comprobante')),
                Field('cliente','integer',label=T('Para uso en')),
                Field('concepto','string',default='Alquiler',label=T('Concepto'))
                )





mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login




