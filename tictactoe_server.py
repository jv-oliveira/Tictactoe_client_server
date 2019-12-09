from server.server_request_handler import ServerRequestHandler
from server.session_manager import SessionManager
from server.game_session_manager import GameSessionManager
import getopt
import sys
import http.server
from timeloop import Timeloop
from datetime import timedelta

HOST = None
PORT = None

tl = Timeloop()


def usage():
    print("python3 tictactoe_server.py [-h host -p port]")


def main():
    parse_arguments()
    handler = ServerRequestHandler
    with http.server.ThreadingHTTPServer((HOST, PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.gsm = GameSessionManager()
        httpd.sm = SessionManager()

        @tl.job(interval=timedelta(seconds=30))
        def delete_old_invites():
            httpd.gsm.remove_old_invites()

        httpd.serve_forever()


def parse_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], ":hf:p:o")
    except getopt.GetoptError as err:
        # print help information and exit:
        print
        str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    global HOST
    global PORT
    for o, a in opts:
        if o in ("-h", "--host"):
            HOST = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        elif o == "--help":
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if HOST is None:
        HOST = '127.0.0.1'
        print("Host was not defined, running in localhost ({})...".format(HOST), file=sys.stderr)

    if PORT is None:
        PORT = 65432
        print("Port was not defined, running in default ({})...".format(PORT), file=sys.stderr)


if __name__ == "__main__":
    main()
