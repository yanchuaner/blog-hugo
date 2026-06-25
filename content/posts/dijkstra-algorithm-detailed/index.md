---
title: "最短路算法：Dijkstra 算法详解"
summary: "从原理到实现，深入理解 Dijkstra 最短路径算法。含朴素版、堆优化版、手写二叉堆版三种实现，配合图例与常见陷阱分析。"
date: 2026-06-25
lastmod: 2026-06-25
draft: false
showtoc: true
categories: ["算法"]
tags: ["ACM", "图论", "最短路", "Dijkstra"]
comments: true
---

> 本文是 [ACM 算法训练营](/posts/series-acm/) 系列第 4 篇。前置阅读：[图论基础：图的存储与遍历](/posts/series-acm/03-tu-lun-ji-chu/)。

## 算法介绍

今天我们来学习 Dijkstra 算法，这是图论里最核心的算法之一。它能解决这样一个问题：**给定一个带权有向图，找出从起点到所有其它节点的最短路径**。注意，Dijkstra 只能处理**边权非负**的情况——如果存在负权边，需要用 Bellman-Ford 或 SPFA。

现实中的导航软件、网络路由协议（OSPF），底层都有 Dijkstra 的影子。ACM 竞赛里，最短路的题目占比非常高，Dijkstra 是最短路入门必学的第一课。

## 算法思想

Dijkstra 的核心思想是**贪心**：每次从"尚未确定最短距离"的节点中，选一个"当前距离最小"的节点，把它标记为已确定，然后用它去更新邻居的距离。这个过程叫**松弛（Relaxation）**。

| 步骤 | 操作 | 说明 |
| :---: | ---- | ---- |
| 1 | 初始化 | `dist[start] = 0`，其余节点 `dist = INF` |
| 2 | 选点 | 从未确定集合中选出 `dist` 最小的节点 `u` |
| 3 | 松弛 | 对 `u` 的每条出边 `(u, v, w)`，若 `dist[u] + w < dist[v]`，更新 `dist[v]` |
| 4 | 标记 | 将 `u` 标记为已确定，重复 2-4 直到所有节点确定 |

## 朴素实现 — O(V²)

最直接的写法：每一轮暴力扫描所有节点，找 `dist` 最小的那个。适合**稠密图**（边数接近 V²）。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;
const int INF = 0x3f3f3f3f;

int n, m, s;                          // 点数、边数、起点
int g[MAXN][MAXN];                    // 邻接矩阵，g[u][v] = w
int dist[MAXN];
bool vis[MAXN];                       // 是否已确定

void dijkstra() {
    memset(dist, 0x3f, sizeof(dist));
    dist[s] = 0;

    for (int i = 1; i <= n; i++) {
        // 1. 从未确定节点中选出 dist 最小的
        int u = -1;
        for (int j = 1; j <= n; j++)
            if (!vis[j] && (u == -1 || dist[j] < dist[u]))
                u = j;

        if (dist[u] == INF) break;    // 剩下的节点不可达，提前结束
        vis[u] = true;

        // 2. 用 u 松弛所有邻居
        for (int v = 1; v <= n; v++)
            if (g[u][v] != INF)
                dist[v] = min(dist[v], dist[u] + g[u][v]);
    }
}
```

## 堆优化 — O((V+E) log V)

稀疏图时，暴力扫描 O(V²) 太慢。观察步骤 2——"找最小值的节点"，这正是**优先队列**的强项。用 `priority_queue` 把找点的开销从 O(V) 降到 O(log V)。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const int INF = 0x3f3f3f3f;

struct Edge {
    int to, w;
};

vector<Edge> g[MAXN];                  // 邻接表
int dist[MAXN];
bool vis[MAXN];

void dijkstra(int s) {
    memset(dist, 0x3f, sizeof(dist));
    dist[s] = 0;

    // 小根堆：pair<距离, 节点编号>
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (vis[u]) continue;          // 过期的旧值，跳过
        vis[u] = true;

        for (auto &e : g[u]) {
            int v = e.to, w = e.w;
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v}); // 松弛成功后入堆
            }
        }
    }
}
```

