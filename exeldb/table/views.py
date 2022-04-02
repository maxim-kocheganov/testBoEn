from ctypes import sizeof
from django.http import HttpResponse
from django.shortcuts import render
import table.models as m
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from openpyxl import Workbook,load_workbook

def index(request):
    return render(request, "index.html")

def bd_search(request):
    if request.method =="GET":
        name = request.GET["db_name"]
        dbs = []
        if name is not None:
            dbs_raw = m.DB.objects.all()
            for i in dbs_raw:
                if (i.name.find(name) != -1):
                    db = {'name':i.name,'create':i.create,\
                        'change':i.change}
                    dbs.append(db)
        else:
            dbs = m.DB.objects.all()
        param = {'db':dbs}
        return render(request,"search_db.html",param)


def db_show(request,id):
    allCells = m.Cell.objects.filter(db = int(id))
    maxColl = allCells.aggregate(Max('column'))["column__max"]
    maxRow = allCells.aggregate(Max('row'))["row__max"]
    res = []
    for i in range(0,maxRow):
        row = []
        for j in range(0,maxColl):
            try:          
                cell = allCells.filter(row = i,column = j)            
                row.append(str(cell.Read()))
            except:
                row.append(" ")       
        res.append(row)
    param = {"res" : res}
    return render(request,"show.html", param)

def process(file):
    db = m.DB()
    db.name = file.name       
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
# Прервись чтением исходников, уважаемый, лови анекдот:
# Байден выступает перед журналистами:
# — Кто сказал, что я читаю по бумажке? Ха, черточка, ха, черточка, ха!