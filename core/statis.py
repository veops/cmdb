# -*- coding:utf-8 -*- 


from flask import Blueprint


statis = Blueprint("statis", __name__)


@statis.route("")
def statis():
    pass