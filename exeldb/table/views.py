from ctypes import sizeof
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
import table.models as m
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from openpyxl import Workbook,load_workbook
import pytz
import os
from wsgiref.util import FileWrapper
from django.conf import settings
import mimetypes

def index(request):
    return render(request, "index.html")

def bd_search(request):
    if request.method =="GET":
        name = request.GET.get("db_name", "")
        before = request.GET.get("db_before", "")
        after = request.GET.get("db_after", "")
        change_or_edit = request.GET.get("db_change_or_edit", "change")
        if before != "":
            before = datetime.strptime(before, '%d/%m/%Y')
        else:
            before = datetime.now()
        if after != "":
            after =  datetime.strptime(after, '%d/%m/%Y')
        else:
            after = datetime.min
        before = pytz.utc.localize(before)
        after = pytz.utc.localize(after)
        dbs = []
        if name != "":
            dbs_raw = m.DB.objects.all()
            for i in dbs_raw:
                if (i.name.find(name) != -1):
                    if (change_or_edit == "changed"):
                        if (i.change >= after and i.change <= before):
                            db = {'name':i.name,'create':i.create,\
                                'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                            dbs.append(db)
                    elif (change_or_edit == "created"):
                        if (i.create >= after and i.create <= before):
                            db = {'name':i.name,'create':i.create,\
                                'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                            dbs.append(db)
                    else:
                        db = {'name':i.name,'create':i.create,\
                                'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                        dbs.append(db)
        else:
            dbs_raw = m.DB.objects.all()
            for i in dbs_raw:            
                if (change_or_edit == "changed"):
                    if (i.change >= after and i.change <= before):
                        db = {'name':i.name,'create':i.create,\
                            'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                        dbs.append(db)
                elif (change_or_edit == "created"):
                    if (i.create >= after and i.create <= before):
                        db = {'name':i.name,'create':i.create,\
                            'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                        dbs.append(db)
                else:
                    db = {'name':i.name,'create':i.create,\
                            'change':i.change,'link':'show/' + str(i.id),\
                                'link_download' : 'download/' + str(i.id)}
                    dbs.append(db)
        param = {'db':dbs}
        return render(request,"search_db.html",param)


def db_show(request,id):
    allCells = m.Cell.objects.filter(db = int(id))
    maxColl = allCells.aggregate(Max('column'))["column__max"]
    maxRow = allCells.aggregate(Max('row'))["row__max"]
    res = []
    for i in range(1,maxRow + 1):
        row = []
        for j in range(1,maxColl + 1):
            try:          
                cell = allCells.filter(row = i,column = j)[0]   
                var = cell.Read()      
                if var is not None:
                    row.append(str(var))
                else:
                    row.append("")
            except:
                row.append(" ")       
        res.append(row)
    param = {"res" : res}
    return render(request,"show.html", param)

def process(file):
    db = m.DB()
    db.name = file.name 
    db.create = date.today()  
    db.change = db.create    
    db.save() 
    wb = load_workbook(file)
    ws = wb.active
    r = 1
    c = 1
    for row in ws.iter_rows():        
        for cell in row:            
            cell = m.Cell()
            cell.row = r
            cell.column = c
            cell.Set(ws._get_cell(r,c).value)
            cell.db = db
            cell.save()
            c += 1
        c = 1
        r += 1
    return db.id

def changeCell(request):
    if request.method =="POST":
        row = request.POST["row"]
        col = request.POST["col"]
        var = request.POST["var"]
        cell = m.Cell().objects.filter(row = row, column=col)
        cell.Set(var)
        cell.save()
    

def upload(request):
    if request.method =='POST' and request.FILES['excel_file']:
        file = request.FILES['excel_file']
        db_id = process(file)
        #fs = FileSystemStorage()
        #filename = fs.save(file.name, file)
        #uploaded_file_url = fs.url(filename)
        if request.POST["to_edit"]:
            return redirect('/show/' + str(db_id)) # go for an show and edit page
        else:
            return redirect('/')

def download(request, id):
    db = m.DB.objects.filter(id=id)[0]
    wb = Workbook()
    ws = wb.active

    #### create xls
    allCells = m.Cell.objects.filter(db = int(id))
    maxColl = allCells.aggregate(Max('column'))["column__max"]
    maxRow = allCells.aggregate(Max('row'))["row__max"]
    if maxColl is None:
        maxColl = 0
    if maxRow is None:
        maxRow = 0
    for i in range(1,maxRow + 1):
        for j in range(1,maxColl + 1):
            try:          
                cell = allCells.filter(row = i,column = j)[0]   
                var = cell.Read()      
                if var is not None:
                    ws.cell(column=i, row=j, value=var)
                else:
                    pass
            except:
                pass

    #### return xls via http
    name = db.name
    dest_filename = os.path.join(settings.BASE_DIR, 'media',  name)    
    wb.save(filename = dest_filename)
    file = open(dest_filename, 'rb')
    response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response

# Прервись чтением исходников, уважаемый, лови анекдот:
# Байден выступает перед журналистами:
# — Кто сказал, что я читаю по бумажке? Ха, черточка, ха, черточка, ха!