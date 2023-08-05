# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Université Catholique de Louvain.
#
# This file is part of INGInious.
#
# INGInious is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INGInious is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with INGInious.  If not, see <http://www.gnu.org/licenses/>.
""" A middleware for Web.py that serves static content """
import posixpath
import urllib
import web


class StaticMiddleware(object):
    """ WSGI middleware for serving static files. """

    def __init__(self, app, paths):
        self.app = app
        self.paths = paths

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)

        for prefix, root_path in self.paths:
            if path.startswith(prefix):
                environ["PATH_INFO"] = root_path + "/" + web.lstrips(path, prefix)
                return web.httpserver.StaticApp(environ, start_response)
        return self.app(environ, start_response)

    def normpath(self, path):
        """ Normalize the path """
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2
