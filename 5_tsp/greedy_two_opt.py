#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def near_list(dist):
    N = len(dist)
    near = []
    for i in range(N):
        neighbors = sorted(
            range(N), key=lambda j: dist[i][j] if i != j else float('inf'))
        near.append(neighbors[:N//2])
    return near


def two_opt(tour: list[int], dist: list[list[int]]):
    near = near_list(dist)
    for i in range(len(tour)-2):
        for j in near[tour[i+1]]:
            if j <= i + 1 or j + 2 > len(tour):
                continue
            else:
                current_dist = dist[tour[i]][tour[i+1]] + \
                    dist[tour[j]][tour[j+1]]
                comparison_dist = dist[tour[i]][tour[j]] + \
                    dist[tour[i+1]][tour[j+1]]
                if current_dist > comparison_dist:
                    tour[i+1:j+1] = reversed(tour[i+1:j+1])
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
