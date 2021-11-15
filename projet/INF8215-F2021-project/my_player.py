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
        depth = 2
        swap = {0: 1, 1: 0}

        # set of legal wall moves
        wall_actions = board.get_legal_wall_moves(player)

        # set of legal pawn moves
        pawn_actions = board.get_legal_pawn_moves(player)
        # board.min_steps_before_victory(player)
        # board_c = board.clone()
        shortest_path = board.get_shortest_path(player)

        def simpleHeuristic(board, p):
            # maximise la différence entre le nb de pas restant avant la victoire pour l'adversaire et
            # les pas restant avant la victoire pour le joueur.
            #  maximise (min_steps_before_victory(player^) - min_steps_before_victory(player) )
            pSteps = board.min_steps_before_victory(p)
            aSteps = board.min_steps_before_victory(swap[p])
            value = aSteps - pSteps
            # value = - board.min_steps_before_victory(player)
            # value = -board.min_steps_before_victory(player)

            # print("simple_heuristic", value)
            return value, pSteps, aSteps

        # Stratégie B : permet d'identifier les meilleurs mouvements potentiels
        # on va évaluer plus bas seulement pour les meilleurs mouvements.
        def getBestMoves(board, p):
            bestMove = []
            currentScore, pSteps, aSteps = simpleHeuristic(board, p)
            print("current score", currentScore)
            # ajouter le cas si on est pour perdre
            positionOp = board.pawns[swap[player]]

            # TODO: si on est en désavantage, on étudie la possibilité de mettre un mur

            # s'il reste moins de 2 pas pour que l'adversaire gagne et nous plus de 2 et qu'il nous reste des murs
            if aSteps <= 2 and pSteps > 2 and board.nb_walls[p] > 0:
                print('<2 steps !!!')
                for m in board.get_legal_wall_moves(p):
                    boardc = board.clone()
                    boardc.play_action(m, p)
                    newScore, _, _ = simpleHeuristic(boardc, p)
                    if newScore > currentScore:
                        bestMove.append((m, boardc))
            elif currentScore < 0:
                print("current score < 0")
                for m in board.get_actions(p):
                    # on étudie la possibilité de mettre un mur autour de l'opposant seulement
                    if abs(m[1] - positionOp[0]) < 4 or abs(m[2] - positionOp[1]) < 4:
                        boardc = board.clone()
                        boardc.play_action(m, p)
                        newScore, _, _ = simpleHeuristic(boardc, p)
                        if newScore > currentScore:
                            bestMove.append((m, boardc))
                        print(m, 'cScore', currentScore, 'nScore', newScore, 'step_p',
                              boardc.min_steps_before_victory(p),
                              'step_a', boardc.min_steps_before_victory(swap[p]))
            # si on est en avantage ou exaco, on déplace notre pion
            else:
                print("current score >= 0")

                for m in board.get_legal_pawn_moves(p):
                    boardc = board.clone()
                    boardc.play_action(m, p)
                    newScore, _, _ = simpleHeuristic(boardc, p)
                    if newScore >= currentScore:
                        bestMove.append((m, boardc))
                    print(m, 'cScore', currentScore, 'nScore', newScore, 'step_p', boardc.min_steps_before_victory(p),
                          'step_a', boardc.min_steps_before_victory(swap[p]))
            # TODO: verification si bestMove est vide

            return bestMove

        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        def alphabeta(boardAB, depthAB, alpha, beta, maximizingPlayer):
            if depthAB == 0 or boardAB.is_finished():
                print("end")
                value, _, _ = simpleHeuristic(boardAB, player)
                return value, None
            move = None
            if maximizingPlayer:
                print("max")
                maxvalue = -math.inf

                # on commence par déterminer les meilleurs mouvements potentiel (stratégie B)
                bestMove = getBestMoves(boardAB, player)
                # On étant les noeuds des meilleurs candidats
                for (pmove, boardCloned) in bestMove:
                    skip = False
                    if not skip:
                        if True:
                            v, m = alphabeta(boardCloned, depthAB - 1, alpha, beta, False)
                            if v > maxvalue:
                                maxvalue = v
                                move = pmove
                                if maxvalue >= beta:
                                    # print("break, β cutoff")
                                    break
                                alpha = max(alpha, maxvalue)

                return maxvalue, move
            else:
                print("min")
                minvalue = math.inf
                # pour chaque noeud = pour chaque action possible
                bestMove = getBestMoves(boardAB, swap[player])
                for (pmove, boardCloned) in bestMove:
                    skip = False
                    if not skip:
                        if True:
                            v, m = alphabeta(boardCloned, depthAB - 1, alpha, beta, True)
                            if (v < minvalue):
                                minvalue = v
                                move = pmove
                                if minvalue <= alpha:
                                    # print("break, a cutoff")
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
