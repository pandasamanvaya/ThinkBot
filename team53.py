import math
import time


def mul(x, y, mod):
    return (x % mod * y % mod) % mod


def add(x, y, mod):
    return (x % mod + y % mod) % mod


def sub(x, y, mod):
    return (x % mod - y % mod + mod) % mod


def modulo_exp(x, y, mod):
    ans = 1
    power = x
    while y > 0:
        if y % 2 == 1:
            ans = (ans % mod * power % mod) % mod
        power = (power % mod * power % mod) % mod
        y /= 2
    return ans


MOD = 1000000007
x = 18


def init_hash():
    cnt = 1
    hashcode = 0
    for j in range(18):
        for i in range(9):
            hashcode = add(hashcode, mul(modulo_exp(x, cnt*j+i,
                                                    MOD), 2, MOD), MOD)
        cnt += 1
    return hashcode


def board_hash(hashcode, new_move, player):
    i = new_move[1]
    j = new_move[0]*8 + new_move[2]
    cnt = i*18 + j
    curr_hash = hashcode
    curr_hash = add(hashcode, mul(modulo_exp(x, cnt*j+i,
                                             MOD), player-2, MOD), MOD)

    return curr_hash


def uct(w_i, n_i, N_i):
    c = math.sqrt(2)
    return (w_i/n_i)+c*math.sqrt((math.log(N_i))/n_i)


class Node:
    def __init__(self):
        self.wins = 0
        self.visited = 0
        self.hashcode = 0


class BigBoard:

    def __init__(self):
        # big_boards_status is the game board
        # small_boards_status shows which small_boards have been won/drawn and by which player
        self.big_boards_status = (
            [['-' for i in range(9)] for j in range(9)], [['-' for i in range(9)] for j in range(9)])
        self.small_boards_status = (
            [['-' for i in range(3)] for j in range(3)], [['-' for i in range(3)] for j in range(3)])

    def print_board(self):
        # for printing the state of the board
        print '================BigBoard State================'
        for i in range(9):
            if i % 3 == 0:
                print
            for k in range(2):
                for j in range(9):
                    if j % 3 == 0:
                        print "",
                    print self.big_boards_status[k][i][j],
                if k == 0:
                    print "   ",
            print
        print

        print '==============SmallBoards States=============='
        for i in range(3):
            for k in range(2):
                for j in range(3):
                    print self.small_boards_status[k][i][j],
                if k == 0:
                    print "  ",
            print
        print '=============================================='
        print
        print


start_time = time.time()


def time_out():
    cur_time = time.time()
    if (cur_time - statr_time) > 23.7:
        return True
    return False


def main():
    board = BigBoard()
    h = init_hash()


global total_traversals


def mcts(root):
    while !time_out():
        node = traverse(root)
        end_node = rollout(node)
        backpropagate(node, end_node)
    total_traversals = 0


def bfs(node, old_move, player, first, mn):
    if first:
        i = 3 * (old_move[1] % 3)
        j = 3 * (old_move[2] % 3)
        mn = j
        cnt = 18*i + j
        first = False
    else:
        i = old_move[1]
        j = old_move[2]
        cnt = 18*i+j

    hashcode = add(node.hashcode, mul(modulo_exp(x, cnt*j+i,
                                                 MOD), 2, MOD), MOD)
    child = Node()
    child.hashcode = hashcode

    if old_move[0] == 0:
        old_move[0] += 1
    else:
        old_move[0] = 0
        if old_move[2] % 3 == 2:
            old_move[1] += 1
        if old_move[2]+1 > mn + 2:
            old_move[2] = mn
        else:
            old_move[2] += 1

    if player == 5:
        player = 3
    else:
        player = 5
    if old_move[1] % 3 != 2 and old_move[2] % 3 != 2:
        bfs(node, old_move, player, first, mn)


def traverse(node, old_move, player):
    mx = 0
    child = 0
    total_traversals += 1
    bfs(node, old_move, player, True, 0)
    for i in range(18):

        # if uct(node.wins, node.visited, total_traversals) > mx:
        #     mx = uct(node.wins, node.visited, total_traversals)
        #     child = i
traverse(node)


def rollout(node):


def backpropagate(start_node, end_node):


if __name__ == "__main__":
    main()
