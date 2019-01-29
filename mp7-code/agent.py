import utils
import random
import numpy as np
import math

class Agent:
    def learning_rate(self, state):
        if self.two_sided:
            C = 1000
        else:
            C = 1000
        return C/(C+self.N[state[0],state[1],state[2],state[3],state[4],state[5]])

    def __init__(self, actions, two_sided=False):
        self.two_sided = False
        self._actions = actions
        self._train = True
        self._x_bins = utils.X_BINS
        self._y_bins = utils.Y_BINS
        self._v_x = utils.V_X
        self._v_y = utils.V_Y
        self._paddle_locations = utils.PADDLE_LOCATIONS
        self._num_actions = utils.NUM_ACTIONS
        # Create the Q Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        self.last_state = None
        self.games = 0
        self.prev_bounce = 0


    def act(self, state, bounces, done, won):
        action = self._actions[0]
        disc_state = self.discretize(state)
        if self.two_sided:
            gamma = 0.6
            if self._train:
                if self.last_state:
                    reward = self.get_reward(bounces,done,won)
                    alpha = self.learning_rate(self.last_state)
                    best_next_action = self.best_next(disc_state)
                    best_next_value = self.Q[disc_state[0],disc_state[1],disc_state[2],disc_state[3],disc_state[4],self.action_to_index(best_next_action)]
                    curr = self.Q[self.last_state[0],self.last_state[1],self.last_state[2],self.last_state[3],self.last_state[4],self.last_state[5]]
                    self.Q[self.last_state[0],self.last_state[1],self.last_state[2],self.last_state[3],self.last_state[4],self.last_state[5]] += alpha * (reward + gamma*(best_next_value-curr))
                self.prev_bounce= bounces
                action = self.chose_next(disc_state)
                disc_state.append(self.action_to_index(action))
                self.inc_n(disc_state)
                self.last_state = disc_state
            else:
                action = self.best_next(disc_state)
            return action

        else:
            gamma = 0.6
            if self._train:
                if self.last_state:
                    reward = self.get_reward(bounces,done,won)
                    alpha = self.learning_rate(self.last_state)
                    best_next_action = self.best_next(disc_state)
                    best_next_value = self.Q[disc_state[0],disc_state[1],disc_state[2],disc_state[3],disc_state[4],self.action_to_index(best_next_action)]
                    curr = self.Q[self.last_state[0],self.last_state[1],self.last_state[2],self.last_state[3],self.last_state[4],self.last_state[5]]
                    self.Q[self.last_state[0],self.last_state[1],self.last_state[2],self.last_state[3],self.last_state[4],self.last_state[5]] += alpha * (reward + gamma*(best_next_value-curr))
                self.prev_bounce= bounces
                action = self.chose_next(disc_state)
                disc_state.append(self.action_to_index(action))
                self.inc_n(disc_state)
                self.last_state = disc_state
            else:
                action = self.best_next(disc_state)
            return action

    def get_reward(self, bounces, done, won):
        if not self.two_sided:
            if self.prev_bounce < bounces or won:
                return 1
            elif done:
                return -10
            return 0
        else:
            if done:
                if won:
                    return 1
                else:
                    return -1
            else:
                return 0

    def inc_n(self, s):
        self.N[s[0],s[1],s[2],s[3],s[4],s[5]] += 1


    def chose_next(self, state):
        if self.two_sided:
            epsilon = 0.991
        else:
            epsilon = 0.991
        options = self.N[state[0],state[1],state[2],state[3],state[4]]
        ids = [0,1,2]
        if random.random() > epsilon:
           return self.index_to_action(random.choice(ids))
        else:
           return self.best_next(state)



    def best_next(self, disc_state):
        options = self.Q[disc_state[0],disc_state[1],disc_state[2],disc_state[3],disc_state[4]]
        max_id = 0
        for i in range(3):
            if options[i]> options[max_id]:
                max_id = i
        return self.index_to_action(max_id)

    def index_to_action(self, index):
        return self._actions[index]

    def action_to_index(self, action):
        return self._actions.index(action)

    def discretize(self, state):
        ball_x, ball_y, velocity_x, velocity_y, paddle_y = state;
        x_bin = y_bin = disc_v_x = disc_v_y = disc_pad = None
        x_bin = int(ball_x*self._x_bins) - 1
        x_bin = min(x_bin,11)
        y_bin = int(ball_y*self._y_bins) - 1
        y_bin = min(y_bin,11)
        if velocity_x > 0:
            disc_v_x = 1
        else:
            disc_v_x = 0
        if velocity_y >= 0.015:
            disc_v_y = 2
        elif velocity_y <= 0.015:
            disc_v_y = 1
        else:
            disc_v_y = 0
        paddle_height = .2
        disc_pad = math.floor(self._paddle_locations * paddle_y / (1 - paddle_height))
        disc_pad = min(disc_pad,11)
        return [
            x_bin,
            y_bin,
            disc_v_x,
            disc_v_x,
            disc_pad
        ]


    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    def save_model(self,model_path):
        # At the end of training save the trained model
        utils.save(model_path,self.Q)

    def load_model(self,model_path):
        # Load the trained model for evaluation
        self.Q = utils.load(model_path)
