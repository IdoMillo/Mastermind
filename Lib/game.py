import random

from game_classes import *

# --------------------------- Pygame initializers
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.font.init()
digit_font_render = pygame.font.Font(DIGITAL_FONT_FILE, DIG_FONT_SIZE)
text_font_render = pygame.font.Font(DIGITAL_FONT_FILE, TEXT_FONT_SIZE)
ins_text_font_render = pygame.font.Font(DIGITAL_FONT_FILE, INSTRUCTIONS_FONT_SIZE)
header_font_render = pygame.font.Font(DIGITAL_FONT_FILE, HEADER_FONT_SIZE)
logo_image = pygame.image.load(M_LOGO_FILE)
pygame.display.set_caption("Mastermind")
pygame.display.set_icon(logo_image)
clock = pygame.time.Clock()

# sound effects
sound_effects = [
    pygame.mixer.Sound(SOUNDS_FILE["button hover"]),
    pygame.mixer.Sound(SOUNDS_FILE["key press"]),
    pygame.mixer.Sound(SOUNDS_FILE["send guess"]),
    pygame.mixer.Sound(SOUNDS_FILE["winning"]),
    pygame.mixer.Sound(SOUNDS_FILE["losing"]),
    pygame.mixer.Sound(SOUNDS_FILE["already guessed"]),
    pygame.mixer.Sound(SOUNDS_FILE["reveal feedback"])
]


# --------------------------- General functions
def update_active_buttons():
    """
    updates the active conditions of all the buttons in the game
    :return: None
    """
    global all_buttons, game_status, winning, losing

    # main menu buttons
    all_buttons[START_GAME].set_active(game_status == MAIN_MENU_STATUS)
    all_buttons[SETTINGS].set_active(game_status == MAIN_MENU_STATUS)
    all_buttons[INSTRUCTIONS].set_active(game_status == MAIN_MENU_STATUS)

    # settings buttons
    all_buttons[CODE_LEN_4].set_active(game_status == SETTINGS)
    all_buttons[CODE_LEN_5].set_active(game_status == SETTINGS)
    all_buttons[CODE_LEN_6].set_active(game_status == SETTINGS)
    all_buttons[DUPLICATES].set_active(game_status == SETTINGS)
    all_buttons[WORDLE_MODE].set_active(game_status == SETTINGS)

    # back to main and retry buttons
    all_buttons[BACK_TO_MENU].set_active(game_status != MAIN_MENU_STATUS)
    all_buttons[RETRY].set_active(game_status == GAME_STATUS and (winning or losing))


def check_buttons_clicked():
    """
    going through the buttons to see which was clicked and updating
    the game accordingly.
    :return: None
    """
    global game_status, num_of_digits, duplicates_allowed, wordle_mode

    for button in all_buttons:
        if button.is_hovered() and button.get_active():
            sound_effects[KEY_PRESS].play()
            if all_buttons.index(button) == START_GAME:
                initialize_game()
                game_status = GAME_STATUS
            elif all_buttons.index(button) == MAIN_MENU_STATUS :
                game_status = MAIN_MENU_STATUS
            elif all_buttons.index(button) == RETRY:
                initialize_game()
            elif all_buttons.index(button) == SETTINGS:
                game_status = SETTINGS_STATUS
            elif all_buttons.index(button) == CODE_LEN_4:
                num_of_digits = 4
            elif all_buttons.index(button) == CODE_LEN_5:
                num_of_digits = 5
            elif all_buttons.index(button) == CODE_LEN_6:
                num_of_digits = 6
            elif all_buttons.index(button) == DUPLICATES:
                duplicates_allowed = not duplicates_allowed
            elif all_buttons.index(button) == WORDLE_MODE:
                wordle_mode = not wordle_mode
            elif all_buttons.index(button) == INSTRUCTIONS:
                game_status = INSTRUCTIONS_STATUS


