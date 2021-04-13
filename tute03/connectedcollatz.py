from collections import defaultdict, deque
import copy


class Processor:

    def __init__(self, id) -> None:
        self.id = id
        self.inboxes = defaultdict(deque)
        self.neighbours = defaultdict()

    def register_channel(self, neighbour):
        self.neighbours[neighbour.getId()] = neighbour
        self.inboxes[neighbour.getId()] = deque()
        return self

    def getId(self):
        return self.id

    def put(self, msg, nid):
        self.inboxes[nid].append(msg)

    def tick(self):
        for k in self.inboxes.keys():
            q = self.inboxes[k]
            if len(q) > 0:
                msg = q.popleft()
                self.process(msg)

    def process(self, msg):
        print(f"process {self.id}: processing msg = {msg}")
        if (msg == 1 or msg == 0):
            return

        if (msg % 2 == 0):
            self.p2p(msg//2, (self.id + 1) % 3)
        else:
            self.p2p(msg*3+1, (self.id - 1) % 3)

    def multicast(self, msg):
        for k in self.neighbours.keys():
            self.neighbours[k].put(msg, self.id)

    def p2p(self, msg, dest):
        self.neighbours[dest].put(msg, self.id)

    def snapshot(self):
        res = []
        for k in self.inboxes.keys():
            res.append(self.inboxes[k].copy())
        return res

# [ p1: [ [], [], [] ], p2, p3 ]


def solve(p: list[list[list[int]]], q: deque):

    q.append(p)
    depth = 0
    while (len(q) > 0 and depth < 5):
        u = len(q)
        depth += 1
        print("\n\n\n")
        for _ in range(u):
            curP = q.popleft()
            print(depth, curP)
            for i in range(len(curP)):
                for j in range(len(curP[i])):
                    if (len(curP[i][j]) > 0):
                        msg = curP[i][j][0]
                        x = copy.deepcopy(curP)
                        x[i][j].pop(0)
                        q.append(recur(x, msg, i))


def recur(p, msg, m):
    if (msg % 2 == 0):
        newmsg = msg // 2
        newproc = (m + 1) % 3
        p[newproc][m].append(newmsg)
    else:
        newmsg = msg * 3 + 1
        newproc = (m - 1) % 3
        p[newproc][m].append(newmsg)
    return p


def collatz(n):
    if (n != 1):
        print(n)
        if n % 2 == 0:
            collatz(n//2)
        else:
            collatz(n*3+1)


if __name__ == '__main__':
    n = 3
    p = [[[11], [], []], [[10], [], []], [[], [], [9]]]
    solve(p, deque())
    print("\n\n\n")
    collatz(11)
    print("\n\n\n")
    collatz(10)
    print("\n\n\n")
    collatz(9)

    # for i in range(1, n):
    #     cur = Processor(i)
    #     for p in processors:
    #         p.register_channel(cur)
    #         cur.register_channel(p)
    #     processors.append(cur)

    # x = 50
    # for p in processors:
    #     p.process(x)
    #     x *= 3

    # for i in range(2):
    #     for pax in processors:
    #         pax.tick()

    # res = []
    # for pax in processors:
    #     inboxes = pax.snapshot()
    #     print(f"process {pax.getId()}:")
    #     for inn in inboxes:
    #         out = []
    #         while len(inn) > 0:
    #             out.append(inn.popleft())
    #         print(*out)

    # print("done")
