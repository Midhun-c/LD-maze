from graphics import GraphWin, Rectangle, Point, Text  # type: ignore
import time
import random

WIDTH = 400
HEIGHT = 400
ROWS = 5
COLS = 5
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

LIGHT_PHASE_DURATION = 3  
DARK_PHASE_DURATION = 5 
TRANSITION_DURATION = 0.5
TRANSITION_STEPS =10 

def initialize_window():
    win = GraphWin("LD Maze Game", WIDTH, HEIGHT)
    return win

def draw_maze_grid(win, obstacles, phase):
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_WIDTH
            y1 = row * CELL_HEIGHT
            x2 = x1 + CELL_WIDTH
            y2 = y1 + CELL_HEIGHT
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            if phase == "light":
                rect.setFill("white")
                rect.setOutline("black")
            else:
                rect.setFill("black")
                rect.setOutline("white")
            rect.draw(win)
            if (row, col) in obstacles:
                obstacle = Rectangle(Point(x1, y1), Point(x2, y2))
                obstacle.setFill("brown")
                obstacle.draw(win)

def draw_player(win, row, col, phase):
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    player = Text(Point(x, y), "😊")
    if phase == "light":
        player.setFill("black")
    else:
        player.setFill("white")
    player.draw(win)
    return player

def draw_goal(win, row, col, phase):
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    goal = Text(Point(x, y), "🧈🧈🧈")
    if phase == "light":
        goal.setFill("black")
    else:
        goal.setFill("white")
    goal.draw(win)

def move_player(win, player, direction, obstacles, goal_row, goal_col):
    if direction == "Up":
        player.move(0, -CELL_HEIGHT)
    elif direction == "Down":
        player.move(0, CELL_HEIGHT)
    elif direction == "Left":
        player.move(-CELL_WIDTH, 0)
    elif direction == "Right":
        player.move(CELL_WIDTH, 0)

    player_pos = player.getAnchor()
    player_row = player_pos.getY() // CELL_HEIGHT
    player_col = player_pos.getX() // CELL_WIDTH
    
    if is_collision(player_row, player_col, obstacles):
        message(win, "🅶🅰🅼🅴 🅾🆅🅴🆁")
        game_over()
    
    if player_row == goal_row and player_col == goal_col:
        message(win, "🆈🅾🆄 🆆🅾🅽")
        game_win()

def is_collision(row, col, obstacles):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return True
    if (row, col) in obstacles:
        return True
    return False

def message(win, mess):
    x = 2 * CELL_WIDTH + CELL_WIDTH // 2
    y = 2 * CELL_HEIGHT + CELL_HEIGHT // 2
    message = Text(Point(x, y), mess)
    message.setSize(18)
    message.setTextColor("red")
    message.draw(win)

def game_over():
    print("Game Over!")
    time.sleep(2)
    exit(1)

def game_win():
    print("Congratulations! You've reached the goal and won the game!")
    time.sleep(2)
    exit(1)

def color_rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_overlay(win, darkness):
    overlay = Rectangle(Point(0, 0), Point(WIDTH, HEIGHT))
    grey_value = int(255 * (1 - darkness))  
    grey_color = color_rgb(grey_value, grey_value, grey_value)
    overlay.setFill(grey_color)
    overlay.setOutline(grey_color)
    overlay.draw(win)
    return overlay

def toggle_phase(win, phase):
    steps = TRANSITION_STEPS
    step_duration = TRANSITION_DURATION / steps
    if phase == "light":
        for i in range(steps):
            draw_overlay(win, i / steps)
            time.sleep(step_duration)
    elif phase == "dark":
        for i in range(steps):
            draw_overlay(win, 1 - (i / steps))
            time.sleep(step_duration)
    if phase == "light":
        draw_overlay(win, 1)
    else:
        draw_overlay(win, 0)

def main():
    win = initialize_window()
    phase = "dark"
    obstacles = [(row, col) for row in range(ROWS) for col in range(COLS) if random.random() < 0.2 and not ((row == 0 and col == 0) or (row == ROWS-1 and col == COLS-1))]

    draw_maze_grid(win, obstacles, phase)

    player_row = 0
    player_col = 0
    player = draw_player(win, player_row, player_col, phase)

    goal_row = ROWS - 1
    goal_col = COLS - 1
    draw_goal(win, goal_row, goal_col, phase)

    phase_start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - phase_start_time

        if phase == "dark" and elapsed_time >= DARK_PHASE_DURATION:
            phase = "light"
            phase_start_time = current_time
            toggle_phase(win, phase)
            draw_maze_grid(win, obstacles, phase)
            player = draw_player(win, player_row, player_col, phase)
            draw_goal(win, goal_row, goal_col, phase)
        elif phase == "light" and elapsed_time >= LIGHT_PHASE_DURATION:
            phase = "dark"
            phase_start_time = current_time
            toggle_phase(win, phase)
            draw_maze_grid(win, obstacles, phase)
            player = draw_player(win, player_row, player_col, phase)
            draw_goal(win, goal_row, goal_col, phase)

        if phase == "light":
            if win.checkKey():
                message(win,"🅶🅰🅼🅴 🅾🆅🅴🆁")
                game_over()
        

        elif phase == "dark":
            key = win.checkKey()
            if key in ["Up", "Down", "Left", "Right"]:
                move_player(win, player, key, obstacles, goal_row, goal_col)
                if key == "Up":
                    player_row -= 1
                elif key == "Down":
                    player_row += 1
                elif key == "Left":
                    player_col -= 1
                elif key == "Right":
                    player_col += 1
            if key == "q":
                break
        else:
            win.checkKey()

    win.close()

if __name__ == "__main__":
    main()