def check_buttons_hover():
    """
    checks for each button object if it's hovered,
    and changes its image accordingly
    :param: Button object to be checked
    :return: none
    """
    global all_buttons, sound_effects

    update_active_buttons()

    for button in all_buttons:
        if button.is_hovered() and button.get_active():
            if not button.get_hovered():  # if it's the first time it is hovered
                sound_effects[BUTTON_HOVER].play()
                button.set_hovered(True)
            button.set_color(text_font_render, GREEN)
        else:
            button.set_hovered(False)
            button.set_color(text_font_render, WHITE)


def get_xmiddle_pos_for_text(text_msg_render):
    """
    calculates the x position for a text render for it to appear
    in the middle of the screen
    :param text_msg_render: text render
    :return: integer representing the middle position for the given specific text
    """
    text_width = text_msg_render.get_size()[0]
    x_middle = WINDOW_WIDTH // 2 - text_width // 2
    return x_middle


def initialize_game():
    """
    re-initializing all the variables to start the game
    :return: None
    """
    global num_of_digits, line_width, lines_x_pos, code, guess, dig_txt_renders,\
        dig_txt_renders_pos, sent_guesses, sent_guesses_pos, all_feedbacks,\
        all_feedbacks_pos, msg, winning, losing

    line_width = (0.8 * WINDOW_WIDTH) // num_of_digits * (4 / 6)  # width of each guess line
    lines_x_pos = get_lines_x_pos(num_of_digits, line_width)  # x pos of each guess line
    code = code_generator()
    guess = ""  # the 4-digit code the user guesses
    dig_txt_renders = []  # the text renders for the written guess
    dig_txt_renders_pos = []  # the text renders position
    for i in range(num_of_digits):
        dig_txt_renders.append(digit_font_render.render('', False, GREEN))
        dig_txt_renders_pos.append((0, 0))
    sent_guesses = []  # all the previous guesses
    sent_guesses_pos = []  # tuple list for all the guess-renders positions
    all_feedbacks = []  # all the feedbacks the user recieves
    all_feedbacks_pos = []  # all the positions for the feedback renders
    msg = ''  # message for the user when winning/losing
    winning = False  # did the user win
    losing = False  # did the user lose


# --------------------------- Menu functions
def draw_main_menu():
    """
    Draws the main menu's screen
    :return: None
    """
    global msg

    screen.fill(BLACK)
    msg = ""

    # header
    header = header_font_render.render("Master Mind", True, WHITE)
    header_x = WINDOW_WIDTH // 2 - header.get_size()[0] // 2
    screen.blit(header, (header_x, HEADER_TEXT_Y))

    # buttons
    screen.blit(all_buttons[START_GAME].get_text_surface(), all_buttons[START_GAME].get_pos())
    screen.blit(all_buttons[SETTINGS].get_text_surface(), all_buttons[SETTINGS].get_pos())
    screen.blit(all_buttons[INSTRUCTIONS].get_text_surface(), all_buttons[INSTRUCTIONS].get_pos())


