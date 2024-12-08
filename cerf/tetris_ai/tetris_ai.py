import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pygame
from tetris_game import Tetris, GRID_WIDTH, GRID_HEIGHT  

STATE_SIZE = GRID_WIDTH * GRID_HEIGHT 
ACTION_SIZE = 4 
HIDDEN_SIZE = 128  
LEARNING_RATE = 0.001
GAMMA = 0.99  
EPSILON_START = 1.0 
EPSILON_END = 0.1 
EPSILON_DECAY = 10000 
class DQN(nn.Module):
    def __init__(self, state_size, action_size, hidden_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
def get_state(tetris):
    grid = np.array(tetris.grid).flatten()
    return torch.tensor(grid, dtype=torch.float32)

def calculate_reward(tetris, lines_cleared):
    return lines_cleared * 10

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
policy_net = DQN(STATE_SIZE, ACTION_SIZE, HIDDEN_SIZE).to(device)
optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
criterion = nn.MSELoss()

replay_buffer = []
BATCH_SIZE = 32
MAX_MEMORY = 50000

def train_agent():
    global EPSILON_START

    total_episodes = 100  
    screen = pygame.display.set_mode((300, 600))  

    for episode in range(total_episodes):
        tetris = Tetris()
        total_reward = 0
        steps = 0

        while not tetris.game_over:
            state = get_state(tetris).to(device)
            if random.random() < EPSILON_START:
                action = random.randint(0, ACTION_SIZE - 1)
            else:
                with torch.no_grad():
                    q_values = policy_net(state)
                    action = torch.argmax(q_values).item()

            prev_lines_cleared = len([row for row in tetris.grid if not any(cell == 0 for cell in row)])
            tetris.step(action)
            lines_cleared = len([row for row in tetris.grid if not any(cell == 0 for cell in row)])
            reward = calculate_reward(tetris, lines_cleared - prev_lines_cleared)
            next_state = get_state(tetris).to(device)
            done = tetris.game_over

            tetris.render(screen)
            pygame.display.flip()
            pygame.time.wait(100)  

            replay_buffer.append((state, action, reward, next_state, done))
            if len(replay_buffer) > MAX_MEMORY:
                replay_buffer.pop(0)

            if len(replay_buffer) >= BATCH_SIZE:
                batch = random.sample(replay_buffer, BATCH_SIZE)
                states, actions, rewards, next_states, dones = zip(*batch)

                states = torch.stack(states).to(device)
                actions = torch.tensor(actions).to(device)
                rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
                next_states = torch.stack(next_states).to(device)
                dones = torch.tensor(dones, dtype=torch.float32).to(device)

                q_values = policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
                next_q_values = policy_net(next_states).max(1)[0]
                target_q_values = rewards + GAMMA * next_q_values * (1 - dones)

                loss = criterion(q_values, target_q_values.detach())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_reward += reward
            steps += 1

            if done:
                break

        EPSILON_START = max(EPSILON_END, EPSILON_START - (EPSILON_START - EPSILON_END) / EPSILON_DECAY)

        print(f"Эпизод {episode + 1}/{total_episodes} | Награда: {total_reward} | Шаги: {steps}")

if __name__ == "__main__":
    train_agent()
