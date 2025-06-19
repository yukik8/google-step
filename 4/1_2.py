import sys
import collections
from collections import deque
from collections import defaultdict


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

    # Example: Find the longest titles.

    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Example: Find the most linked pages.

    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # titleから対応するidを見つける
    def find_id(self, target_title):
        for id, title in self.titles.items():
            if title == target_title:
                return id
        raise ValueError('not found the title')

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    def find_shortest_path(self, start, goal):
        # ------------------------#
        # Write your code here!  #
        start_id = self.find_id(start)
        goal_id = self.find_id(goal)
        queue = deque([start_id])   # 探索中のノード集合
        checked_nodes = set()
        node_to_root = {}
        node = goal_id
        path = []
        while queue:
            current = queue.popleft()   # dequeue
            if current == goal_id:  # goalを見つけたら終了
                break
            for link in self.links[current]:    # currentから辿れるlinkを探索
                if link not in checked_nodes:   # check済みでなかった場合、check済みに更新してqueueに追加
                    checked_nodes.add(link)
                    queue.append(link)
                    node_to_root[link] = current    # nodeの親を辞書に保存
        while node != start_id:  # nodeの親を辿ってpathを再現
            path.append(self.titles[node])
            node = node_to_root[node]
        path.append(self.titles[start_id])
        path.reverse()
        print(f'Shortest path: {path}')
        return path

        # ------------------------#

    # Homework #2: Calculate the page ranks and print the most popular pages.

    def find_most_popular_pages(self):
        # ------------------------#
        # Write your code here!  #
        id_to_rank = {id: 1.0 for id in self.titles}
        difference = 1
        while difference > 0.1:
            old_ranks = id_to_rank.copy()
            id_to_rank = {id: (1 - 0.85) / len(self.titles)
                          for id in self.titles}
            for index, links in self.links.items():
                if len(links) != 0:
                    next_share = old_ranks[index] * \
                        0.85 / len(links)  # 隣接するノード
                    for link_id in links:
                        id_to_rank[link_id] += next_share
                else:
                    share = old_ranks[index] * 0.85 / \
                        len(self.titles)  # すでに15%分配済み
                    for id in self.titles:
                        id_to_rank[id] += share
            difference = sum((old_ranks[id] - id_to_rank[id])**2
                             for id in self.titles)
            print(difference)
            sorted_ranks = sorted(id_to_rank.items(),
                                  key=lambda x: x[1], reverse=True)
            for i in range(10):
                print(sorted_ranks[i], self.titles[sorted_ranks[i][0]])

        # ------------------------#

    def bfs_check_availability(self, start_id):
        queue = deque([start_id])   # 探索中のノード集合
        checked_nodes = set()
        while queue:
            current = queue.popleft()
            for link in self.links[current]:
                if link not in checked_nodes:
                    checked_nodes.add(link)
                    queue.append(link)
        return checked_nodes

    def dfs_longest_path(self, start_id, goal_id, nodes):
        longest_path = []
        current = start_id
        path = [start_id]
        checked_nodes = set([start_id])
        stack = [(start_id, path, checked_nodes)]
        while stack:
            current, path, checked_nodes = stack.pop()
            if current == goal_id:
                if len(path) > len(longest_path):
                    longest_path = path
                continue
            for neighbour in self.links[current]:
                if neighbour not in checked_nodes and neighbour in nodes:
                    new_checked_nodes = checked_nodes | {neighbour}  # 和演算
                    new_path = path + [neighbour]  # pathにneighbourを追加した新しいリスト
                    stack.append((neighbour, new_path, new_checked_nodes))
            len(stack)
        return longest_path

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    # メモリが大きすぎてクラッシュしてしまう
    def find_longest_path(self, start, goal):
        # ------------------------#
        # Write your code here!  #
        # BFS
        start_id = self.find_id(start)
        goal_id = self.find_id(goal)
        nodes = self.bfs_check_availability(start_id)
        print(nodes)
        longest_path = self.dfs_longest_path(goal_id, start_id, nodes)
        print(longest_path)
        return longest_path

        # ------------------------#

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
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")