# --------------------------- Settings functions
def draw_settings():
    """
    Draws the settings menu's screen
    :return: None
    """
    global num_of_digits

    screen.fill(BLACK)

    # header
    header = header_font_render.render("SETTINGS", True, WHITE)
    header_x = WINDOW_WIDTH // 2 - header.get_size()[0] // 2
    screen.blit(header, (header_x, HEADER_TEXT_Y))

    # buttons' headers' text renders
    code_len_render = text_font_render.render("CODE LENGTH:", True, GREEN)
    duplicate_render = text_font_render.render("DUPLICATES:", True, GREEN)
    wordle_render = text_font_render.render("WORDLE MODE:", True, GREEN)

    # buttons and their headers

    # code length chooser
    screen.blit(code_len_render, CODE_LEN_TEXT_POS)
    all_buttons[num_of_digits].set_color(text_font_render, RED)  # turning the selected length on
    screen.blit(all_buttons[CODE_LEN_4].get_text_surface(), all_buttons[CODE_LEN_4].get_pos())
    screen.blit(all_buttons[CODE_LEN_5].get_text_surface(), all_buttons[CODE_LEN_5].get_pos())
    screen.blit(all_buttons[CODE_LEN_6].get_text_surface(), all_buttons[CODE_LEN_6].get_pos())

    # duplicates
    if duplicates_allowed:  # turning the button on or off
        all_buttons[DUPLICATES].set_color(text_font_render, RED)
        all_buttons[DUPLICATES].set_text(text_font_render, "ENABLED")
    else:
        all_buttons[DUPLICATES].set_color(text_font_render, WHITE)
        all_buttons[DUPLICATES].set_text(text_font_render, "DISABLED")
    screen.blit(duplicate_render, DUPLICATES_TEXT_POS)
    screen.blit(all_buttons[DUPLICATES].get_text_surface(), all_buttons[DUPLICATES].get_pos())

    # wordle mode
    screen.blit(wordle_render, WORDLE_MODE_TEXT_POS)
    if wordle_mode:
        all_buttons[WORDLE_MODE].set_color(text_font_render, RED)
        all_buttons[WORDLE_MODE].set_text(text_font_render, "ENABLED")
    else:
        all_buttons[WORDLE_MODE].set_color(text_font_render, WHITE)
        all_buttons[WORDLE_MODE].set_text(text_font_render, "DISABLED")
    screen.blit(all_buttons[WORDLE_MODE].get_text_surface(), all_buttons[WORDLE_MODE].get_pos())

    # back to main
    screen.blit(all_buttons[BACK_TO_MENU].get_text_surface(), all_buttons[BACK_TO_MENU].get_pos())


# --------------------------- Instructions functions
def draw_instructions():
    """
    draws the instructions screen
    :return: None
    """
    screen.fill(BLACK)

    # header
    header = header_font_render.render("INSTRUCTIONS", True, WHITE)
    header_x = WINDOW_WIDTH // 2 - header.get_size()[0] // 2
    screen.blit(header, (header_x, HEADER_TEXT_Y))

    text_surfaces = get_text_box(INSTRUCTIONS_FILE)
    for i, text_surface in enumerate(text_surfaces):
        pos = (INSTRUCTIONS_TEXT_POS[0], INSTRUCTIONS_TEXT_POS[1] + i * TEXT_FONT_SIZE)
        screen.blit(text_surface, pos)

    # back to main
    screen.blit(all_buttons[BACK_TO_MENU].get_text_surface(), all_buttons[BACK_TO_MENU].get_pos())


def get_text_box(text_path):
    """
    creates a text box to be displayed on screen
    :param text_path: string of a file route
    :return: text.surface[] containing all the lines
    splits the text into all its words, and loading them one by one
    """
    global text_font_render

    text_surfaces = []  # the array of text surfaces
    with open(text_path, 'r') as text:
        for line in text:
            text_surface = ins_text_font_render.render(line.replace("\n", ""), True, WHITE)
            text_surfaces.append(text_surface)
    return text_surfaces


# --------------------------- Game functions
def draw_game():
    """
    Draws the main game's screen
    :return: None
    """
    global num_of_digits, guess, all_buttons, winning, losing

    screen.fill(BLACK)

    # creating the main guess lines
    for line in range(num_of_digits):
        pygame.draw.line(screen, GREEN, (lines_x_pos[line], LINE_Y),
                         (lines_x_pos[line] + line_width, LINE_Y), LINES_GIRTH)

    # drawing the text cursor
    draw_text_cursor()

    # main menu and retry buttons
    screen.blit(all_buttons[BACK_TO_MENU].get_text_surface(), all_buttons[BACK_TO_MENU].get_pos())
    if winning or losing:
        screen.blit(all_buttons[RETRY].get_text_surface(), all_buttons[RETRY].get_pos())

    # writing the current guess
    write_guess()

    # function to display previous guesses and feedbacks
    draw_guesses()
    draw_feedbacks()


