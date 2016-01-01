# -*- coding: utf-8 -*-

from flask_script import Command, Option


class GunicornServer(Command):
    description = 'Run the app within Gunicorn'

    def __init__(self, host='127.0.0.1', port=5000, workers=8,
                 worker_class="sync", daemon=False):
        self.port = port
        self.host = host
        self.workers = workers
        self.worker_class = worker_class
        self.daemon = daemon

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),

            Option("-c", "--worker_class",
                   dest='worker_class',
                   type=str,
                   default=self.worker_class),

            Option("-d", "--daemon",
                   dest="daemon",
                   type=bool,
                   default=self.daemon)
        )

    def handle(self, app, host, port, workers, worker_class, daemon):

        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config

            arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)),
                                      'workers': workers,
                                      'worker_class': worker_class,
                                      'daemon': daemon}), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers,
                        'worker_class': worker_class,
                        'daemon': daemon
                    }

                def load(self):
                    return app

            FlaskApplication().run()
