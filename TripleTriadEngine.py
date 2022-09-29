import random
import TripleTriadCardGenerator as cardGenerate
import os


class GameState:
    def __init__(self):
        self._board = [["-", "-", "-"],
                       ["-", "-", "-"],
                       ["-", "-", "-"]]
        self._blue_player_cards = []
        self._red_player_cards = []
        self._current_state = "UNFINISHED"
        self._turn_counter = 0
        starting_player = random.randint(1, 2)
        if starting_player == 1:
            self._player_turn = "blue"
        elif starting_player == 2:
            self._player_turn = "red"
        self._blue_score = 5
        self._red_score = 5

    def make_card(self, color):
        card = Card(color)
        card_top = card.get_card_top()
        card_right = card.get_card_right()
        card_left = card.get_card_left()
        card_bot = card.get_card_bot()
        card_color = card.get_card_color()

        if card_color == "red":
            card_name = cardGenerate.make_card(card_top, card_right, card_left, card_bot, "red")
            card.set_name("red_" + card_name)
            card.set_mirror("blue_" + card_name)
            self._red_player_cards.append(card)

        elif card_color == "blue":
            card_name = cardGenerate.make_card(card_top, card_right, card_left, card_bot, "blue")
            card.set_name("blue_" + card_name)
            card.set_mirror("red_" + card_name)
            self._blue_player_cards.append(card)

    def make_all_cards(self):
        self.delete_all_cards()
        for num in range(0, 5):
            self.make_card("blue")
            self.make_card("red")

    def delete_all_cards(self):
        self._blue_player_cards = []
        self._red_player_cards = []

        for items in os.listdir("Assets/Temp"):
            os.remove("Assets/Temp/" + items)

    def get_player_cards(self, color):
        if color == "red":
            return self._red_player_cards
        if color == "blue":
            return self._blue_player_cards

    def get_board(self):
        return self._board

    def print_board(self):
        for rows in self._board:
            print(rows)

    def get_player_turn(self):
        return self._player_turn

    def get_turn_counter(self):
        return self._turn_counter

    def switch_turn(self):
        if self._player_turn == "red":
            self._player_turn = "blue"
            return
        if self._player_turn == "blue":
            self._player_turn = "red"
            return

    def test(self):
        return

    def update_score(self):
        self._blue_score = len(self._blue_player_cards)
        self._red_score = len(self._red_player_cards)

        for rows in self._board:
            for squares in rows:
                if squares == "-":
                    continue
                if squares != "-":
                    card_color = Card.get_card_color(squares)
                    if card_color == "blue":
                        self._blue_score += 1
                    if card_color == "red":
                        self._red_score += 1

    def get_blue_score(self):
        return self._blue_score

    def get_red_score(self):
        return self._red_score

    def remove_card(self, card):
        if self._player_turn == "blue":
            self._blue_player_cards.remove(card)
        if self._player_turn == "red":
            self._red_player_cards.remove(card)

    def make_move(self, card, square_x, square_y):
        if self._board[square_x][square_y] == "-":
            self._board[square_x][square_y] = card
            self.remove_card(card)
            self.flip_sequence(card, square_x, square_y)
            self.update_score()
            self.switch_turn()
            self._turn_counter += 1
            if self._turn_counter == 9:
                self.check_win()
            return
        else:
            print("Invalid Move")
            return False

    def check_win(self):
        if self._blue_score > self._red_score:
            self._current_state = "blue_won"
            print("blue won")
        if self._red_score > self._blue_score:
            self._current_state = "red_won"
            print("red won")
        if self._red_score == self._blue_score:
            self._current_state = "draw"
            print("draw game")

    def check_legal_move(self, square_x, square_y):
        if self._board[square_x][square_y] == "-":
            return True
        else:
            return False

    def get_current_gamestate(self):
        return self._current_state

    def flip_sequence(self, card, square_x, square_y):
        board = self._board
        placed_card_top = Card.get_card_values(card)[0]
        placed_card_right = Card.get_card_values(card)[1]
        placed_card_left = Card.get_card_values(card)[2]
        placed_card_bot = Card.get_card_values(card)[3]
        placed_card_color = Card.get_card_color(card)

        # Square 0,0 logic
        if square_x == 0 and square_y == 0:
            if board[1][0] != "-" and placed_card_color != Card.get_card_color(board[1][0]):
                if placed_card_bot > Card.get_card_top(board[1][0]):
                    Card.flip_card(self._board[1][0])
            if board[0][1] != "-" and placed_card_color != Card.get_card_color(board[0][1]):
                if placed_card_right > Card.get_card_left(board[0][1]):
                    Card.flip_card(self._board[0][1])

        # Square 0,1 logic
        if square_x == 0 and square_y == 1:
            if board[0][0] != "-" and placed_card_color != Card.get_card_color(board[0][0]):
                if placed_card_left > Card.get_card_right(board[0][0]):
                    Card.flip_card(self._board[0][0])
            if board[1][1] != "-" and placed_card_color != Card.get_card_color(board[1][1]):
                if placed_card_bot > Card.get_card_top(board[1][1]):
                    Card.flip_card(self._board[1][1])
            if board[0][2] != "-" and placed_card_color != Card.get_card_color(board[0][2]):
                if placed_card_right > Card.get_card_left(board[0][2]):
                    Card.flip_card(self._board[0][2])

        # Square 0,2 logic
        if square_x == 0 and square_y == 2:
            if board[0][1] != "-" and placed_card_color != Card.get_card_color(board[0][1]):
                if placed_card_left > Card.get_card_right(board[0][1]):
                    Card.flip_card(self._board[0][1])
            if board[1][2] != "-" and placed_card_color != Card.get_card_color(board[1][2]):
                if placed_card_bot > Card.get_card_top(board[1][2]):
                    Card.flip_card(self._board[1][2])

        # Square 1,0 logic
        if square_x == 1 and square_y == 0:
            if board[0][0] != "-" and placed_card_color != Card.get_card_color(board[0][0]):
                if placed_card_top > Card.get_card_bot(board[0][0]):
                    Card.flip_card(self._board[0][0])
            if board[1][1] != "-" and placed_card_color != Card.get_card_color(board[1][1]):
                if placed_card_right > Card.get_card_left(board[1][1]):
                    Card.flip_card(self._board[1][1])
            if board[2][0] != "-" and placed_card_color != Card.get_card_color(board[2][0]):
                if placed_card_bot > Card.get_card_top(board[2][0]):
                    Card.flip_card(self._board[2][0])

        # Square 1,1 logic
        if square_x == 1 and square_y == 1:
            if board[0][1] != "-" and placed_card_color != Card.get_card_color(board[0][1]):
                if placed_card_top > Card.get_card_bot(board[0][1]):
                    Card.flip_card(self._board[0][1])
            if board[1][0] != "-" and placed_card_color != Card.get_card_color(board[1][0]):
                if placed_card_left > Card.get_card_right(board[1][0]):
                    Card.flip_card(self._board[1][0])
            if board[2][1] != "-" and placed_card_color != Card.get_card_color(board[2][1]):
                if placed_card_bot > Card.get_card_top(board[2][1]):
                    Card.flip_card(self._board[2][1])
            if board[1][2] != "-" and placed_card_color != Card.get_card_color(board[1][2]):
                if placed_card_right > Card.get_card_left(board[1][2]):
                    Card.flip_card(self._board[1][2])

        # Square 1,2 logic
        if square_x == 1 and square_y == 2:
            if board[0][2] != "-" and placed_card_color != Card.get_card_color(board[0][2]):
                if placed_card_top > Card.get_card_bot(board[0][2]):
                    Card.flip_card(self._board[0][2])
            if board[1][1] != "-" and placed_card_color != Card.get_card_color(board[1][1]):
                if placed_card_left > Card.get_card_right(board[1][1]):
                    Card.flip_card(self._board[1][1])
            if board[2][2] != "-" and placed_card_color != Card.get_card_color(board[2][2]):
                if placed_card_bot > Card.get_card_top(board[2][2]):
                    Card.flip_card(self._board[2][2])

        # Square 2,0 logic
        if square_x == 2 and square_y == 0:
            if board[1][0] != "-" and placed_card_color != Card.get_card_color(board[1][0]):
                if placed_card_top > Card.get_card_bot(board[1][0]):
                    Card.flip_card(self._board[1][0])
            if board[2][1] != "-" and placed_card_color != Card.get_card_color(board[2][1]):
                if placed_card_right > Card.get_card_left(board[2][1]):
                    Card.flip_card(self._board[2][1])

        # Square 2,1 logic
        if square_x == 2 and square_y == 1:
            if board[2][0] != "-" and placed_card_color != Card.get_card_color(board[2][0]):
                if placed_card_left > Card.get_card_right(board[2][0]):
                    Card.flip_card(self._board[2][0])
            if board[1][1] != "-" and placed_card_color != Card.get_card_color(board[1][1]):
                if placed_card_top > Card.get_card_bot(board[1][1]):
                    Card.flip_card(self._board[1][1])
            if board[2][2] != "-" and placed_card_color != Card.get_card_color(board[2][2]):
                if placed_card_right > Card.get_card_left(board[2][2]):
                    Card.flip_card(self._board[2][2])

        # Square 2,2 logic
        if square_x == 2 and square_y == 2:
            if board[1][2] != "-" and placed_card_color != Card.get_card_color(board[1][2]):
                if placed_card_top > Card.get_card_bot(board[1][2]):
                    Card.flip_card(self._board[1][2])
            if board[2][1] != "-" and placed_card_color != Card.get_card_color(board[2][1]):
                if placed_card_left > Card.get_card_right(board[2][1]):
                    Card.flip_card(self._board[2][1])


