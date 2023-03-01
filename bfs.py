import json
import math
import argparse

def read_inputs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("graph_file", type=str)
    argparser.add_argument("truth_path", type=str)
    argparser.add_argument("num_slices", type=int)
    argparser.add_argument("mode", type=str)
    args = argparser.parse_args()
    return args.graph_file, args.truth_path, args.num_slices, args.mode

def process_graph(graph_file):
    curr_src_id = -1
    curr_edge_index = 0
    curr_num_edges = 0
    max_dst_id = -1

    edge_indices = []
    edges = []

    src_id = -1
    dst_id = -1

    for line in graph_file.readlines():
        src_id, dst_id = line.split()
        src_id = int(src_id)
        dst_id = int(dst_id)

        if dst_id > max_dst_id:
            max_dst_id = dst_id

        if src_id != curr_src_id:
            if curr_src_id != -1:
                edge_indices.append(curr_edge_index)
                curr_edge_index += curr_num_edges
                curr_num_edges = 0
            for _ in range(curr_src_id + 1, src_id):
                edge_indices.append(curr_edge_index)
            curr_src_id = src_id
            edges.append(dst_id)
            curr_num_edges += 1
        else:
            edges.append(dst_id)
            curr_num_edges += 1
    edge_indices.append(curr_edge_index)
    curr_edge_index += curr_num_edges

    for _ in range(src_id + 1, max_dst_id + 1):
        edge_indices.append(curr_edge_index)
    return edge_indices, edges

def bfs(edge_indices, edges):
    heights = [1000 for _ in range(len(edge_indices))]
    frontier = [0]
    heights[0] = 0

    while True:
        next_frontier = []
        for curr_id in frontier:
            start = edge_indices[curr_id]
            if (curr_id != len(edge_indices) - 1):
                end = edge_indices[curr_id + 1]
            else:
                end = len(edge_indices)
            curr_edges = edges[start : end]

            for edge in curr_edges:
                if heights[edge] > (heights[curr_id] + 1):
                    heights[edge] = heights[curr_id] + 1
                    next_frontier.append(edge)
        frontier = next_frontier
        if len(frontier) == 0:
            break
    return heights

def bfs_graph_sync(edge_indices, edges, num_slices, slice_size):
    heights = [1000 for _ in range(len(edge_indices))]
    temp_heights = [1000 for _ in range(len(edge_indices))]
    frontier = [[]  for _ in range(num_slices)]
    frontier[0] = [0]
    heights[0] = 0
    count = 0
    slices = 1
    while True:
        for slice in range(num_slices):
            next_frontier = []
            if (len(frontier[slice]) == 0):
                continue
            slices += 1
            for curr_id in frontier[slice]:
                start = edge_indices[curr_id]
                if (curr_id != len(edge_indices) - 1):
                    end = edge_indices[curr_id + 1]
                else:
                    end = len(edge_indices)
                curr_edges = edges[start : end]
                for edge in curr_edges:
                    slice_index = math.floor(edge/slice_size)
                    if temp_heights[edge] > (heights[curr_id] + 1):
                        temp_heights[edge] = heights[curr_id] + 1
                        if slice_index == slice:
                            next_frontier.append(edge)
                        else:
                            frontier[slice_index].append(edge)
            frontier[slice] = next_frontier
            count = 0
            for f in frontier:
                # print(f)
                if len(f) == 0:
                    count += 1
            if count == len(frontier):
                break
        for i in range(len(edge_indices)):
                if (heights[i] > temp_heights[i]):
                    heights[i] = temp_heights[i]
        if count == len(frontier):
            break
    print(f"Number of slices: {num_slices}. Slice size: {slice_size} with mode: {mode}. Total number of slices switching: {slices}")
    return heights

def bfs_slice_sync(edge_indices, edges, num_slices, slice_size):
    heights = [1000 for _ in range(len(edge_indices))]
    temp_heights = [1000 for _ in range(len(edge_indices))]
    frontier = [[]  for _ in range(num_slices)]
    frontier[0] = [0]
    heights[0] = 0
    count = 0
    slices = 1
    while True:
        for slice in range(num_slices):
            next_frontier = []
            if (len(frontier[slice]) == 0):
                continue
            slices += 1
            for curr_id in frontier[slice]:
                start = edge_indices[curr_id]
                if (curr_id != len(edge_indices) - 1):
                    end = edge_indices[curr_id + 1]
                else:
                    end = len(edge_indices)
                curr_edges = edges[start : end]
                for edge in curr_edges:
                    slice_index = math.floor(edge/slice_size)
                    if temp_heights[edge] > (heights[curr_id] + 1):
                        temp_heights[edge] = heights[curr_id] + 1
                        if slice_index == slice:
                            next_frontier.append(edge)
                        else:
                            frontier[slice_index].append(edge)
            for i in range(len(edge_indices)):
                if (heights[i] > temp_heights[i]):
                    heights[i] = temp_heights[i]
            frontier[slice] = next_frontier
            count = 0
            for f in frontier:
                if len(f) == 0:
                    count += 1
            if count == len(frontier):
                break
        if count == len(frontier):
            break
    print(f"Number of slices: {num_slices}. Slice size: {slice_size} with mode: {mode}. Total number of slices switching: {slices}")
    return heights

def bfs_async_slice(edge_indices, edges, num_slices, slice_size):
    heights = [1000 for _ in range(len(edge_indices))]
    frontier = [[]  for _ in range(num_slices)]
    frontier[0] = [0]
    heights[0] = 0
    count = 0
    slices = 1
    while True:
        for slice in range(num_slices):
            if (len(frontier[slice]) == 0):
                continue
            slices += 1
            for curr_id in frontier[slice]:
                start = edge_indices[curr_id]
                if (curr_id != len(edge_indices) - 1):
                    end = edge_indices[curr_id + 1]
                else:
                    end = len(edge_indices)
                curr_edges = edges[start : end]
                for edge in curr_edges:
                    slice_index = math.floor(edge/slice_size)
                    if heights[edge] > (heights[curr_id] + 1):
                        heights[edge] = heights[curr_id] + 1
                        if slice_index == slice:
                            frontier[slice].append(edge)
                        else:
                            frontier[slice_index].append(edge)
            frontier[slice] = []
            count = 0
            for f in frontier:
                if len(f) == 0:
                    count += 1
            if count == len(frontier):
                break
        if count == len(frontier):
            break
    print(f"Number of slices: {num_slices}. Slice size: {slice_size} with mode: {mode}. Total number of slices switching: {slices}")
    return heights

if __name__ == "__main__":

    graph_file_name, truth_file_path, num_slices, mode = read_inputs()

    edge_indices = []
    edges = []
    with open(graph_file_name, "r") as graph_file:
        edge_indices, edges = process_graph(graph_file)

    num_vertex_slice = math.ceil(float(len(edge_indices)/num_slices))

    if (mode == "sliced"):
        heights = bfs_slice_sync(edge_indices, edges, num_slices, num_vertex_slice)
    elif (mode == "graph"):
        heights = bfs_graph_sync(edge_indices, edges, num_slices, num_vertex_slice)
    elif (mode == "async"):
        heights = bfs_async_slice(edge_indices, edges, num_slices, num_vertex_slice)
   

    with open(f"{truth_file_path}/truth.json", "w") as truth_file:
        json.dump(heights, truth_file)
