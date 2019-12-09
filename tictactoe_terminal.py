"""tictactoe game for 2 players
from blogpost: http://thebillington.co.uk/blog/posts/writing-a-tic-tac-toe-game-in-python by  BILLY REBECCHI,
slightly improved by Horst JENS"""
from __future__ import print_function
import getopt
import sys
import http.client

choices = []

HOST = None
PORT = None

OUTPUT = None
FILEPATH = None

server_conn = None


def connect_to_server():
    server_conn = http.client.HTTPConnection(HOST, PORT, timeout=10)



def usage():
    print("python3 cliente.py -f filepath")


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
    global FILEPATH
    global OUTPUT
    for o, a in opts:
        if o in ("-h", "--host"):
            HOST = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        elif o in ("-f", "--filepath"):
            FILEPATH = a
        elif o == "--help":
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            OUTPUT = a
        else:
            assert False, "unhandled option"

    if HOST is None:
        HOST = '127.0.0.1'
        print("Host was not defined, running in localhost ({})...".format(HOST), file=sys.stderr)

    if PORT is None:
        PORT = 65432
        print("Port was not defined, running in default ({})...".format(PORT), file=sys.stderr)

    if FILEPATH is None:
        print("Please specify a file path to request from server!", file=sys.stderr)
        usage()
        sys.exit(-1)


def print_board():
    print('\n -----')
    print('|' + choices[0] + '|' + choices[1] + '|' + choices[2] + '|')
    print(' -----')
    print('|' + choices[3] + '|' + choices[4] + '|' + choices[5] + '|')
    print(' -----')
    print('|' + choices[6] + '|' + choices[7] + '|' + choices[8] + '|')
    print(' -----\n')

if __name__ == "__main__":
    parse_arguments()

    connect_to_server()


    for x in range(0, 9):
        choices.append(str(x + 1))

    playerOneTurn = True
    winner = False

    while not winner:
        print_board()

        if playerOneTurn :
            print( "Player 1:")
        else :
            print( "Player 2:")

        try:
            choice = int(input(">> "))
        except:
            print("please enter a valid field")
            continue
        if choice not in range(1,9) or choices[choice - 1] == 'X' or choices [choice-1] == 'O':
            print("illegal move, plase try again")
            continue

        if playerOneTurn :
            choices[choice - 1] = 'X'
        else :
            choices[choice - 1] = 'O'

        playerOneTurn = not playerOneTurn

        for x in range (0, 3) :
            y = x * 3
            if (choices[y] == choices[(y + 1)] and choices[y] == choices[(y + 2)]) :
                winner = True
                print_board()
            if (choices[x] == choices[(x + 3)] and choices[x] == choices[(x + 6)]) :
                winner = True
                print_board()

        if((choices[0] == choices[4] and choices[0] == choices[8]) or
           (choices[2] == choices[4] and choices[4] == choices[6])):
            winner = True
            print_board()

    print ("Player " + str(int(playerOneTurn + 1)) + " wins!\n")