class Card:
    def __init__(self, color):
        self._top_value = random.randint(1, 10)
        self._bot_value = random.randint(1, 10)
        self._left_value = random.randint(1, 10)
        self._right_value = random.randint(1, 10)
        self._color = color
        self._name = None
        self._mirror = None

    def get_card_values(self):
        return self._top_value, self._right_value, self._left_value, self._bot_value

    def get_card_top(self):
        return self._top_value

    def get_card_bot(self):
        return self._bot_value

    def get_card_left(self):
        return self._left_value

    def get_card_right(self):
        return self._right_value

    def get_card_color(self):
        return self._color

    def get_name(self):
        return self._name

    def get_mirror(self):
        return self._mirror

    def get_image(self):
        return str(self._name + ".png")

    def set_color(self, color):
        self._color = color

    def set_name(self, name):
        self._name = name

    def set_mirror(self, mirror):
        self._mirror = mirror

    def flip_card(self):
        if self._color == "blue":
            self._color = "red"
            front_side = self.get_mirror()
            flip_side = self._name
            self.set_name(front_side)
            self.set_mirror(flip_side)

        elif self._color == "red":
            self._color = "blue"
            front_side = self.get_mirror()
            flip_side = self._name
            self.set_name(front_side)
            self.set_mirror(flip_side)


