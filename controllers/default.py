# -*- coding: utf-8 -*-
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
    datasource = db(db.products.id>0).select()
    powerTable = plugins.powerTable
    powerTable.datasource = datasource
    powerTable.headers = 'labels'
    powerTable.showkeycolumn = False
    powerTable.dtfeatures['bJQueryUI'] = request.vars.get('jqueryui',True)
    powerTable.uitheme = request.vars.get('theme','Smoothness')
        
    
    return dict(table=powerTable.create())
