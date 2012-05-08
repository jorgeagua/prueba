response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Inicio'),URL('default','index')==URL(),URL('default','index'),[]),
(T('cliente'),URL('default','cliente')==URL(),URL('default','cliente'),[]),
(T('categoria'),URL('default','categoria')==URL(),URL('default','categoria'),[]),
(T('articulos'),URL('default','articulo')==URL,URL('default','articulo'),[]),
(T('Lista de Pendientes'),URL('default','presupuestos2')==URL,URL('default','presupuestos2'),[]),
(T('Modificacion'),URL('default','presupuestos')==URL,URL('default','presupuestos'),[]),

(T('Nueva Salida'),URL('default','movimientos')==URL,URL('default','movimientos'),[])
]