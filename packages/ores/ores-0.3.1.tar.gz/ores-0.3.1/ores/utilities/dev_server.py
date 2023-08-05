"""
Starts a development web server.

Usage:
    dev_server (-h | --help)
    dev_server [--port=<num>] [--verbose] [--config=<path>]

Options:
    -h --help        Print this documentation
    --port=<num>     The port number to start the server on [default: 8080]
    --config=<path>  The path to a yaml config file
                     [default: config/ores-localdev.yaml]
    --verbose        Print logging information
"""
import logging

import docopt

import yamlconf

from ..wsgi import server


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    config = yamlconf.load(open(args['--config']))

    if args['--verbose']:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
        )

    app = server.configure(config)
    app.run(host="0.0.0.0",
            port=int(args['--port']),
            debug=True,
            ssl_context="adhoc",
            threaded=True)
