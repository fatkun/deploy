 # -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(u'机器名', max_length=100)
    username = models.CharField(u'用户名', max_length=100)
    version = models.CharField(u'版本', max_length=20)
    tags = models.CharField(u'标签', max_length=250, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('hostname', 'username')

# class Task(models.Model):
#     """主任务"""
#     cmd = models.TextField()
#     state = models.CharField(u'状态', max_length=20)
#     create_time = models.DateTimeField(auto_now_add=True)
#
# class SubTask(models.Model):
#     task = models.ForeignKey(Task)
#     state = models.CharField(u'状态', max_length=20)
#     start_time = models.DateTimeField(null=True)
#     end_time = models.DateTimeField(null=True)
#     result = models.TextField()

class Health(models.Model):
    host = models.ForeignKey(Host)
    type = models.CharField(u'指标种类', max_length=20)
    data = models.TextField(u'内容')
    modify_time = models.DateTimeField(auto_now=True)