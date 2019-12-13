# -*- coding:utf-8 -*-


from werkzeug.exceptions import NotFound, Forbidden, BadRequest


class CommitException(Exception):
    pass


AbortException = (NotFound, Forbidden, BadRequest)
