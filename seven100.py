import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)
RED = (220, 20, 60)
GREEN = (34, 139, 34)

# Fonts
TITLE_FONT = pygame.font.SysFont('arial', 48, bold=True)
BUTTON_FONT = pygame.font.SysFont('arial', 32)
TEXT_FONT = pygame.font.SysFont('arial', 24)
INPUT_FONT = pygame.font.SysFont('arial', 28)
DICE_FONT = pygame.font.SysFont('arial', 100, bold=True)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GridGuard")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game States
MAIN_MENU = 'main_menu'
START_MENU = 'start_menu'
SETTINGS = 'settings'
ACHIEVEMENTS = 'achievements'
ENCYCLOPEDIA = 'encyclopedia'
ROLE_SELECTION = 'role_selection'
USERNAME_INPUT = 'username_input'
DICE_ROLL = 'dice_roll'
SHOW_RESULT = 'show_result'
ROLE_INFO = 'role_info'
IN_GAME = 'in_game'

# Current game state
game_state = MAIN_MENU

# Player Data
players = {
    "Player1": {"role": None, "username": ""},
    "Player2": {"role": None, "username": ""}
}

# Role Information
ROLE_INFO_DATA = {
    "Aviation Network Security Specialist": {
        "Focus": [
            "Securing the airline's network infrastructure.",
            "Safeguarding communication links between aircraft and ground control.",
            "Monitoring for suspicious activities."
        ],
        "Tools": [
            "Network Intrusion Detection System (NIDS)",
            "Firewall Configuration Console",
            "Secure Communication Protocols"
        ]
    },
    "Cyber Forensics Analyst": {
        "Focus": [
            "Analyzing compromised systems.",
            "Detecting malware or unauthorized code within flight control software.",
            "Identifying the hackers' footprints."
        ],
        "Tools": [
            "Forensic Analysis Suite",
            "Malware Disassembler",
            "System Integrity Verifier"
        ]
    }
}

# Button Class
class Button:
    def _init_(self, text, rect, color, hover_color, font, action=None):
        """
        Initialize a Button instance.

        :param text: Text displayed on the button.
        :param rect: Tuple defining the button's position and size (x, y, width, height).
        :param color: Button color when not hovered.
        :param hover_color: Button color when hovered.
        :param font: Pygame font object for rendering text.
        :param action: Function to execute when the button is clicked.
        """
        self.text = text
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.action = action

    def draw(self, surface):
        """
        Draw the button on the given surface.

        :param surface: Pygame surface to draw the button on.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Render the text
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """
        Check if the button is clicked.

        :param event: Pygame event.
        :return: True if clicked, else False.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Function to create main menu buttons
def create_main_menu_buttons():
    buttons = []
    button_width = 200
    button_height = 60
    spacing = 20
    start_x = (SCREEN_WIDTH - button_width) // 2
    start_y = SCREEN_HEIGHT // 2 - (4 * (button_height + spacing)) // 2

    labels = ['Start', 'Settings', 'Achievements', 'Encyclopedia']
    actions = [goto_start_menu, goto_settings, goto_achievements, goto_encyclopedia]

    for i in range(4):
        rect = (start_x, start_y + i * (button_height + spacing), button_width, button_height)
        color = BLUE if labels[i] == 'Start' else GRAY
        hover_color = LIGHT_GRAY
        button = Button(labels[i], rect, color, hover_color, BUTTON_FONT, actions[i])
        buttons.append(button)

    return buttons

# Function to create start menu buttons (game modes)
def create_start_menu_buttons():
    buttons = []
    button_width = 300
    button_height = 80
    spacing_x = 50
    spacing_y = 50
    start_x = (SCREEN_WIDTH - (2 * button_width + spacing_x)) // 2
    start_y = SCREEN_HEIGHT // 4  # Adjusted for more buttons

    labels = [
        'Airline Cybersecurity',
        'Smart Grid Protection',
        'Military Software Breach',
        'Corporate Website Defacement'
    ]
    actions = [lambda: select_mode(labels[0]),
               lambda: select_mode(labels[1]),
               lambda: select_mode(labels[2]),
               lambda: select_mode(labels[3])]

    for i in range(4):
        row = i // 2
        col = i % 2
        x = start_x + col * (button_width + spacing_x)
        y = start_y + row * (button_height + spacing_y)
        rect = (x, y, button_width, button_height)
        color = RED
        hover_color = LIGHT_GRAY
        button = Button(labels[i], rect, color, hover_color, BUTTON_FONT, actions[i])
        buttons.append(button)

    # Back Button
    back_rect = (20, SCREEN_HEIGHT - 70, 120, 50)
    back_button = Button('Back', back_rect, DARK_GRAY, LIGHT_GRAY, BUTTON_FONT, goto_main_menu)
    buttons.append(back_button)

    return buttons

