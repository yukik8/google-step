import sys
from collections import deque

# Homework #3 (optional):
# Search the longest path with heuristics.
# 'start': A title of the start page.
# 'goal': A title of the goal page.


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # titleに対応するidを見つける
    def find_id(self, target_title):
        for id, title in self.titles.items():
            if title == target_title:
                return id
        raise ValueError('not found the title')

    # bfsで全てのnodeの中から、ゴールに辿り着くことができるnodeのみに限定する
    def bfs_check_availability(self, start_id):
        queue = deque([start_id])   # 探索中のノード集合
        checked_nodes = set([start_id])
        while queue:
            current = queue.popleft()
            for link in self.links[current]:
                if link not in checked_nodes:
                    checked_nodes.add(link)
                    queue.append(link)
        return checked_nodes

    # dfsで最長のpathを探索する
    def dfs_longest_path(self, start_id, goal_id, nodes):
        longest_path = []
        current = start_id
        path = [start_id]
        node_to_root = {start_id: None}
        depth = {start_id: 1}
        checked_nodes = set([start_id])
        stack = [(start_id, 1, checked_nodes)]
        ver = 0
        while stack:
            current, d, checked_nodes = stack.pop()
            if current == goal_id:
                if d > len(longest_path):   # 現在見たpathが最長の場合longestを現在のものに更新
                    ver += 1
                    # パス復元
                    path = []
                    node = goal_id
                    while node is not None:
                        path.append(node)
                        node = node_to_root[node]
                    longest_path = list(reversed(path))
                    print(ver, len(longest_path), len(stack))
                    # if ver == 9:    # 10個目を試すときにクラッシュしてしまうため一旦、９回で止める
                    #     break
                continue

            # 次につながるリンクが多い順にneighbourを並べてTOP5まで検索する
            # three_neighbours = sorted(self.links[current], key=lambda x: len(
            #     self.links[x]) + sum(len(self.links[n]) for n in self.links[x]), reverse=True)
                # 2階層のリンク数を数えようとしたけど精度が落ちた
            five_neighbours = sorted(
                self.links[current], key=lambda x: len(self.links[x]), reverse=True)
            i = 0
            for neighbour in five_neighbours:
                if neighbour not in checked_nodes and neighbour in nodes:
                    i += 1
                    new_checked_nodes = checked_nodes | {neighbour}
                    node_to_root[neighbour] = current
                    depth[neighbour] = d + 1
                    stack.append((neighbour, d + 1, new_checked_nodes))
                    if i >= 5:  # 上位5つのみ探索
                        break
        return longest_path

    def find_longest_path(self, start, goal):
        start_id = self.find_id(start)
        goal_id = self.find_id(goal)
        longest_path_id = self.dfs_longest_path(
            start_id, goal_id, self.bfs_check_availability(start_id))
        self.assert_path(longest_path_id, start, goal)
        longest_path_title = []
        count = 0
        for id in longest_path_id:  # titleに変換
            longest_path_title.append(self.titles[id])
            count += 1  # pathの単語数をカウント
        print(count)
        return longest_path_title

        # Helper function for Homework #3:
        # Please use this function to check if the found path is well formed.
        # 'path': An array of page IDs that stores the found path.
        #     path[0] is the start page. path[-1] is the goal page.
        #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
        #     page to the goal page.
        # 'start': A title of the start page.
        # 'goal': A title of the goal page.

    def assert_path(self, path, start, goal):
        assert (start != goal)
        assert (len(path) >= 2)
        assert (self.titles[path[0]] == start)
        assert (self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert (path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_path("池袋", "渋谷")
