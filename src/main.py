import src.utils as utils

# using this for now; may use command line args in the future.
filename = 'board.txt'
board = []
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        row_text = line.split(',')
        board.append([eval(i) for i in row_text])

utils.solve(board)
utils.print_board(board)
print(utils.check_solution(board))
