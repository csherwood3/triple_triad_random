"""
The main driver file. This file handles user input and displays current game-state information.
"""

import pygame as p
from pygame.locals import *
import TripleTriadEngine as ttEng
import sys


# Constructs the window and the game's caption.
FPS = 144
BOARD_WIDTH = 1440
BOARD_HEIGHT = 900
BOARD_CENTER_WIDTH = 400
BOARD_CENTER_HEIGHT = 415
WIN = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
p.display.set_caption("Triple Triad Random")


# These dictionaries contain the board location tuples required to visualize the cursor and card locations.
grid_card_locations = {1: (451, 72),
                       2: (630, 72),
                       3: (809, 72),
                       4: (451, 323),
                       5: (630, 323),
                       6: (809, 323),
                       7: (451, 575),
                       8: (630, 575),
                       9: (809, 575)
                       }
grid_x_cursor_locations = {0: 180,
                           1: 430,
                           2: 680
                           }
grid_y_cursor_locations = {0: 530,
                           1: 720,
                           2: 890
                           }
blue_cursor_locations = {0: (136, 130),
                         1: (136, 380),
                         2: (136, 630),
                         3: (316, 130),
                         4: (316, 380)
                         }
red_cursor_locations = {0: (1236, 130),
                        1: (1236, 380),
                        2: (1236, 630),
                        3: (1051, 130),
                        4: (1051, 380)
                        }


# Initialize all the non-card images necessary to visualize the game state.
active_img = p.image.load("Assets/active.png")
null_card = p.image.load("Assets/Card Templates/null_card.png")
grid_cursor_image = p.image.load("Assets/grid_cursor.png")
blue_cursor_img = p.image.load("Assets/blue_cursor.png")
blue_won_img = p.image.load("Assets/blue_wins.png")
red_won_img = p.image.load("Assets/red_wins.png")
red_cursor_img = p.image.load("Assets/red_cursor.png")
board = p.image.load("Assets/board_new.png")
draw_game = p.image.load("Assets/draw_game.png")


# Initialize all the game engine classes.
GameState = ttEng.GameState()
GameState.make_all_cards()
BlueCursor = ttEng.BlueCursor(GameState)
RedCursor = ttEng.RedCursor(GameState)
BoardCursor = ttEng.BoardCursor()


# Loads all the sounds.
p.mixer.init()
menu_move_sound = p.mixer.Sound("Assets/Cursor - Move.wav")
menu_move_sound.set_volume(.20)
invalid_move_sound = p.mixer.Sound("Assets/Cursor - Buzzer.wav")
invalid_move_sound.set_volume(.17)
place_card_sound = p.mixer.Sound("Assets/Cursor - Equip.wav")
place_card_sound.set_volume(.17)
menu_cancel_sound = p.mixer.Sound("Assets/Cursor - Cancel.wav")
menu_cancel_sound.set_volume(.17)


def draw_window():
    WIN.blit(board, (0, 0))


def draw_player_turn():
    player_turn = GameState.get_player_turn()
    if player_turn == "blue":
        WIN.blit(active_img, (50, 781))
    elif player_turn == "red":
        WIN.blit(active_img, (1211, 781))


def draw_blue_cards():
    x_coord = 5
    y_coord = 5
    for blue_cards in ttEng.GameState.get_player_cards(GameState, "blue"):
        card_image = p.image.load("Assets/Temp/" + ttEng.Card.get_image(blue_cards))
        WIN.blit(card_image, (x_coord, y_coord))
        y_coord += 252
        if y_coord > 600:
            x_coord += 180
            y_coord = 5


def draw_red_cards():
    x_coord = 1255
    y_coord = 5
    for red_cards in ttEng.GameState.get_player_cards(GameState, "red"):
        card_image = p.image.load("Assets/Temp/" + ttEng.Card.get_image(red_cards))
        WIN.blit(card_image, (x_coord, y_coord))
        y_coord += 252
        if y_coord > 600:
            x_coord -= 180
            y_coord = 5


def draw_blue_cursor():
    if len(GameState.get_player_cards("blue")) != 0:
        WIN.blit(blue_cursor_img, blue_cursor_locations[BlueCursor.get_points_to_value()])


def draw_red_cursor():
    if len(GameState.get_player_cards("red")) != 0:
        WIN.blit(red_cursor_img, red_cursor_locations[RedCursor.get_points_to_value()])


def draw_grid():
    counter = 1
    for rows in ttEng.GameState.get_board(GameState):
        for squares in rows:
            if squares == "-":
                WIN.blit(p.image.load("Assets/Card Templates/null_card.png"),
                         (grid_card_locations[counter][0], grid_card_locations[counter][1]))
                counter += 1
            if squares != "-":
                card_image = p.image.load("Assets/Temp/" + ttEng.Card.get_image(squares))
                WIN.blit(card_image, (grid_card_locations[counter][0], grid_card_locations[counter][1]))
                counter += 1


def draw_grid_cursor():
    WIN.blit(grid_cursor_image, (grid_y_cursor_locations[BoardCursor.get_y_loc()],
                                 grid_x_cursor_locations[BoardCursor.get_x_loc()]))


def draw_score():
    blue_score = GameState.get_blue_score()
    blue_score_img = p.image.load("Assets/Numbers/number_" + str(blue_score) + ".png")
    blue_score_img = p.transform.scale(blue_score_img, (31, 46))

    red_score = GameState.get_red_score()
    red_score_img = p.image.load("Assets/Numbers/number_" + str(red_score) + ".png")
    red_score_img = p.transform.scale(red_score_img, (31, 46))

    WIN.blit(blue_score_img, (175, 795))
    WIN.blit(red_score_img, (1335, 795))


