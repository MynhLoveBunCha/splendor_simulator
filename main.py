import gym
import gym_splendor
import os
import pandas as pd

def check_winner(state):
    name = ''
    score_max = 14
    player_win = None
    if (state['Turn']+1)%4 == 0:
        for player in list(state['Player']):
            if player.score > score_max:
                score_max = player.score 
        if score_max > 14:
            for player in list(state['Player']):
                if player.score >= score_max:
                    score_max = player.score 
                    player_win = player
                elif player.score == score_max:
                    if len(player.card_open) < len(player_win.card_open):
                        player_win = player
    if player_win != None:
        # pd.read_csv(f'State_tam_{player_win.name}.csv').assign(win = 1).to_csv(f'State_tam_{player_win.name}.csv', index = False)
        return player_win.name, score_max, state['Turn']+1
    else:
        return "None"

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    env.render()
    while env.turn <200:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if env.turn % 50 == 1:
            # input()
            pass
        if done == True:
            break
    state = env.state
    print(check_winner(state))

if __name__ == '__main__':
    for _ in range(100):
        main()

