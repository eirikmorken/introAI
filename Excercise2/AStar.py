import math, numpy
from PIL import Image
import heapq

inf = math.inf


def main():  #Takes inn file from python directory and excecutes a* algorythm
    node_matrix = read_file("board-2-4.txt")
    board = Board(node_matrix)
    board.a_star()


class Node(object):
    def __init__(self, letter, value, x_pos, y_pos):
        self.letter = letter
        self.value = value
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.parent = None
        self.distance = None
        self.path_cost = inf

    def __str__(self):
        return str(self.letter)

    def __lt__(self, other): #Overiding less than variable, so i can order nodes in heapq
        return self.value + self.distance*0.9 < other.value + other.distance*0.9


class Board(object):
    def __init__(self, node_matrix):
        self.node_matrix = node_matrix
        self.height = len(node_matrix)
        self.width = len(node_matrix[0])
        self.walls = []
        self.child_heap = []
        self.visited = []
        for line in node_matrix:
            for node in line:
                if node.letter == '#':
                    self.walls.append((node.x_pos, node.y_pos)) #Noting all walls so i dont have to search them
                elif node.letter == 'A':
                    self.start_node = node
                    node.path_cost = 0
                elif node.letter == 'B':
                    self.target = node

    def a_star(self):
        heapq.heappush(self.child_heap, self.start_node)  #Adding startnode to OPEN
        while True:
            if len(self.child_heap) <= 0:  #Check if all children are
                print("fail")
                break
            search_node = heapq.heappop(self.child_heap)  #Extracts first item in priority queue
            if search_node is self.target:
                print("Node found")
                print(search_node.path_cost)
                self.path_img(self.getPath(search_node))  #Genereate img
                break
            self.visited.append(search_node)  #Keeps track of visited nodes
            self.get_children((search_node.x_pos, search_node.y_pos))


    '''Most of the logic is done here. Pushes all newly discovered children on a heapq.
    recalculates path if node already is visited.'''
    def get_children(self, node):
        (x, y) = node
        children = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        children = filter(self.not_edge, children)  #Filters out out_bound nodes
        children = filter(self.not_wall, children)  #Filters out walls
        for child_xy in children:
            child = self.node_matrix[child_xy[1]][child_xy[0]]
            if (child not in self.visited) and (child not in self.child_heap):
                child.distance = self.distance(child)
                child.parent = self.node_matrix[y][x]
                child.path_cost = self.node_matrix[y][x].path_cost + child.value
                heapq.heappush(self.child_heap, child)
            elif child in self.visited:
                if child.path_cost > self.node_matrix[y][x].path_cost:
                    child.path_cost = self.node_matrix[y][x].path_cost
                    child.parent = self.node_matrix[y][x]
                    heapq.heappush(self.child_heap, child)
                    self.visited.remove(child)

                    # child.path_cost = min(child.path_cost, self.node_matrix[y][x].path_cost + child.value)

    def getPath(self, node):  #Gets path by "asking up the tree"
        path = [node]
        while node.parent is not None:
            path.append(node.parent)
            node = node.parent
        return path

    def distance(self, current_node): #Gets Manhatten distance
        x0 = self.target.x_pos
        y0 = self.target.y_pos
        (x, y) = (current_node.x_pos, current_node.y_pos)
        dx = abs(x - x0)
        dy = abs(y - y0)
        return dx + dy

    def not_edge(self, node): #Checks if a node is in the board
        (x, y) = node
        return 0 <= x < self.width and 0 <= y < self.height

    def not_wall(self, node): #Checks if node is wall
        return node not in self.walls

    def getColor(self, node):  # Returns a color for each node type
        Water = [0, 0, 255]
        Mountain = [128, 128, 128]
        Forest = [0, 102, 0]
        Grasslands = [0, 255, 0]
        Roads = [153, 102, 51]
        StartFinish = [255, 102, 255]
        Wall = [150, 150, 105]
        Dot = [255, 255, 255]

        def letter_to_color(char):  #Maps color to letter.
            return {
                'A': StartFinish,
                'B': StartFinish,
                '.': Dot,
                'w': Water,
                'm': Mountain,
                'f': Forest,
                'g': Grasslands,
                'r': Roads,
                '#': Wall,
            }[char]
        return letter_to_color(node.letter)

    def path_img(self, path):  #Genereates image using PIL Image. First painting board using all the nodes,
        size = 10                                                 #then adding the path on the board.
        w, h = self.width * size, self.height * size
        data = numpy.zeros((h, w, 3), dtype=numpy.uint8)
        for node_row in self.node_matrix:
            for node in node_row:
                for i in range(size):
                    for i2 in range(size):
                        data[node.y_pos * size + i, node.x_pos * size + i2] = self.getColor(node)  #Creating board
        for path_node in path:
            data[path_node.y_pos * size + size // 2, path_node.x_pos * size + size // 2] = [0, 0, 0]  #Adding path
        img = Image.fromarray(data, 'RGB')
        img.show()


def read_file(file):
    def get_cost(char): #Maps character to value
        return {
            'A': inf,
            'B': 0,
            '.': 1,
            'w': 100,
            'm': 50,
            'f': 10,
            'g': 5,
            'r': 1,
            '#': inf,
        }[char]

    f = open(file, "r")
    lines = [line.strip() for line in f]
    f.close()

    node_matrix = []
    for y in range(len(lines)):
        new_line = []
        for x in range(len(lines[y])):
            letter = lines[y][x]
            new_line.append(Node(letter, get_cost(letter), x, y))  #Creates nodeobjects and puts them in a matrix
        node_matrix.append(new_line)
    return node_matrix


if __name__ == '__main__':
    main()