class BlueCursor:
    def __init__(self, game):
        self._game = game
        self._pointer_value = 0
        self._cards = GameState.get_player_cards(game, "blue")
        self._points_to = self._cards[self._pointer_value]

    def reset_points_to(self):
        if len(self._cards) == 0:
            self._points_to = None
        else:
            self._pointer_value = 0
            self._points_to = self._cards[self._pointer_value]

    def get_points_to(self):
        return self._points_to

    def get_points_to_value(self):
        return self._pointer_value

    def inc_cursor(self):
        if self.check_zero_cards() is False:
            list_length = len(GameState.get_player_cards(self._game, "blue"))

            self._pointer_value += 1
            if self._pointer_value >= list_length:
                self._pointer_value = 0
            self._points_to = self._cards[self._pointer_value]

    def dec_cursor(self):
        if self.check_zero_cards() is False:
            list_length = len(GameState.get_player_cards(self._game, "blue"))

            self._pointer_value -= 1
            if self._pointer_value < 0:
                self._pointer_value = list_length - 1
            self._points_to = self._cards[self._pointer_value]

    def move_cursor_left(self):
        if self.check_zero_cards() is False:

            if self._pointer_value == 3:
                self._pointer_value = 0
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 4:
                self._pointer_value = 1
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 0 and len(self._cards) >= 4:
                self._pointer_value = 3
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 1 and len(self._cards) == 5:
                self._pointer_value = 4
                self._points_to = self._cards[self._pointer_value]
                return

            else:
                return False

    def move_cursor_right(self):
        if self.check_zero_cards() is False:

            if self._pointer_value == 0 and len(self._cards) >= 4:
                self._pointer_value = 3
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 1 and len(self._cards) == 5:
                self._pointer_value = 4
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 3:
                self._pointer_value = 0
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 4:
                self._pointer_value = 1
                self._points_to = self._cards[self._pointer_value]
                return
            else:
                return False

    def check_zero_cards(self):
        if len(self._cards) == 0:
            return True
        else:
            return False