# Function to create role selection buttons
def create_role_buttons():
    buttons = []
    button_width = 350
    button_height = 80
    spacing = 50
    start_x = (SCREEN_WIDTH - (button_width * 2 + spacing)) // 2
    start_y = SCREEN_HEIGHT // 3

    labels = ["Aviation Network Security Specialist", "Cyber Forensics Analyst"]
    actions = [lambda: assign_role(labels[0]),
               lambda: assign_role(labels[1])]

    for i in range(2):
        x = start_x + i * (button_width + spacing)
        y = start_y
        rect = (x, y, button_width, button_height)
        color = BLUE if "Specialist" in labels[i] else RED
        hover_color = LIGHT_GRAY
        button = Button(labels[i], rect, color, hover_color, BUTTON_FONT, actions[i])
        buttons.append(button)

    return buttons

# Function to create a placeholder back button for Settings, Achievements, Encyclopedia
def create_placeholder_back_button():
    back_rect = (20, SCREEN_HEIGHT - 70, 120, 50)
    back_button = Button('Back', back_rect, DARK_GRAY, LIGHT_GRAY, BUTTON_FONT, goto_main_menu)
    return back_button

# Navigation Functions
def goto_main_menu():
    global game_state
    game_state = MAIN_MENU

def goto_start_menu():
    global game_state
    game_state = START_MENU

def goto_settings():
    global game_state
    game_state = SETTINGS

def goto_achievements():
    global game_state
    game_state = ACHIEVEMENTS

def goto_encyclopedia():
    global game_state
    game_state = ENCYCLOPEDIA

def select_mode(mode_name):
    """
    Handle selection of a game mode.
    """
    global selected_mode, game_state
    selected_mode = mode_name
    print(f"Selected Mode: {selected_mode}")
    # Navigate to role selection
    game_state = ROLE_SELECTION

def assign_role(role_name):
    """
    Assign role to the current player and assign the opposite role to the other player.
    """
    global current_player, other_player, game_state
    players[current_player]['role'] = role_name
    other_player = "Player2" if current_player == "Player1" else "Player1"
    players[other_player]['role'] = "Cyber Forensics Analyst" if role_name == "Aviation Network Security Specialist" else "Aviation Network Security Specialist"
    print(f"{current_player} assigned role: {role_name}")
    print(f"{other_player} automatically assigned role: {players[other_player]['role']}")
    # Proceed to username input
    game_state = USERNAME_INPUT
    # Set the next player for username entry
    set_current_player(other_player)

def set_current_player(player):
    """
    Set the current player for actions like role selection or username input.
    """
    global current_player
    current_player = player

def handle_username_input(event):
    """
    Handle the username input for players.
    """
    global input_active, input_text, game_state
    if event.key == pygame.K_RETURN:
        if input_text.strip() != "":
            players[current_player]['username'] = input_text.strip()
            print(f"{current_player} entered username: {players[current_player]['username']}")
            input_text = ""
            # Check if both players have entered usernames
            if players["Player1"]['username'] != "" and players["Player2"]['username'] != "":
                # Proceed to dice rolling
                game_state = DICE_ROLL
                initiate_dice_roll()
            else:
                # Switch to the other player for username input
                switch_player()
    elif event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]
    else:
        if len(input_text) < 20:
            input_text += event.unicode

def switch_player():
    """
    Switch the current player between Player1 and Player2.
    """
    global current_player
    current_player = "Player2" if current_player == "Player1" else "Player1"

def initiate_dice_roll():
    """
    Initialize dice rolling for the first player.
    """
    global dice_animation, current_dice_player, dice_rolls
    dice_animation = True
    current_dice_player = "Player1" if dice_rolls["Player1"] == 0 else "Player2"
    dice_rolls[current_dice_player] = 0

def roll_dice():
    """
    Simulate a dice roll.
    """
    return random.randint(1, 6)

