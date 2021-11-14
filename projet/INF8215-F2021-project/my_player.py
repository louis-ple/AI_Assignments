#!/usr/bin/env python3
"""
Quoridor agent.
Copyright (C) 2013, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

from quoridor import *
import math


class MyAgent(Agent):
    """My Quoridor agent."""

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in quoridor.py.
        :param player: the player to control in this step (0 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
          eg: ('P', 5, 2) to move your pawn to cell (5,2)
          eg: ('WH', 5, 2) to put a horizontal wall on corridor (5,2)
          for more details, see `Board.get_actions()` in quoridor.py
        """
        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        # TODO: implement your agent and return an action for the current step.

        board = dict_to_board(percepts)
        depth = 1
        swap = {0: 1, 1: 0}

        # set of legal wall moves
        wall_actions = board.get_legal_wall_moves(player)

        # set of legal pawn moves
        pawn_actions = board.get_legal_pawn_moves(player)
        # board.min_steps_before_victory(player)
        # board_c = board.clone()
        shortest_path = board.get_shortest_path(player)

        def simpleHeuristic(board, player):
            #  maximise (min_steps_before_victory(player^) - min_steps_before_victory(player) )
            value = board.min_steps_before_victory(swap[player]) - board.min_steps_before_victory(player)
            # value = -board.min_steps_before_victory(player)

            print("simple_heuristic", value)
            return value

        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        def alphabeta(boardAB, depthAB, alpha, beta, maximizingPlayer):
            if depthAB == 0 or boardAB.is_finished():
                print("end")
                return simpleHeuristic(boardAB, player), None
            move = None
            if maximizingPlayer:
                print("max")
                maxvalue = -math.inf

                # pour chaque noeud = pour chaque action possible
                print(boardAB.get_actions(player))
                for pmove in boardAB.get_actions(player):

                    # ici on aimerait filtrer les positions de mur considérer
                    # pour ne garder que les positions autour de l'oposant
                    skip = False
                    if pmove[0] == 'WH' or pmove[0] == 'WV':
                        print("f")
                        position_op = boardAB.pawns[swap[player]]
                        if abs(pmove[1] - position_op[0]) > 3 or abs(pmove[2] - position_op[1]) > 3:
                            skip = True
                    # fin  filtre
                    if not skip:
                        print(depthAB, pmove)
                        boardCloned = boardAB.clone()
                        boardCloned.play_action(pmove, player)
                        v, m = alphabeta(boardCloned, depthAB - 1, alpha, beta, False)
                        if v > maxvalue:
                            maxvalue = v
                            move = pmove
                            if maxvalue >= beta:
                                print("break, β cutoff")
                                break
                            alpha = max(alpha, maxvalue)

                return maxvalue, move
            else:
                print("min")
                minvalue = math.inf
                # pour chaque noeud = pour chaque action possible
                for pmove in boardAB.get_actions(swap[player]):
                    print(depthAB, pmove)
                    boardCloned = boardAB.clone()
                    boardCloned.play_action(pmove, swap[player])
                    v, m = alphabeta(boardCloned, depthAB - 1, alpha, beta, True)
                    if (v < minvalue):
                        minvalue = v
                        move = pmove
                        if minvalue <= alpha:
                            print("break, a cutoff")
                            break
                        beta = min(beta, minvalue)
                return minvalue, move

        alpha = -math.inf
        beta = math.inf

        value, move = alphabeta(board, depth, alpha, beta, True)
        print("value", value, "move", move)
        return move


if __name__ == "__main__":
    agent_main(MyAgent())
