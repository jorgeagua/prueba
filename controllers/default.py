# -*- coding: utf-8 -*-
if 0:
    from gluon.globals import *
    from gluon.html import *
    from gluon.http import *
    from gluon.tools import Auth
    from gluon.sqlhtml import SQLFORM, SQLTABLE, form_factory
    session = Session()
    request = Request()
    response = Response()

### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires



def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def cliente():
    # presentacion de listado de clientes
    datasource = db(db.cliente.id>0).select()
    powerTable = plugins.powerTable
    powerTable.datasource = datasource
    powerTable.headers = 'labels'
    powerTable.showkeycolumn = False
    powerTable.dtfeatures['bJQueryUI'] = request.vars.get('jqueryui',True)
    powerTable.uitheme = request.vars.get('theme','Smoothness')
    powerTable.dtfeatures["sScrollY"] = "100%"
    powerTable.dtfeatures["sScrollX"] = "100%"
    powerTable.dtfeatures['sPaginationType'] = 'full_numbers'
    powerTable.dtfeatures["iDisplayLength"] = 20
    # alta de clientes 
    mystep = [dict(title='NUEVO CLIENTE',Legend='Ingrese los datos del nuevo cliente',
                   fields=['empresa','contacto','telefono','correo'])]
    from plugin_PowerFormWizard import PowerFormWizard
    options = {'description':False,'legend':True,'validate':True}
    form = PowerFormWizard(db.cliente, steps=mystep, options=options)
    
    if form.accepts(request.vars, session):
        response.flash = "registro aceptado"
    elif form.errors:
        form.step_validation()
        response.flash = "error en los datos"
    return dict( table=powerTable.create(),form=form)    
   
@auth.requires_login()
def categoria():
    # presentacion de categorias de articulos
    datasource = db(db.categoria.id>0).select()
    powerTable = plugins.powerTable
    powerTable.datasource = datasource
    powerTable.headers = 'labels'
    powerTable.showkeycolumn = False
    powerTable.dtfeatures['bJQueryUI'] = request.vars.get('jqueryui',True)
    powerTable.uitheme = request.vars.get('theme','Smoothness')
    powerTable.dtfeatures["sScrollY"] = "100%"
    powerTable.dtfeatures["sScrollX"] = "100%"
    powerTable.dtfeatures['sPaginationType'] = 'full_numbers'
    powerTable.dtfeatures["iDisplayLength"] = 30
    # alta de categoria de articulos
    mystep = [dict(title='NUEVAS CATEGORIAS',Legend='Ingrese una Categoria para Agrupar artículos',fields=['name'])]
    from plugin_PowerFormWizard import PowerFormWizard
    options = {'description':False,'legend':True,'validate':True}
    form = PowerFormWizard(db.categoria, steps=mystep, options=options)
    
    if form.accepts(request.vars, session):
        response.flash = "registro aceptado"
    elif form.errors:
        form.step_validation()
        response.flash = "error en los datos"
    return dict( table=powerTable.create(),form=form)

def editablefunction():
    id = request.vars.row_id
    column = request.vars.column
    db(db.order_lines.id==id).update(column=value)
    db.commit()

@auth.requires_login()
def articulo():
    
    # presentacion de tabla de articulos ############    
    datasource = db(db.articulo.id>0).select()
    powerTable = plugins.powerTable
    powerTable.datasource = datasource
    powerTable.headers = 'labels'
    powerTable.showkeycolumn = False
    powerTable.dtfeatures['bJQueryUI'] = request.vars.get('jqueryui',True)
    powerTable.uitheme = request.vars.get('theme','Smoothness')
    powerTable.dtfeatures["sScrollY"] = "100%"
    powerTable.dtfeatures["sScrollX"] = "100%"
    powerTable.dtfeatures['sPaginationType'] = 'full_numbers'
    powerTable.dtfeatures["iDisplayLength"] = 10
    powerTable.extrajs = dict(autoresize={},
                             tooltip={},
                             details={'detailscolumns':'articulo.memo'}
                             )
    powerTable.keycolumn = 'articulo.id'
    powerTable.columns = ['articulo.descripcion','articulo.link',
                          'articulo.precio','articulo.categoria']
    # alta de articulos ####################    
    mystep = [dict(title='NUEVOS ARTICULOS',Legend='Ingrese los datos del articulo',
                   fields=['descripcion','memo','iva','precio','categoria'])]
    from plugin_PowerFormWizard import PowerFormWizard
    options = {'description':False,'legend':True,'validate':True}
    form = PowerFormWizard(db.articulo, steps=mystep, options=options)
    
    if form.accepts(request.vars, session):
        response.flash = "registro aceptado"
    elif form.errors:
        form.step_validation()
        response.flash = "error en los datos"
    return dict( table=powerTable.create(),form=form)


def features():
    from plugin_PowerGrid.CallBack import CallBack        
    return CallBack(db.movimientos.id>0 and db.movimientos.fecha_devuelta==None)

