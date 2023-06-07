from pydantic import BaseModel
from typing import List, Tuple, Dict, Optional, Union
from collections import namedtuple
import pandas as pd
from os import path
from itertools import permutations

ACROSS = 'across'
DOWN = 'down'

Position = namedtuple('Position', ['i', 'j'])
BoardVariable = namedtuple(
    'BoardVariable', ['i', 'j', 'index', 'orientation', 'length'])
PromptVariable = namedtuple(
    'PromptVariable', ['orientation', 'index', 'prompt', 'length'])


class Clue():
    pass

# declare variable class


class Variable():
    pass


class Crossword():
    def __init__(self, board_filepath: str, prompts_filepath: str) -> None:
        self.board, variable_positions = read_board(board_filepath)
        prompts = read_prompts(prompts_filepath)
        self.variables = combine_board_and_prompts(variable_positions, prompts)
        self.setup_intersections()

    def setup_intersections(self):
        self.intersections = dict()
        # loop through all the variables
        for v1, v2 in permutations(self.variables, 2):
            v1_cells = v1.cells
            v2_cells = v2.cells
            # check if they intersect
            intersection = set(v1_cells).intersection(set(v2_cells))
            if intersection:
                # add to the intersections dict
                intersection = intersection.pop()
                self.intersections[v1, v2] = (
                    v1_cells.index(intersection),
                    v2_cells.index(intersection)
                )

    def neighbours(self, var: Variable) -> List[Variable]:
        neighbours = []
        for v1, v2 in self.intersections.keys():
            if v1 == var:
                neighbours.append(v2)
            elif v2 == var:
                neighbours.append(v1)
        return neighbours


class Variable():

    def __init__(self,
                 pos: Position,
                 index: int,
                 orientation: str,
                 length: Union[int, Tuple[int, int]], prompt: str) -> None:
        # let's setup the values
        self.pos = pos
        self.index = index
        self.orientation = orientation
        self.length = length
        self.prompt = prompt

        # validate the values
        if not self.validate():
            raise ValueError("Invalid variable")

        self.setup_cells()

    def validate(self) -> bool:
        # check the orientation
        if self.orientation not in [ACROSS, DOWN]:
            print("orientation not in ['across', 'down']")
            return False
        # check the length
        if isinstance(self.length, int) and self.length < 3:
            print("length < 3")
            return False
        if isinstance(
            self.length,
            tuple) and (
            self.length[0] +
                self.length[1] < 3):
            print("length < 3")
            return False
        # check the prompt
        if len(self.prompt) < 1:
            print("len(prompt) < 1")
            return False
        # check i, j, index are ints
        if not isinstance(
                self.pos.i,
                int) or not isinstance(
                self.pos.i,
                int) or not isinstance(
                self.index,
                int):
            print("i, j, index not ints")
            return False
        return True

    def setup_cells(self) -> None:
        # setup the cells
        if self.orientation == ACROSS:
            self.cells = [(self.pos.i, self.pos.j + k)
                          for k in range(self.length)]
        elif self.orientation == DOWN:
            self.cells = [(self.pos.i + k, self.pos.j)
                          for k in range(self.length)]
        return

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'Variable(coordinate: ({self.pos.i}, {self.pos.j}),\
                    \norientation: {self.orientation},\
                    \nlength: {self.length},\
                    \nprompt: {self.prompt})'

    def __hash__(self) -> int:
        return hash((self.pos, self.orientation, self.length))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()


def read_board(filepath: str) -> List[List[str]]:

    def get_variable_length(board, pos, orientation):
        rows = len(board)
        cols = len(board[0])
        length = 1
        if orientation == ACROSS:
            for j in range(pos.j + 1, cols):
                if board[pos.i][j]:
                    length += 1
                else:
                    break
        elif orientation == DOWN:
            for i in range(pos.i + 1, rows):
                if board[i][pos.j]:
                    length += 1
                else:
                    break
        return length

    def is_start_of_variable(board, pos) -> List:

        starts = []
        if board[pos.i][pos.j] and (pos.i == 0 or not board[pos.i - 1][pos.j]):
            starts.append(DOWN)
        if board[pos.i][pos.j] and (pos.j == 0 or not board[pos.i][pos.j - 1]):
            starts.append(ACROSS)
        return starts

    with open(filepath, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    rows = len(lines)
    cols = len(lines[0])
    board = []
    # make board
    for i in range(rows):
        board.append([])
        for j in range(cols):
            board[i].append(True if lines[i][j] == '_' else False)
    # need to find the position of the variables

    board_variables = []
    index = 1
    for i in range(rows):
        for j in range(cols):
            appended = False
            if is_start_of_variable(board, Position(i, j)):
                for orientation in is_start_of_variable(board, Position(i, j)):
                    length = get_variable_length(
                        board, Position(i, j), orientation)
                    if length > 1:
                        board_variables.append(BoardVariable(
                            i, j, index, orientation, length))
                        appended = True
                if appended:
                    index += 1

    return board, board_variables


def read_prompts(filepath: str) -> List[PromptVariable]:
    # now we need to read in the prompts
    df = pd.read_csv(filepath, escapechar="\\")
    prompts = []
    for _, row in df.iterrows():
        index = int(row['index'])
        # handle tuples for length
        length = row['length']
        if '(' in length:
            # remove the parentheses
            length = length[1:-1]
            # split on comma
            length = length.split(',')
            # convert to ints
            length = tuple([int(x) for x in length])
        else:
            length = int(length)
        # handle orientations
        orientation = DOWN if row['orientation'] == 'D' else ACROSS

        prompts.append(PromptVariable(
            orientation, index, row['prompt'], length))
    return prompts


def match_prompt_to_position(
        board_var: BoardVariable,
        prompt: PromptVariable) -> bool:
    index = board_var.index
    orientation = board_var.orientation
    # find corresponding prompt
    if index == prompt.index and orientation == prompt.orientation:
        return True


def combine_board_and_prompts(
        board_vars: List[BoardVariable],
        prompts: List[PromptVariable]) -> List[Variable]:
    variables = []
    for board_var in board_vars:
        for prompt in prompts:
            if match_prompt_to_position(board_var, prompt):
                variables.append(
                    Variable(
                        Position(
                            board_var.i,
                            board_var.j),
                        board_var.index,
                        board_var.orientation,
                        board_var.length,
                        prompt.prompt))

    return variables


def main():

    puzzle = 'puzzle1'
    board_filepath = path.join('puzzles', puzzle, 'board.txt')
    prompts_filepath = path.join('puzzles', puzzle, 'prompts.csv')

    # variable_positions = read_board(board_filepath)
    # prompts = read_prompts(prompts_filepath)
    # variables = combine_board_and_prompts(variable_positions, prompts)
    # for variable in variables:
    #     print(variable)
    # return

    crossword = Crossword(board_filepath, prompts_filepath)
    return


if __name__ == "__main__":
    main()
