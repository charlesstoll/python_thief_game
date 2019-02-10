import sys
# This a dummy script to stand in for our motion scripts. It just needs to read STDIN and print.

while True:
    x = sys.stdin.readline()

    if x:
        print("Motion script received: {}".format(x))