def draw_everything():
    draw_window()
    draw_grid()
    draw_blue_cards()
    draw_red_cards()
    draw_blue_cursor()
    draw_red_cursor()
    draw_player_turn()
    draw_score()
    p.display.update()


def play_menu_sound():
    p.mixer.Sound.play(menu_move_sound)


def grid_control(card):
    card = card
    clock = p.time.Clock()
    running = True
    active_player = GameState.get_player_turn()

    while running:
        clock.tick(FPS)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.KEYDOWN:
                if active_player == "blue":

                    # Blue cursor keys
                    if event.key == K_w:
                        play_menu_sound()
                        BoardCursor.move_y_up()

                    if event.key == K_s:
                        play_menu_sound()
                        BoardCursor.move_y_down()

                    if event.key == K_a:
                        play_menu_sound()
                        BoardCursor.move_x_left()

                    if event.key == K_d:
                        play_menu_sound()
                        BoardCursor.move_x_right()

                    if event.key == K_q:
                        if GameState.check_legal_move(BoardCursor.get_x_loc(), BoardCursor.get_y_loc()):
                            GameState.make_move(card, BoardCursor.get_x_loc(), BoardCursor.get_y_loc())
                            BlueCursor.reset_points_to()
                            p.mixer.Sound.play(place_card_sound)
                            running = False
                        else:
                            p.mixer.Sound.play(invalid_move_sound)
                            continue

                    if event.key == K_e:
                        p.mixer.Sound.play(menu_cancel_sound)
                        running = False

                if active_player == "red":

                    # Red cursor keys
                    if event.key == K_UP:
                        play_menu_sound()
                        BoardCursor.move_y_up()

                    if event.key == K_DOWN:
                        play_menu_sound()
                        BoardCursor.move_y_down()

                    if event.key == K_LEFT:
                        play_menu_sound()
                        BoardCursor.move_x_left()

                    if event.key == K_RIGHT:
                        play_menu_sound()
                        BoardCursor.move_x_right()

                    if event.key == K_RIGHTBRACKET:
                        if GameState.check_legal_move(BoardCursor.get_x_loc(), BoardCursor.get_y_loc()):
                            GameState.make_move(card, BoardCursor.get_x_loc(), BoardCursor.get_y_loc())
                            RedCursor.reset_points_to()
                            p.mixer.Sound.play(place_card_sound)
                            running = False
                        else:
                            p.mixer.Sound.play(invalid_move_sound)
                            continue

                    if event.key == K_BACKSLASH:
                        p.mixer.Sound.play(menu_cancel_sound)
                        running = False

        draw_window()
        draw_grid()
        draw_grid_cursor()

        draw_blue_cards()
        draw_red_cards()

        draw_blue_cursor()
        draw_red_cursor()

        draw_player_turn()
        draw_score()

        p.display.update()


def main():
    clock = p.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        blue_player_length = GameState.get_player_cards("blue")
        red_player_length = GameState.get_player_cards("red")
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:

                # Blue cursor keys
                if event.key == K_s:
                    if len(blue_player_length) > 1:
                        play_menu_sound()
                    BlueCursor.inc_cursor()
                if event.key == K_w:
                    if len(blue_player_length) > 1:
                        play_menu_sound()
                    BlueCursor.dec_cursor()
                if event.key == K_a:
                    if len(blue_player_length) > 1:
                        play_menu_sound()
                    BlueCursor.move_cursor_left()
                if event.key == K_d:
                    if len(blue_player_length) > 1:
                        play_menu_sound()
                    BlueCursor.move_cursor_right()

                if event.key == K_q and GameState.get_player_turn() == "blue":
                    grid_control(BlueCursor.get_points_to())

                # Red cursor keys
                if event.key == K_DOWN:
                    if len(red_player_length) > 1:
                        play_menu_sound()
                    RedCursor.inc_cursor()
                if event.key == K_UP:
                    if len(red_player_length) > 1:
                        play_menu_sound()
                    RedCursor.dec_cursor()
                if event.key == K_RIGHT:
                    if len(red_player_length) > 1:
                        play_menu_sound()
                    RedCursor.move_cursor_right()
                if event.key == K_LEFT:
                    if len(red_player_length) > 1:
                        play_menu_sound()
                    RedCursor.move_cursor_left()

                if event.key == K_RIGHTBRACKET and GameState.get_player_turn() == "red":
                    grid_control(RedCursor.get_points_to())

                if event.key == K_SPACE:
                    GameState.switch_turn()

        draw_window()
        draw_grid()

        draw_blue_cards()
        draw_red_cards()

        draw_blue_cursor()
        draw_red_cursor()

        draw_player_turn()
        draw_score()

        if GameState.get_turn_counter() == 9:
            if GameState.get_current_gamestate() == "blue_won":
                WIN.blit(blue_won_img, (BOARD_CENTER_WIDTH, BOARD_CENTER_HEIGHT))
            if GameState.get_current_gamestate() == "red_won":
                WIN.blit(red_won_img, (BOARD_CENTER_WIDTH, BOARD_CENTER_HEIGHT))
            if GameState.get_current_gamestate() == "draw":
                WIN.blit(draw_game, (BOARD_CENTER_WIDTH, BOARD_CENTER_HEIGHT))

        p.display.update()

    p.quit()


if __name__ == "__main__":
    main()
