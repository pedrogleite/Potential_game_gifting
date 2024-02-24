# path imports
import os
import sys
root = os.path.abspath(os.curdir)
sys.path.append(root)
# general imports
import json
import argparse
# specific imports
import numpy as np
import matplotlib.pyplot as plt
# local imports
from utils import game_2p
# path setup


def setup(args):
    '''
    setup output path for figure
    '''
    # directory structure for experiments
    dir_list = ['%s'%args.out_dir, 
                '%s'%args.exp_dir,]

    # create dir structure
    save_dir = ''
    for dirname in dir_list:
        save_dir += '%s/'%dirname
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
    
    # no need for config yet
    # setup_path = os.path.join(save_dir,'setup.json')
    # with open(setup_path, 'w') as f:
    #     json.dump(vars(args),f,indent=4)

    return os.path.join(root,save_dir)

def p1_p2_plot(size, r, gift, save_path):
    _, datax, datay = game_2p.play_game(size, r, gift)

    plt.scatter(100*np.array(datax)/size, 100*np.array(datay)/size, color='green')
    plt.xlabel("Player 1's Initial Potential to Hunt [%]")
    plt.ylabel("Player 2's Initial Potential to Hunt [%]")
    plt.title(f'Convergence to Prosocial Equilibrium \n as a Function of Initial Potential Towards Hunting \n with r = {r} and $\\gamma$ = {gift}:  {100*len(datax)/size**2:.1f}%')
    plt.xlim(0,100)
    plt.ylim(0,100)
    # save
    fig_path = f'{size}_{r:.1f}_{gift:.1f}.pdf'
    plt.savefig(os.path.join(save_path,fig_path))


def main(args):
    # SETUP #
    save_path = setup(args)
    print('Configuration:')
    for key in vars(args).keys():
        print('\t', key,': ', vars(args)[key])
    # run
    # plot
    p1_p2_plot(args.size, args.risk, args.gift, save_path)

    print('Finished Execution')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--out_dir",
        type=str,
        default='results',
        help="folder to save results in"
    )

    parser.add_argument(
        "--exp_dir",
        type=str,
        default='test',
        help="experiment folder"
    )

    parser.add_argument(
        "--size",
        type=int,
        default=100,
        help="maximum values allowed in potential game"
    )

    parser.add_argument(
        "--risk",
        type=float,
        default=-6,
        help="risk of payoff matrix",
    )

    parser.add_argument(
        "--gift",
        type=float,
        default=10,
        help="gifting value used",
    )

    args = parser.parse_args()
    main(args)