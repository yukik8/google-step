#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# 距離が近い都市の組み合わせを返す
def near_list(dist):
    N = len(dist)
    near = []
    for i in range(N):
        neighbors = sorted(
            range(N), key=lambda j: dist[i][j] if i != j else float('inf'))  # 同じcity同士は含めないために距離を無限に設定
        near.append(neighbors[:N//2])   # 距離が近い順上位N//2個を返す
    return near


# 2-opt法
def two_opt(tour: list[int], dist: list[list[int]]):
    near = near_list(dist)
    improved = True

    while improved:  # 改善がある間繰り返す
        improved = False
        for i in range(len(tour)-2):
            for j in near[tour[i+1]]:
                if j <= i + 1 or j + 2 > len(tour):
                    continue
                else:
                    # 　変更前後の距離を算出
                    current_dist = dist[tour[i]][tour[i+1]
                                                 ] + dist[tour[j]][tour[j+1]]
                    new_dist = dist[tour[i]][tour[j]] + \
                        dist[tour[i+1]][tour[j+1]]
                    #  変更前後で距離が短くなる場合、その区間を逆順にする
                    if current_dist > new_dist:
                        tour[i+1:j+1] = reversed(tour[i+1:j+1])
                        improved = True
                        break
            if improved:
                break
    return tour


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        # 現在の都市から最も近い未訪問cityを探して追加
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return two_opt(tour, dist)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