@auth.requires(auth.has_membership(role='Admin'))   
def presupuestos():
            
    from plugin_PowerGrid.PowerGrid import PowerGrid
    p = PowerGrid(
                  callback=URL('default','features', extension='json'),
                  buttons=[
                            ##('details',URL('plugin_PowerGrid','data',args=['read','products'])+'/${id}','_blank','Details of Record ${id}','modal positive left button','magnifier',[600,500]),
                            ('cargar comprobante',URL('default','prueba',args=['read','movimientos'])+'/${id}','_blank','Editando Registro ${id}','refreshmodal middle button', 'pen',[600,800]),
                            ##('delete',URL('plugin_PowerGrid','data',args=['delete','products'])+'/${id}','_blank','Are you sure you want to delete record ${id}','confirmationmodal right negative button', 'cross'),
                          
                         ],
                  addurl=URL('plugin_PowerGrid','data',args=['create','features']), 
                  addLabel='Add New Record',   
                  addTitle='You are adding a new record',              
                  headers=[['id','Codigo'],['entregado_x','Entrega: '], ['retirado_x','Retira'],
                           ],
                  
                  #headers=[['entregado_x','Entrega: '], ['retirado_x','Retira'], ['id_articulo','Articulo'],['cantidad','Cantidad'],
                           #['cliente','Usado en']],
                  #hidecontrolbuttons=True,
                  #hiderefreshbutton=True,
                  hideaddbutton=True,
                  #_id="banana",
                  #target="melancia",
                  #searchBy='equal',
                  minH=800,
                  options=dict(#colsWidth=[60,60,60],
                               #width=700,
                               #buttonBackTitle='Back',
                               #buttonMax=4,
                               #buttonNextTitle='Next',
                               #success="""js[function(){alert('Executed on success');}]js""",
                               #before="""js[function(){alert('Executed before');}]js""",
                               #error="""js[function(){alert('Executed on load error');}]js""",
                               #buttonOption=False,
                               #buttonsWidth=200
                               #buttonTitle='oi',
                               #clickFx=False,
                               #debug=True,
                               #find='name',search='J',
                               #searchOption=False,
                               searchButtonLabel='Buscar',
                               searchButtonTitle='Clique para buscar',
                               searchFocus=True,
                               #cache=True,
                               #contentType='application/x-www-form-urlencoded; charset=utf-8',
                               #type='get',
                               #dataType='jsonp',
                               #jsonp=True,
                               #jsonpCallback='callback',
                               #findsName=[['name','name']],
                               #hoverFx=False,
                               #loadingOption=True,
                               #loadingText='Carregando...',
                               #messageOption=False,
                               #noResultOption=False,
                               noResultText='no se encontraron datos ',
                               #page=1,
                               #rows=3,
                               #rowsNumber=[3,25],
                               #params='&blablabla=45',
                               #resize=False,
                               #resultOption=False,
                               #resultText= 'Exibindo {from} - {to} de {total} registros',
                               #scroll=True,height=100,
                               #searchText='Busque aqui',
                               #sortName='name',
                               #sortOrder='asc',
                               #template='template',
                               #templateStyle='blabla',



                                   ),
                  )

    return dict(p=p)

@auth.requires_login()
def presupuestos2():
            
    class Virtual(object):
        @virtualsettings(label=T('Informacion: '))
        def virtualtooltip(self):
            return T('se retiro para  <strong>%s</strong>, en concepto de <strong>%s</strong>' %
                     (self.cliente.empresa,self.movimientos.concepto))
        
    datasource = db(db.movimientos.cliente==db.cliente.id).select() 
    powerTable = plugins.powerTable
    powerTable.datasource = datasource
    powerTable.virtualfields = Virtual()
    powerTable.headers = 'labels'
    powerTable.showkeycolumn = True
    powerTable.dtfeatures['bJQueryUI'] = request.vars.get('jqueryui',True)
    powerTable.uitheme = request.vars.get('theme','Smoothness')
    powerTable.dtfeatures['sScrollX'] = '100%'
    powerTable.dtfeatures['sPaginationType'] = request.vars.get('pager','scrolling')
    powerTable.extrajs = dict(autoresize={},
                               tooltip={},
                               )
    powerTable.columns = ['movimientos.id',
                         'movimientos.entregado_x',
                         'movimientos.retirado_x',
                         'movimientos.id_articulo',
                         'movimientos.cantidad',
                         'movimientos.Comprobante',
                         'movimientos.fecha_pedido',
                         'movimientos.fecha_devuelta'
                         ]
    return dict(table=powerTable.create())

@auth.requires(auth.has_membership(role='Admin'))  
def movimientos():
    mystep = [dict(title='MOVIMIENTOS',Legend='Ingrese los datos solicitados',
                   fields=['entregado_x','retirado_x','id_articulo','cantidad',
                           'estado','Comprobante',
                           'cliente','concepto'])]
    from plugin_PowerFormWizard import PowerFormWizard
    options = {'description':False,'legend':True,'validate':True}
    form = PowerFormWizard(db.movimientos, steps=mystep, options=options)
    
    if form.accepts(request.vars, session):
        response.flash = "registro aceptado"
        #rows = db(db.movimientos.id>0).select()
        #last_row = rows.last()
        #a=db.memomovi.insert(referencia=last_row.id,entregado_x=last_row.entregado_x,
                             #retirado_x=last_row.retirado_x,id_articulo=last_row.id_articulo,
                             #cantidad=last_row.cantidad,fecha_pedido=last_row.fecha_pedido,
                             #fecha_devuelta=last_row.fecha_devuelta,estado=last_row.estado,
                             #Comprobante=last_row.Comprobante,cliente=last_row.cliente)
        #db.commit()
    elif form.errors:
        form.step_validation()
        response.flash = "error en los datos"
    return dict(form=form)

def prueba():
    variable = request.args[0]
    form=FORM('Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted '
    elif form.errors:
        response.flash = 'form has errors  '
    else:
        response.flash = 'please fill the form  ${variable}s'
    return dict(form=form)