**为什么新入堆而不是修改堆中旧值？** C++ `priority_queue` 不支持 decrease-key 操作。我们直接 push 新值，旧值留在堆底——当它被 pop 时，`vis[u]` 已经在 `true` 状态，直接 `continue` 跳过。这是最常用的写法，简洁且实际效率不差。

## 手写二叉堆 — 支持 decrease-key

如果你真的需要 decrease-key（比如某些卡常题目），可以手写一个最小堆：

```cpp
// 手写最小堆，支持 decrease-key
struct MinHeap {
    pair<int, int> h[MAXN]; // {dist, node}
    int pos[MAXN];          // pos[node] = index in heap, 0 表示不在堆中
    int sz;

    void init() { sz = 0; memset(pos, 0, sizeof(pos)); }

    void swap_node(int i, int j) {
        swap(h[i], h[j]);
        pos[h[i].second] = i;
        pos[h[j].second] = j;
    }

    void push(int node, int d) {
        h[++sz] = {d, node};
        pos[node] = sz;
        int i = sz;
        while (i > 1 && h[i].first < h[i / 2].first) {
            swap_node(i, i / 2);
            i /= 2;
        }
    }

    void decrease_key(int node, int new_d) {
        int i = pos[node];
        if (i == 0) { push(node, new_d); return; }
        h[i].first = new_d;
        while (i > 1 && h[i].first < h[i / 2].first) {
            swap_node(i, i / 2);
            i /= 2;
        }
    }

    pair<int, int> pop() {
        auto res = h[1];
        pos[res.second] = 0;
        h[1] = h[sz--];
        if (sz > 0) {
            pos[h[1].second] = 1;
            int i = 1;
            while (true) {
                int mn = i;
                if (i * 2 <= sz && h[i * 2].first < h[mn].first) mn = i * 2;
                if (i * 2 + 1 <= sz && h[i * 2 + 1].first < h[mn].first) mn = i * 2 + 1;
                if (mn == i) break;
                swap_node(i, mn);
                i = mn;
            }
        }
        return res;
    }
};
```

## 常见易错点

1. **把 Dijkstra 用在负权图上** — 结果是错的。Dijkstra 依赖"当前最小距离不会再被更新"这一性质，负权边会破坏它。有负权请用 Bellman-Ford 或 SPFA。
2. **INF 溢出** — `dist[u] + w` 时若 `dist[u] = INF`（比如 `0x3f3f3f3f`），加一个正权会溢出成负数。写法上需要判断 `dist[u] != INF` 或使用 `long long`。
3. **vis 标记时机** — vis 应该在**出队时**标记，而不是入队时。同一个节点可能多次入队（不同距离），只有第一次 pop 的时候才真正确定。
4. **重边处理** — 邻接矩阵写法需要取 `min(g[u][v], w)`，邻接表则不需要，因为每条边独立存储。
5. **堆中节点被多次 push** — 如前所述，这是预期行为，`vis` 检查即可过滤。

## 复杂度对比

| 实现方式 | 时间复杂度 | 适用场景 |
| -------- | -------- | -------- |
| 朴素 O(V²) | O(V²) | 稠密图，V ≤ 1000 |
| STL 堆 | O((V+E) log V) | 稀疏图，通用首选 |
| 手写二叉堆 | O((V+E) log V) | 需要 decrease-key，常数更小 |
| Fibonacci 堆 | O(E + V log V) | 理论上最优，竞赛中几乎不用（常数大） |

## 实战题目推荐

- **P3371 【模板】单源最短路径（弱化版）** — 直接套板子
- **P4779 【模板】单源最短路径（标准版）** — 必须用堆优化
- **P1339 [USACO09OCT] Heat Wave** — 简单应用
- **P1144 最短路计数** — Dijkstra + DP 计数

## 总结

Dijkstra 算法虽然思想上很直观——贪心地每次取最近节点进行松弛——但真正写对、写好，还是有不少细节需要注意。今天主要掌握三点：**邻接表建图 + priority_queue 堆优化 + vis 去重**，这是竞赛中最实用的写法。

感觉 Dijkstra 算法还是有一定难度的，尤其是手写堆部分和负权边边界条件。下次继续学习 Bellman-Ford 和 SPFA，把最短路这一块彻底吃透。