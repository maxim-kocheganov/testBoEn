from django.db import models
import enum
import struct
import base64
from datetime import date

class DB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    create = models.DateTimeField(default = date.today())
    change = models.DateTimeField(default = date.today())

class Type(enum.IntEnum):
    integer = 1
    string = 2
    date = 3
    null = 4

# Type-packed version
"""
class Cell(models.Model):    
    id = models.IntegerField(primary_key=True)
    row = models.IntegerField()
    column = models.IntegerField()
    type = models.IntegerField()
    data = models.TextField(blank=True, null=True)
    db = models.ForeignKey(
        DB,
        on_delete=models.CASCADE)
    def Set(self,var):
        if var is None:
            self.type = Type.null
        if type(var) == int:
            self.type = Type.integer
            self.data = base64.b64encode(struct.pack('i', var)).decode("utf-8")
        elif type(var) == str:
            self.type = Type.string
            self.data = base64.b64encode(var.encode("utf-8")).decode("utf-8")

    def Read(self):
        if self.type == Type.string:
            return base64.b64decode(self.data.encode("utf-8")).decode('utf-8')
        elif self.type == Type.integer:
            return struct.unpack('i',base64.b64decode(self.data.encode("utf-8")))[0]
        elif self.type == Type.null:
            return None
"""

class Cell(models.Model):    
    id = models.AutoField(primary_key=True)
    row = models.IntegerField()
    column = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    db = models.ForeignKey(
        DB,
        on_delete=models.CASCADE)
    def Set(self,var):
        self.data = str(var)

    def Read(self):
        return self.data