def get_lines_x_pos(num_of_digits, line_width):
    """
    generates the x position for the guess lines based on the number of digits in the code
    :param num_of_digits: integer indicating the number of digits
    :param line_width: integer indicating the width of each line
    :return: integer array containing the relevent x positions
    """
    lines_x = [0.1 * WINDOW_WIDTH + (0.8 * WINDOW_WIDTH) // num_of_digits * (1 / 6)]  # the pos of the first line
    for i in range(num_of_digits - 1):
        lines_x.append(lines_x[i] + line_width + (0.8 * WINDOW_WIDTH) // num_of_digits * (2 / 6))
    return lines_x


def code_generator():
    """
        generates a random digit code
        :return: digit string of the code
        """
    global duplicates_allowed

    new_code = ''
    while len(new_code) < num_of_digits:
        new_dig = random.randint(0, 9)
        if not duplicates_allowed:  # if the digit exists - change it
            while new_code.find(str(new_dig)) != -1:
                new_dig = random.randint(0, 9)

        new_code += str(new_dig)
    return new_code


def set_dig_renders(code_guess):
    """
    updates the digits render list
    the guess might not have a full length, therefore the try-except
    :param code_guess: the digit-string guess that needs to be displayed
    :return: None
    """
    global dig_txt_renders, dig_txt_renders_pos, lines_x_pos, line_width

    for index in range(len(dig_txt_renders)):
        # if there is a digit, add it to the render
        try:
            next_dig = digit_font_render.render(code_guess[index], False, GREEN)
            dig_txt_renders[index] = next_dig
            next_dig_x = lines_x_pos[index] + line_width // 2 - next_dig.get_size()[0] // 2
            next_dig_y = LINE_Y - next_dig.get_size()[1] - 2
            dig_txt_renders_pos[index] = (next_dig_x, next_dig_y)

        # if index out of range, put a blank
        except:
            dig_txt_renders[index] = digit_font_render.render('', False, GREEN)


def write_guess():
    """
    write's the user guess on the screen
    :return: None
    """
    global num_of_digits, lines_x_pos, line_width

    set_dig_renders(guess)
    for dig in range(num_of_digits):
        screen.blit(dig_txt_renders[dig], dig_txt_renders_pos[dig])


def draw_text_cursor():
    """
    responsible for the "blinking" of the text cursor
    :return: None
    """
    global screen, text_cursor_timer, cursor_is_visible, lines_x_pos

    current_time = pygame.time.get_ticks()
    if current_time - text_cursor_timer >= TEXT_CURSOR_INTERVAL:
        cursor_is_visible = not cursor_is_visible
        text_cursor_timer = current_time

    if cursor_is_visible:
        try:
            text_cursor_x = lines_x_pos[len(guess)] + TEXT_CURSOR_GIRTH
            pygame.draw.line(screen, GREEN, (text_cursor_x, TEXT_CURSOR_Y),
                             (text_cursor_x, TEXT_CURSOR_Y - TEXT_CURSOR_LENGTH), TEXT_CURSOR_GIRTH)

        except IndexError:
            cursor_is_visible = False


def update_guesses(new_guess):
    """
    calls all the relevent function when a new guess is inserted
    displays a msg if the guess was already guessed
    :param new_guess: string of the new guess
    :return: None
    """
    global sent_guesses, msg, code, all_feedbacks, all_feedbacks_pos

    if new_guess in sent_guesses:
        sound_effects[ALREADY_GUESSED].play()
        msg = "ALREADY GUESSED"

    else:
        sound_effects[SEND_GUESS].play()
        msg = ''
        new_feedback = get_feedback(new_guess, code)

        add_guess(new_guess)
        draw_guesses()
        pygame.display.flip()
        add_feedback(new_feedback)
        animate_feedback(new_feedback, all_feedbacks_pos[-1])


def add_guess(new_guess):
    """
    Updating previous guesses and feedbacks lists
    if the guess have already been tried, update msg
    :param new_guess: string containing the new guess
    :return: None
    """
    global sent_guesses, sent_guesses_pos, msg

    # creating a text render for the new guess
    new_guess_x = SENT_GUESS_X
    new_guess_y = SENT_GUESS_Y + 60 * len(sent_guesses)  # making the new guess lower after every guess
    # adding it to previous guesses
    sent_guesses.append(new_guess)
    # adding a new guess render position
    sent_guesses_pos.append((new_guess_x, new_guess_y))


def add_feedback(new_feedback):
    """
    adds a feedback and position to the feedback arrays
    :param new_feedback: string of the new guess
    :return: None
    """
    global all_feedbacks, all_feedbacks_pos

    new_feedback_x = FEEDBACK_X
    new_feedback_y = SENT_GUESS_Y + 60 * len(all_feedbacks)

    # adding it to the previous feedbacks
    all_feedbacks.append(new_feedback)
    # adding a new feedback render position
    all_feedbacks_pos.append((new_feedback_x, new_feedback_y))


def draw_guesses():
    """
    displays all the previous guesses of the player
    :return: None
    """
    global show_feedback_animation

    for i in range(len(sent_guesses)):
        text_surface = digit_font_render.render(sent_guesses[i], False, GREEN)
        screen.blit(text_surface, sent_guesses_pos[i])


def draw_feedbacks():
    """
    displays all the feedbacks
    :return: None
    """
    global all_feedbacks, all_feedbacks_pos

    for i in range(len(all_feedbacks)):
        text_surface = digit_font_render.render(all_feedbacks[i], True, GREEN)
        screen.blit(text_surface, all_feedbacks_pos[i])


def get_feedback(guess_check, code_check):
    """

    :param guess_check: digit-string containing a guess
    :param code_check: digit-string containing a code to compare to
    :return: string representing the feedback:
    V - right number at the right position
    * - right number at the wrong position
    _ - wrong number

    wordle mode - if true, the feedback is position sensitive
    """

    feedback = ['_' for i in range(num_of_digits)]  # the answer to be returned to the user

    # checking for correct digits in the correct position
    for i, dig in enumerate(guess_check):
        if dig == code_check[i]:
            feedback[i] = 'V'
            code_check = code_check.replace(dig, 'X', 1)
            guess_check = guess_check.replace(dig, 'X', 1)

    # checking for correct digit in the wrong positions
    for i, dig in enumerate(guess_check):
        if str.isdigit(dig) and code_check.find(dig) != -1:
            feedback[i] = '*'
            code_check = code_check.replace(dig, 'X', 1)
            guess_check = guess_check.replace(dig, 'X', 1)

    if not wordle_mode:
        feedback_dic = {'V': 1, '*': 2, '_': 3}
        return ''.join(sorted(feedback, key=lambda x: feedback_dic.get(x)))
    return ''.join(feedback)


def animate_feedback(feedback, pos):
    """
    create the animation of feedback-writing on screen
    :param feedback: string containing the feedback
    :param pos: tuple containing the position the feedback supposed to be displayed
    :return: None
    """
    global sound_effects

    sound_effects[REVEAL_FEEDBACK].play()
    pygame.time.delay(1500)
    for i in range(len(feedback)):
        feedback_text_surface = digit_font_render.render(feedback[:i+1], True, GREEN)
        screen.blit(feedback_text_surface, pos)
        pygame.display.flip()
        pygame.time.delay(100)


# --------------------------- Starting Menu variables
game_status = MAIN_MENU_STATUS  # determines what screen will be displayed

# --------------------------- Settings variables
duplicates_allowed = False  # are duplicates allowed
wordle_mode = False  # is wordle mode on

# --------------------------- Main Game variables
num_of_digits = 4
"""line_width = (0.8 * WINDOW_WIDTH) // num_of_digits * (4 / 6)  # width of each guess line
lines_x_pos = get_lines_x_pos(num_of_digits, line_width)  # x pos of each guess line
code = code_generator()
guess = ""  # the 4-digit code the user guesses
dig_txt_renders = []  # the text renders for the written guess
dig_txt_renders_pos = []  # the text renders position
for i in range(num_of_digits):
    dig_txt_renders.append(digit_font_render.render('', False, GREEN))
    dig_txt_renders_pos.append((0, 0))
sent_guesses = []  # all the previous guesses
sent_guesses_pos = []  # tuple list for all the guess-renders positions
all_feedbacks = []  # all the feedbacks the user recieves
all_feedbacks_pos = []  # all the positions for the feedback renders
msg = ''  # message for the user when winning/losing
winning = False  # did the user win
losing = False  # did the user lose
"""
initialize_game()
text_cursor_timer = 0  # inner timer to be compared with the game ticks
cursor_is_visible = True  # should the text cursor be displayed
show_feedback_animation = True  # should the feedback animation run

# --------------------------- Creating all the buttons
all_buttons = [  # list containing all the game buttons
    Button(START_BUTTON_POS, "START", text_font_render),
    Button(BACK_TO_MAIN_BUTTON_POS, "MAIN MENU", text_font_render),
    Button(RETRY_BUTTON_POS, "RETRY", text_font_render),
    Button(SETTINGS_BUTTON_POS, "SETTINGS", text_font_render),
    Button(CODE_LEN_4_BUTTON_POS, "4", text_font_render),
    Button(CODE_LEN_5_BUTTON_POS, "5", text_font_render),
    Button(CODE_LEN_6_BUTTON_POS, "6", text_font_render),
    Button(DUPLICATES_BUTTON_POS, "DISABLED", text_font_render),
    Button(WORDLE_MODE_BUTTON_POS, "DISABLED", text_font_render),
    Button(INSTRUCTIONS_BUTTON_POS, "INSTRUCTIONS", text_font_render)
]


finished = False

# --------------------------- Game loop
while not finished:

    if game_status == MAIN_MENU_STATUS:
        for event in pygame.event.get():
            # Clicking the close button
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    check_buttons_clicked()

        draw_main_menu()

    elif game_status == SETTINGS:

        for event in pygame.event.get():
            # Clicking the close button
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    check_buttons_clicked()

        draw_settings()

    elif game_status == INSTRUCTIONS_STATUS:
        for event in pygame.event.get():
            # Clicking the close button
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    check_buttons_clicked()

        draw_instructions()

    elif game_status == GAME_STATUS:

        for event in pygame.event.get():
            # Clicking the close button
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    check_buttons_clicked()

            elif event.type == pygame.KEYDOWN and not (winning or losing):
                msg = ""
                if event.unicode.isdigit() and len(guess) < num_of_digits:  # writing a guess
                    sound_effects[KEY_PRESS].play()
                    guess += event.unicode
                elif event.key == pygame.K_BACKSPACE:  # deleting a guess
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(guess) != num_of_digits:  # sending a complete guess
                        sound_effects[ALREADY_GUESSED].play()
                    else:
                        show_feedback_animation = True
                        update_guesses(guess)
                        if guess == code:
                            winning = True
                            sound_effects[WINNING].play()
                        elif len(sent_guesses) == MAX_GUESSES:
                            losing = True
                            sound_effects[LOSING].play()
                        guess = ""  # deleting the displayed guess

        # Background, number-code text lines
        draw_game()

        # checking for game over
        if winning:
            msg = 'You Win!'
        elif losing:
            msg = 'Game Over: ' + code

    msg_render = header_font_render.render(msg, False, RED)
    screen.blit(msg_render, (get_xmiddle_pos_for_text(msg_render), HEADER_TEXT_Y))
    check_buttons_hover()
    pygame.display.flip()
    # clock.tick(REFRESH_RATE)

pygame.quit()
