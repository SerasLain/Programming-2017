def get_graf():
    with open('input.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    graf_arr = [list(map(int, line.split(' '))) for line in lines]
    n, m = graf_arr[0][0], graf_arr[0][1]
    graf_arr.pop(0)
    return (n, m, graf_arr)

def make_graf_dict(n, graf_arr):
    dictionary = {}
    for l in range(n):
        dictionary[l] = set()
    for i in graf_arr:
        dictionary[i[0]].add(i[1])
    return dictionary


def find(graf, n):
    Visited = [False] * (n + 1)
    def DFS(start):
        Visited[start] = True
        for v in graf[start]:
            if not Visited[v]:
                DFS(v)
    ncomp = 0
    for i in range(1, n + 1):
        if not Visited[i]:
            ncomp += 1
            DFS(i)


def find_components(graf_dict):
    queue = []
    visited = {}
    for i in graf_dict:
        visited


def make_matrix(graf):
    n = graf[0]
    e = graf[2]
    arr_lines = []
    while n != 0:
        arr_lines.append(list('0'*graf[0]))
        n -= 1
    for i in e:
        row = i[0] - 1
        col = i[1] - 1
        arr_lines[row][col] = '1'
        arr_lines[col][row] = '1'
    return arr_lines

def write_matrix(arr_lines):
    lines = [' '.join(line) for line in arr_lines]
    with open('output.txt', 'w', encoding = 'utf-8') as f:
        f.write('\n'.join(lines).strip())


def parse_matrix():
    with open('input.txt', 'r', encoding='utf-8') as f:
        matrix = f.readlines()
    return (matrix[0], matrix[1::])

def count_v(matrix):
    arr_counts = []
    for i in matrix[1]:
        n = sum(list(map(int, i.split(' '))))
        arr_counts.append(str(n))
    return '\n'.join(arr_counts)

def write_result(string):
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(string)


def main():
    graf = get_graf()
    print(make_graf_dict(graf[0], graf[2]))

if __name__ == '__main__':
    main()