class RedCursor:
    def __init__(self, game):
        self._game = game
        self._pointer_value = 0
        self._cards = GameState.get_player_cards(game, "red")
        self._points_to = self._cards[self._pointer_value]

    def reset_points_to(self):
        if len(self._cards) == 0:
            self._points_to = None
        else:
            self._pointer_value = 0
            self._points_to = self._cards[self._pointer_value]

    def get_points_to(self):
        return self._points_to

    def get_points_to_value(self):
        return self._pointer_value

    def inc_cursor(self):
        if self.check_zero_cards() is False:
            list_length = len(GameState.get_player_cards(self._game, "red"))

            self._pointer_value += 1
            if self._pointer_value >= list_length:
                self._pointer_value = 0
            self._points_to = self._cards[self._pointer_value]

    def dec_cursor(self):
        if self.check_zero_cards() is False:
            list_length = len(GameState.get_player_cards(self._game, "red"))

            self._pointer_value -= 1
            if self._pointer_value < 0:
                self._pointer_value = list_length - 1
            self._points_to = self._cards[self._pointer_value]

    def move_cursor_right(self):
        if self.check_zero_cards() is False:

            if self._pointer_value == 0 and len(self._cards) >= 4:
                self._pointer_value = 3
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 1 and len(self._cards) == 5:
                self._pointer_value = 4
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 3:
                self._pointer_value = 0
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 4:
                self._pointer_value = 1
                self._points_to = self._cards[self._pointer_value]
                return
            else:
                return False

    def move_cursor_left(self):
        if self.check_zero_cards() is False:

            if self._pointer_value == 3:
                self._pointer_value = 0
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 4:
                self._pointer_value = 1
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 0 and len(self._cards) >= 4:
                self._pointer_value = 3
                self._points_to = self._cards[self._pointer_value]
                return
            if self._pointer_value == 1 and len(self._cards) == 5:
                self._pointer_value = 4
                self._points_to = self._cards[self._pointer_value]
                return

            else:
                return False

    def check_zero_cards(self):
        if len(self._cards) == 0:
            return True
        else:
            return False


class BoardCursor:
    def __init__(self):
        self._board_x = 1
        self._board_y = 1

    def reset_cursors(self):
        self._board_x = 1
        self._board_y = 1

    def move_x_right(self):
        self._board_y += 1
        if self._board_y > 2:
            self._board_y = 0

    def move_x_left(self):
        self._board_y -= 1
        if self._board_y < 0:
            self._board_y = 2

    def move_y_down(self):
        self._board_x += 1
        if self._board_x > 2:
            self._board_x = 0

    def move_y_up(self):
        self._board_x -= 1
        if self._board_x < 0:
            self._board_x = 2

    def get_x_loc(self):
        return self._board_x

    def get_y_loc(self):
        return self._board_y


def main():
    game = GameState()
    game.make_all_cards()
    blue_cursor = BlueCursor(game)
    red_cursor = RedCursor(game)
    board_cursor = BoardCursor()
    print(game.get_player_cards("blue"))
    game.print_board()
    print(game.get_player_cards("red"))


if __name__ == "__main__":
    main()
