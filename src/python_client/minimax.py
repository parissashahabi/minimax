import random
from base import Action


def evaluation_function(current_game_state):  # TODO
    # print(current_game_state[1])
    values = [value for value in range(20)]
    return random.choice(values)


def map_action(action):
    if action == 0:  # LEFT
        return Action.LEFT
    elif action == 1:  # DOWN LEFT
        return Action.DOWN_LEFT
    elif action == 2:  # DOWN
        return Action.DOWN
    elif action == 3:  # DOWN RIGHT
        return Action.DOWN_RIGHT
    elif action == 4:  # RIGHT
        return Action.RIGHT
    elif action == 5:  # UP RIGHT
        return Action.UP_RIGHT
    elif action == 6:  # UP
        return Action.UP
    elif action == 7:  # UP LEFT
        return Action.UP_LEFT
    elif action == 8:  # NOOP
        return Action.NOOP


class MinimaxAgent:
    def __init__(self, height, width, forbidden_cells, depth=2):
        self.dRow = [0, 1, 1, 1, 0, -1, -1, -1, 0]
        self.dCol = [-1, -1, 0, 1, 1, 1, 0, -1, 0]
        self.forbidden_cells = forbidden_cells
        self.width = width
        self.height = height
        self.depth = depth
        self.path = []

    def minimax(self, agent, depth, game_state):
        if self.is_terminated(game_state[0]) or depth == self.depth:
            return evaluation_function(game_state)
        if agent == 'A':  # maximize for agent
            # self.path.append(self.get_agent_type())
            return min(self.minimax('B', depth, self.generate_successor(game_state, agent, action)) for action in
                       self.get_legal_actions('B', game_state[0]))
        elif agent == 'B':
            depth += 1
            return max(self.minimax('A', depth, self.generate_successor(game_state, agent, action)) for action in
                       self.get_legal_actions('A', game_state[0]))

    def get_action(self, game_state):
        # print(f'game state:\n{game_state}\n')
        # print(f'game state[0]:\n{game_state[0]}\n')
        # print(f'game state[1]:\n{game_state[1]}\n')
        possible_actions = self.get_legal_actions('A', game_state[0])
        action_scores = [self.minimax('A', 0, self.generate_successor(game_state, 'A', action)) for action
                         in possible_actions]
        max_action = max(action_scores)
        max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
        chosen_index = random.choice(max_indices)
        return map_action(possible_actions[chosen_index])

    def is_valid(self, row, col):
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return False
        return True

    def get_agent_location(self, agent, game_state):
        for x in range(self.height):
            for y in range(self.width):
                if agent in game_state[x][y]:
                    return x, y

    def get_agent_type(self, agent, game_state):
        for x in range(self.height):
            for y in range(self.width):
                if agent in game_state[x][y]:
                    return game_state[x][y]

    def get_legal_actions(self, agent, game_state):
        legal_actions = []
        x, y = self.get_agent_location(agent, game_state)
        for i in range(9):
            adj_x = x + self.dRow[i]
            adj_y = y + self.dCol[i]
            if self.is_valid(adj_x, adj_y) and not game_state[adj_x][adj_y] in self.forbidden_cells:
                legal_actions.append(i)
        return legal_actions

    def generate_successor(self, game_state, agent, action):
        grid = game_state[0]
        successor_state = grid
        x, y = self.get_agent_location(agent, grid)
        adj_x = x + self.dRow[action]
        adj_y = y + self.dCol[action]
        if self.is_valid(adj_x, adj_y) and not grid[adj_x][adj_y] in ['W']:
            adj_type = grid[adj_x][adj_y]
            if 'A' not in adj_type or 'B' not in adj_type:
                game_state[1].append(adj_type)
                if adj_type in ['1', '2', '3', '4', 'r', 'g', 'y']:
                    successor_state[adj_x][adj_y] = 'E' + agent
                else:
                    successor_state[adj_x][adj_y] = successor_state[adj_x][adj_y] + agent
            else:
                return successor_state
            successor_state[x][y] = successor_state[x][y].replace(agent, '')
        return successor_state

    def is_terminated(self, game_state):  # TODO
        pass
