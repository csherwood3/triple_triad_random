"""
The card generator file. This file handles generating random card images using Python's Pillow library.
"""

from PIL import Image
import random

red_card = Image.open("Assets/Card Templates/red_card.png").convert("RGBA")
blue_card = Image.open("Assets/Card Templates/blue_card.png").convert("RGBA")

card_dict = {1: "Amarant",
             2: "Banon",
             3: "Beatrix",
             4: "Cloud",
             5: "Edgar",
             6: "Eiko",
             7: "Freya",
             8: "Garnet",
             9: "Gerald",
             10: "Kefka",
             11: "Leila",
             12: "Locke",
             13: "Magitek",
             14: "Quina",
             15: "Red_sword",
             16: "Sabin",
             17: "Seifer",
             18: "Shadow",
             19: "Steiner",
             20: "Terra",
             21: "Ultemecia",
             22: "Vivi",
             23: "Zidane",
             24: "Aerith",
             25: "Arabian_knight",
             26: "Cecil",
             27: "Clown",
             28: "Dualheads",
             29: "Exdeath",
             30: "Gogo",
             31: "Guy",
             32: "Knight_plus_girl",
             33: "Knight_plus_girl_two",
             34: "Lightning",
             35: "Maria",
             36: "Yeng_feng",
             37: "Brat",
             38: "Red_dragon",
             39: "Lenna",
             40: "Cid",
             41: "Crusader",
             42: "Sad_girl",
             43: "Xezat",
             44: "Faris",
             45: "Aerith_Portrait",
             46: "Cloud_Portrait",
             47: "Colossus",
             48: "Cute_girl",
             49: "Lulu",
             50: "Ramuh",
             51: "Rikku",
             52: "Skybenders",
             53: "Skydiver",
             54: "Squall_rinoa",
             55: "Cyan",
             56: "Whispy_knight",
             57: "Yuna",
             58: "Tidus",
             59: "Cat",
             60: "Sephiroth",
             61: "Onionex",
             62: "Sage",
             63: "Kuja",
             64: "Jecht",
             65: "Gabranth",
             66: "Crazy_bird",
             67: "Dagger",
             68: "Dr_lugae",
             69: "Forza",
             70: "Leviathon",
             71: "Unei",
             72: "Barrett",
             73: "Tifa",
             74: "Terra2",
             75: "Highwind"
             }

num_dict = {1: "number_1.png",
            2: "number_2.png",
            3: "number_3.png",
            4: "number_4.png",
            5: "number_5.png",
            6: "number_6.png",
            7: "number_7.png",
            8: "number_8.png",
            9: "number_9.png",
            10: "number_10.png"}


# noinspection PyGlobalUndefined
def make_card(top, right, left, bot, color):
    """
    Generate a random card. The random number arguments are generated in the main TripleTriadEngine file.
    """

    global card_mirror, card_template
    color = color
    top_number = top
    right_number = right
    left_number = left
    bot_number = bot

    top_number_img = Image.open("Assets/Numbers/number_" + str(top_number) + ".png").convert("RGBA")
    right_number_img = Image.open("Assets/Numbers/number_" + str(right_number) + ".png").convert("RGBA")
    left_number_img = Image.open("Assets/Numbers/number_" + str(left_number) + ".png").convert("RGBA")
    bot_number_img = Image.open("Assets/Numbers/number_" + str(bot_number) + ".png").convert("RGBA")

    card_key = card_dict[random.randint(1, 75)]
    card_portrait = Image.open(r"Assets/Portraits/" + str(card_key) + ".png")

    if color == "blue":
        card_template = blue_card
        card_mirror = red_card
    if color == "red":
        card_template = red_card
        card_mirror = blue_card

    card = Image.alpha_composite(card_template, card_portrait)
    mirror = Image.alpha_composite(card_mirror, card_portrait)

    # Top number
    card.paste(top_number_img, (26, 8), top_number_img)
    mirror.paste(top_number_img, (26, 8), top_number_img)

    # Right number
    card.paste(right_number_img, (44, 22), right_number_img)
    mirror.paste(right_number_img, (44, 22), right_number_img)

    # Left number
    card.paste(left_number_img, (8, 22), left_number_img)
    mirror.paste(left_number_img, (8, 22), left_number_img)

    # Bot number
    card.paste(bot_number_img, (26, 38), bot_number_img)
    mirror.paste(bot_number_img, (26, 38), bot_number_img)

    card_name = str(card_key) + "_" + str(top_number) + "_" + str(right_number) + "_" + str(left_number) +\
        "_" + str(bot_number)

    if color == "blue":
        card.save("Assets/Temp/blue_" + card_name + ".png")
        mirror.save("Assets/Temp/red_" + card_name + ".png")
    if color == "red":
        card.save("Assets/Temp/red_" + card_name + ".png")
        mirror.save("Assets/Temp/blue_" + card_name + ".png")

    return card_name