def update_dice_animation():
    """
    Update the dice animation by displaying random numbers until the user stops it.
    """
    global dice_rolls, dice_animation, current_dice_player, game_state
    # Assign a random number to simulate rolling
    dice_rolls[current_dice_player] = roll_dice()

def determine_turn_order():
    """
    Determine which player goes first based on dice rolls.
    """
    global first_player, second_player
    p1_roll = dice_rolls["Player1"]
    p2_roll = dice_rolls["Player2"]
    if p1_roll > p2_roll:
        first_player = "Player1"
        second_player = "Player2"
    elif p2_roll > p1_roll:
        first_player = "Player2"
        second_player = "Player1"
    else:
        # Tie: re-roll
        initiate_dice_roll()

def show_result():
    """
    Display the result of the dice rolls and determine the turn order.
    """
    global game_state
    screen.fill(WHITE)
    # Title
    title_surf = TITLE_FONT.render("Dice Roll Result", True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
    screen.blit(title_surf, title_rect)

    # Display both dice rolls
    p1_username = players["Player1"]['username']
    p2_username = players["Player2"]['username']
    p1_role = players["Player1"]['role']
    p2_role = players["Player2"]['role']
    p1_roll = dice_rolls["Player1"]
    p2_roll = dice_rolls["Player2"]

    p1_text = f"{p1_role}: {p1_username} rolled {p1_roll}"
    p2_text = f"{p2_role}: {p2_username} rolled {p2_roll}"

    p1_surf = TEXT_FONT.render(p1_text, True, BLACK)
    p1_rect = p1_surf.get_rect(center=(SCREEN_WIDTH//2, 200))
    screen.blit(p1_surf, p1_rect)

    p2_surf = TEXT_FONT.render(p2_text, True, BLACK)
    p2_rect = p2_surf.get_rect(center=(SCREEN_WIDTH//2, 250))
    screen.blit(p2_surf, p2_rect)

    # Determine winner
    if first_player and second_player:
        winner_text = f"{first_player} ({players[first_player]['username']}) goes first!"
        winner_surf = TEXT_FONT.render(winner_text, True, GREEN)
    else:
        winner_text = "It's a tie! Re-rolling..."
        winner_surf = TEXT_FONT.render(winner_text, True, RED)
    winner_rect = winner_surf.get_rect(center=(SCREEN_WIDTH//2, 350))
    screen.blit(winner_surf, winner_rect)

    # Button to continue or re-roll
    if first_player and second_player:
        action = show_role_info
        button_text = "Continue"
    else:
        action = initiate_dice_roll
        button_text = "Re-roll"

    continue_button = Button(button_text, (SCREEN_WIDTH//2 - 100, 400, 200, 60), BLUE, LIGHT_GRAY, BUTTON_FONT, action)
    continue_button.draw(screen)

    pygame.display.flip()

    # Wait for button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if continue_button.is_clicked(event):
                waiting = False
                break
        clock.tick(60)

def show_role_info():
    """
    Display the focus and tools based on the winning player's role.
    """
    global game_state
    screen.fill(WHITE)
    # Title
    title_text = f"{first_player}'s Role: {players[first_player]['role']}"
    title_surf = TITLE_FONT.render(title_text, True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
    screen.blit(title_surf, title_rect)

    # Focus
    focus = ROLE_INFO_DATA[players[first_player]['role']]['Focus']
    focus_title = TEXT_FONT.render("Focus:", True, BLACK)
    screen.blit(focus_title, (50, 150))
    for i, line in enumerate(focus):
        line_surf = TEXT_FONT.render(line, True, BLACK)
        screen.blit(line_surf, (70, 180 + i * 30))

    # Tools
    tools = ROLE_INFO_DATA[players[first_player]['role']]['Tools']
    tools_title = TEXT_FONT.render("Tools:", True, BLACK)
    screen.blit(tools_title, (450, 150))
    for i, line in enumerate(tools):
        line_surf = TEXT_FONT.render(line, True, BLACK)
        screen.blit(line_surf, (470, 180 + i * 30))

    # Button to proceed to game
    proceed_button = Button('Proceed to Game', (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 60), GREEN, LIGHT_GRAY, BUTTON_FONT, proceed_to_game)
    proceed_button.draw(screen)

    pygame.display.flip()

    # Wait for button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if proceed_button.is_clicked(event):
                waiting = False
                break
        clock.tick(60)

def proceed_to_game():
    """
    Transition to the in-game state.
    """
    global game_state
    game_state = IN_GAME
    # Placeholder for actual game mechanics

def draw_in_game():
    """
    Display the in-game screen. Placeholder for actual game mechanics.
    """
    screen.fill(WHITE)
    # Title
    title_surf = TITLE_FONT.render("Game Started!", True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
    screen.blit(title_surf, title_rect)

    # Placeholder Text
    placeholder_surf = TEXT_FONT.render("Game mechanics coming soon!", True, DARK_GRAY)
    placeholder_rect = placeholder_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(placeholder_surf, placeholder_rect)

    pygame.display.flip()

# Initialize Buttons
main_menu_buttons = create_main_menu_buttons()
start_menu_buttons = create_start_menu_buttons()
placeholder_back_button = create_placeholder_back_button()

# Current Player for Role Selection and Username Input
current_player = "Player1"  # Start with Player1

# Dice Rolling Variables
dice_animation = False
current_dice_player = None
dice_rolls = {"Player1": 0, "Player2": 0}

# Turn Order Variables
first_player = None
second_player = None

# Text Input Variables
input_active = False  # Initialize input_active
input_text = ""

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle events based on game state
        if game_state == MAIN_MENU:
            for button in main_menu_buttons:
                if button.is_clicked(event):
                    button.action()

        elif game_state == START_MENU:
            for button in start_menu_buttons:
                if button.is_clicked(event):
                    button.action()

        elif game_state in [SETTINGS, ACHIEVEMENTS, ENCYCLOPEDIA]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if placeholder_back_button.is_clicked(event):
                    placeholder_back_button.action()

        elif game_state == ROLE_SELECTION:
            role_buttons = create_role_buttons()
            for button in role_buttons:
                if button.is_clicked(event):
                    button.action()

        elif game_state == USERNAME_INPUT:
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 50)
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    handle_username_input(event)

        elif game_state == DICE_ROLL:
            if event.type == pygame.KEYDOWN and dice_animation:
                # Stop the dice animation upon any key press
                dice_animation = False
                # Assign the final roll
                final_roll = roll_dice()
                dice_rolls[current_dice_player] = final_roll
                print(f"{current_dice_player} rolled: {final_roll}")
                # Proceed to show results if both players have rolled
                if current_dice_player == "Player1":
                    initiate_dice_roll()  # Start rolling for Player2
                else:
                    determine_turn_order()
                    game_state = SHOW_RESULT

    # Update Game State
    if game_state == MAIN_MENU:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("GridGuard", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Draw buttons
        for button in main_menu_buttons:
            button.draw(screen)

    elif game_state == START_MENU:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Select Game Mode", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title_surf, title_rect)

        # Draw buttons
        for button in start_menu_buttons:
            button.draw(screen)

    elif game_state == SETTINGS:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Settings", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Placeholder Content
        placeholder_surf = TEXT_FONT.render("Settings coming soon!", True, DARK_GRAY)
        placeholder_rect = placeholder_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(placeholder_surf, placeholder_rect)

        # Draw Back Button
        placeholder_back_button.draw(screen)

    elif game_state == ACHIEVEMENTS:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Achievements", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Placeholder Content
        placeholder_surf = TEXT_FONT.render("Achievements coming soon!", True, DARK_GRAY)
        placeholder_rect = placeholder_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(placeholder_surf, placeholder_rect)

        # Draw Back Button
        placeholder_back_button.draw(screen)

    elif game_state == ENCYCLOPEDIA:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Encyclopedia", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Placeholder Content
        placeholder_surf = TEXT_FONT.render("Encyclopedia coming soon!", True, DARK_GRAY)
        placeholder_rect = placeholder_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(placeholder_surf, placeholder_rect)

        # Draw Back Button
        placeholder_back_button.draw(screen)

    elif game_state == ROLE_SELECTION:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Select Your Role", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Instruction
        instruction_surf = TEXT_FONT.render(f"{current_player}, choose your role:", True, BLACK)
        instruction_rect = instruction_surf.get_rect(center=(SCREEN_WIDTH//2, 180))
        screen.blit(instruction_surf, instruction_rect)

        # Create and draw role buttons
        role_buttons = create_role_buttons()
        for button in role_buttons:
            button.draw(screen)

    elif game_state == USERNAME_INPUT:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Enter Username", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_surf, title_rect)

        # Prompt
        prompt_text = f"{current_player}, enter your username:"
        prompt_surf = TEXT_FONT.render(prompt_text, True, BLACK)
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(prompt_surf, prompt_rect)

        # Input box
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 50)
        pygame.draw.rect(screen, LIGHT_GRAY, input_box, 2 if not input_active else 4)

        # Render the current input text
        input_text_surf = INPUT_FONT.render(input_text, True, BLACK)
        input_text_rect = input_text_surf.get_rect(center=input_box.center)
        screen.blit(input_text_surf, input_text_rect)

        # Instruction
        instruction_surf = TEXT_FONT.render("Type your name and press Enter to save.", True, DARK_GRAY)
        instruction_rect = instruction_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        screen.blit(instruction_surf, instruction_rect)

    elif game_state == DICE_ROLL:
        screen.fill(WHITE)
        # Title
        title_surf = TITLE_FONT.render("Dice Roll", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title_surf, title_rect)

        # Current Player Rolling
        rolling_text = f"{current_dice_player} is rolling the dice! Press any key to stop..."
        rolling_surf = TEXT_FONT.render(rolling_text, True, BLACK)
        rolling_rect = rolling_surf.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(rolling_surf, rolling_rect)

        # Dice Animation or Final Roll
        if dice_animation:
            # Display a random number to simulate rolling
            update_dice_animation()
            dice_number = dice_rolls[current_dice_player]
            dice_surf = DICE_FONT.render(str(dice_number), True, BLACK)
            dice_rect = dice_surf.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(dice_surf, dice_rect)
        else:
            # Show final dice roll (already handled in event)
            dice_number = dice_rolls[current_dice_player]
            dice_surf = DICE_FONT.render(str(dice_number), True, BLACK)
            dice_rect = dice_surf.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(dice_surf, dice_rect)

    elif game_state == SHOW_RESULT:
        show_result()

    elif game_state == ROLE_INFO:
        show_role_info()

    elif game_state == IN_GAME:
        draw_in_game()

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

def show_role_info():
    """
    Display the focus and tools based on the winning player's role.
    """
    global game_state
    game_state = ROLE_INFO
    winner_role = players[first_player]['role']

    # Clear the screen
    screen.fill(WHITE)

    # Title: Display Role
    title_text = f"{first_player}'s Role: {winner_role}"
    title_surf = TITLE_FONT.render(title_text, True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)

    # Display Role Focus
    focus_title = TEXT_FONT.render("Focus:", True, BLACK)
    screen.blit(focus_title, (50, 150))
    focus_items = ROLE_INFO_DATA[winner_role]["Focus"]
    y_offset = 180
    for item in focus_items:
        focus_item_surf = TEXT_FONT.render(f"- {item}", True, BLACK)
        screen.blit(focus_item_surf, (70, y_offset))
        y_offset += 30

    # Display Role Tools
    tools_title = TEXT_FONT.render("Tools:", True, BLACK)
    screen.blit(tools_title, (450, 150))
    tools_items = ROLE_INFO_DATA[winner_role]["Tools"]
    y_offset = 180
    for item in tools_items:
        tools_item_surf = TEXT_FONT.render(f"- {item}", True, BLACK)
        screen.blit(tools_item_surf, (470, y_offset))
        y_offset += 30

    # Continue Button to Proceed to the Game
    proceed_button = Button(
        'Proceed to Game',
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 60),
        GREEN, LIGHT_GRAY, BUTTON_FONT, proceed_to_game
    )
    proceed_button.draw(screen)

    pygame.display.flip()

    # Wait for button click to proceed
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if proceed_button.is_clicked(event):
                waiting = False
                break
        clock.tick(60)

def proceed_to_game():
    """
    Transition to the in-game state.
    """
    global game_state
    game_state = IN_GAME  # Placeholder for in-game mechanics
    draw_in_game()

def draw_in_game():
    """
    Display the in-game screen. Placeholder for actual game mechanics.
    """
    screen.fill(WHITE)

    # Title
    title_surf = TITLE_FONT.render("Game Started!", True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)

    # Placeholder Content
    placeholder_surf = TEXT_FONT.render(
        "In-game mechanics coming soon...", True, DARK_GRAY
    )
    placeholder_rect = placeholder_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(placeholder_surf, placeholder_rect)

    pygame.display.flip()

    # Game loop placeholder (exit on quit event)
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)


# Quit Pygame
pygame.quit()
sys.exit()