import math
import time
import random

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



total_traversals = 0

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
def uct(w_i, n_i, N_i):
    c = math.sqrt(2)
    return (w_i/n_i)+c*math.sqrt((math.log(N_i))/n_i)


class Node:
    def __init__(self):
        #self.wins = 0
        self.visited = 0
        self.hashcode = 0
        self.val = random.randint(10, 200)

def main():
    board = BigBoard()
    global total_traversals
    root = Node()
    root.hashcode = init_hash()
    old_move = [1,4,4]
    mcts(root, old_move, 5)

    for i in explored:
        print(i.hashcode)

    print(total_traversals)
    print("Time taken = ", time.time() - start_time)

def time_out():
    cur_time = time.time()
    if (cur_time - start_time) > 0.1:
        return True
    return False


def change_player(player):
    if player == 5:
        return 3

    return 5

def mcts(root, old_move, player):
    while not(time_out()):
        traverse(root, old_move, player)
        #end_node = rollout(node)
        #backpropagate(node, end_node)

explored = []

def traverse(node, old_move, player):
    mx = 0
    child = 0
    bfs(node, old_move, player, True, 0)
    #for i in explored:

        # if uct(node.wins, node.visited, total_traversals) > mx:
        #     mx = uct(node.wins, node.visited, total_traversals)
        #     child = i
    #traverse(node)

def bfs(node, old_move, player, first, mn):
    global total_traversals
    
    if first:
        i = 3 * (old_move[1] % 3)
        j = 3 * (old_move[2] % 3)
        mn = j
        cnt = 18*i + j + 8*old_move[0]
        print("First move", i, j)
    else:
        i = old_move[1]
        j = old_move[2]
        cnt = 18*i + j + 8*old_move[0]

    hashcode = add(node.hashcode, mul(modulo_exp(x, cnt*j+i,
                                                 MOD), player-2, MOD), MOD)
    child = Node()
    child.hashcode = hashcode

    if first:
        first = False
        old_move = [0, i, j]
    else:            
        if old_move[0] == 0:
            old_move[0] += 1
        else:
            old_move[0] = 0
            if old_move[2] % 3 == 2:
                old_move[1] = (old_move[1]+1)%9
            if old_move[2]+1 > mn + 2:
                old_move[2] = mn
            else:
                old_move[2] += 1

    total_traversals += 1
    #print(old_move)
    explored.append(child)
    rollout(child, old_move, player)
    child.visited += 1
    #player = change_player(player)
    if old_move[1] != 2*mn:
        print(old_move)
        bfs(node, old_move, player, first, mn)
    else:
        print(mn)



exploit = []
move = []

def rollout(node, old_move, player):
    depth = 100
    exploit = []
    while depth > 0:
        print(old_move)
        exploit.append(node)
        move.append(old_move)

        i = 3 * (old_move[1] % 3)
        j = 3 * (old_move[2] % 3)
        
        i = random.randint(i, i+2)
        j = random.randint(j, j+2)
        cnt = 18*i + j + 8*old_move[0]

        child = Node()
        child.hashcode = add(node.hashcode, mul(modulo_exp(x, cnt*j+i,
                                                 MOD), player-2, MOD), MOD)
        depth -= 1
        old_move = [(i^j)%2, i, j]
        node = child
        player = change_player(player)
    #     if child.val > 100 and depth > 50:
    #         break

    # backpropagate(child.val)

def backpropagate(val):
    pass


if __name__ == "__main__":
    main()
