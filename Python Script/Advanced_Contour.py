import cv2
import numpy as np
from collections import defaultdict

def error(p1, p2):
    erx = abs(p1[0] - p2[0])
    ery = abs(p1[1] - p2[1])
    return max(erx, ery)

def find_nearest_point(target, candidates, threshold=10):
    """Find the nearest point in candidates to target within threshold"""
    min_dist = float('inf')
    nearest = None
    for candidate in candidates:
        dist = error(target, candidate)
        if dist < min_dist and dist < threshold:
            min_dist = dist
            nearest = candidate
    return nearest

def normalize_point(point, all_points, threshold=10):
    """Normalize a point to match existing points in the graph"""
    nearest = find_nearest_point(point, all_points, threshold)
    return nearest if nearest else point

def build_graph(pairs, all_points, threshold=10):
    """Build adjacency list from line pairs"""
    graph = defaultdict(list)
    
    for p1, p2 in pairs:
        # Normalize points to handle small coordinate differences
        p1_norm = normalize_point(p1, all_points, threshold)
        p2_norm = normalize_point(p2, all_points, threshold)
        
        graph[p1_norm].append(p2_norm)
        graph[p2_norm].append(p1_norm)
    
    return graph

def find_path_with_backtracking(graph, start_point, end_point):
    """Find path that covers all edges, including backtracking for dead ends"""
    edges_used = set()
    path = [start_point]
    total_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    def make_edge_key(p1, p2):
        return tuple(sorted([p1, p2], key=lambda x: (x[0], x[1])))
    
    def get_unused_neighbors(node):
        neighbors = []
        for neighbor in graph[node]:
            edge_key = make_edge_key(node, neighbor)
            if edge_key not in edges_used:
                neighbors.append(neighbor)
        return neighbors
    
    def dfs(node, parent=None):
        neighbors = get_unused_neighbors(node)
        # Sort to prefer nodes with more unused connections (avoid dead ends early)
        neighbors.sort(key=lambda n: -len(get_unused_neighbors(n)))
        
        for neighbor in neighbors:
            edge_key = make_edge_key(node, neighbor)
            
            if edge_key not in edges_used:
                edges_used.add(edge_key)
                path.append(neighbor)
                dfs(neighbor, parent=node)
        
        # After exploring all neighbors, backtrack to parent if needed
        if parent is not None and len(edges_used) < total_edges:
            path.append(parent)
    
    dfs(start_point)
    return path

image1=cv2.imread("C:/Users/Asus/Downloads/Image5.png")
image=cv2.resize(image1,(470,394))

#Get the pairs of the points joining each line
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh_image = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
pairs=[]

#Lines detection
# Iterate through each contour
for contour in contours:
    # Approximate the contour to a line
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    #print("approx:",approx)
    
    # Find the endpoints
    if len(approx) >= 2:
        start_point = tuple(approx[0][0])  # First point of the contour
        end_point = tuple(approx[-1][0])   # Last point of the contour
        pairs.append([start_point,end_point])

        #cv2.circle(image, start_point, 5, (0, 0, 255), -1)  # Red for start
        #cv2.circle(image, end_point, 5, (0, 255, 0), -1)    # Green for end
        #cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Red color for Start
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Green color for End
lower_green = np.array([70,50, 50])
upper_green = np.array([80, 255, 255])

# Blue color for Turns
lower_blue = np.array([110, 100, 100])
upper_blue = np.array([130, 255, 255])
mask_redt = cv2.inRange(hsv, lower_red, upper_red)

kernel = np.ones((20, 20), np.uint8)
mask_red = cv2.morphologyEx(mask_redt, cv2.MORPH_CLOSE, kernel)

mask_green = cv2.inRange(hsv, lower_green, upper_green)
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

#mask_green = cv2.morphologyEx(mask_redt, cv2.MORPH_CLOSE, kernel)
#mask_blue = cv2.morphologyEx(mask_redt, cv2.MORPH_CLOSE, kernel)
cv2.imshow('red',thresh_image)
cv2.imshow('blue',mask_blue)
cv2.imshow('green',mask_green)

contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def get_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)
    return None

start_point=get_center(contours_red[0])
end_point=get_center(contours_green[0])
turn_points=[get_center(contour_blue) for contour_blue in contours_blue]
#turn_points.reverse()
#print("end",contours_green)

points=[start_point]+turn_points+[end_point]
#print(points)
print(len(pairs))
path1=[start_point]

# Build graph from pairs
graph = build_graph(pairs, points)

print("Graph structure:")
for node, neighbors in graph.items():
    print(f"{node}: {neighbors}")

# Find the path with backtracking
path = find_path_with_backtracking(graph, start_point, end_point)

print("\n" + "="*50)
print("Path sequence with backtracking:")
print(f"Number of points in path: {len(path)}")
print("="*50)
for i, point in enumerate(path):
    print(f"Step {i}: {point}")

for i in range(0,len(path)-1):
    cv2.arrowedLine(image,path[i],path[i+1],(0,0,255),5)

img1=cv2.resize(image,(480,720))



img=cv2.resize(mask_green,(480,480))
#print(path)
directions = ["S"]
for i in range(1, len(path) - 1):
    p1, p2, p3 = path[i - 1], path[i], path[i + 1]
    
    # Calculate direction (right or left) based on relative position
    if p1 and p2 and p3:
        dx1, dy1 = p2[0] - p1[0], p2[1] - p1[1]
        dx2, dy2 = p3[0] - p2[0], p3[1] - p2[1]
        cross_product = dx1 * dy2 - dy1 * dx2
        print(p1,p2,p3,cross_product)
        if cross_product > 150:
            directions += "R"  # Right turn
        elif cross_product < -150:
            directions += "L"  # Left turn
        elif (cross_product< 150 or cross_product>-150) and (p1!=p3):
            directions += "G" # Go straight
        elif dx1==-dx2 or dy1==-dy2:
            directions += "U" # U turn
directions.append("F")
print(directions)


cv2.imshow("HSV",image)
cv2.waitKey(0)
cv2.destroyAllWindows()