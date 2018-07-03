# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting

import CMenu
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import json

def main(stdscr):

    #Display Options Menu
    menu = CMenu.Menu()
    Menu_Title = 'Python Options'
    Menu_Options = ['Easy', 'Medium', 'Hard', 'God Mode', 'Enter Your Own Difficulty', 'Highscores', 'Exit']
    xy = menu.xy
    menu.GetMenu(Menu_Title, Menu_Options)
    menu.DoMenu()

    #Get Results From Options Menu
    if menu.selection == 0:
        speed = 200
    elif menu.selection  == 1:
        speed = 125
    elif menu.selection == 2:
        speed = 75
    elif menu.selection == 3:
        speed = 30
    elif menu.selection == 4:
        stdscr.clear()
        curses.echo()
        stdscr.addstr(0, 0, 'Enter Difficulty: ')
        speed = stdscr.getstr(0, 19, 3)
        speed = int(speed.decode('utf-8'))
    elif menu.selection == 5:
        stdscr.clear()
        with open('Highscores') as hs:
            scores = json.load(hs)
        for score in scores:
            msg = f"{score['name']} --> {score['score']}"
            stdscr.addstr(int(xy[1]/2 + scores.index(score)), int(xy[0]/2 - len(msg)/2), msg)
        stdscr.refresh()
        stdscr.nodelay(0)
        stdscr.getch()
        return
    elif menu.selection == 6:
        return

    #Start the NCurses Window
    curses.initscr()
    curses.start_color()
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    stdscr = curses.newwin(xy[1], xy[0], 0, 0)
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    stdscr.border(0)
    stdscr.nodelay(1)

    #Declare Variables to be Used Later
    key = KEY_RIGHT                                                    
    score = 0
    snake = [[4,10], [4,9], [4,8]]                                     
    food = [10,20]                                                     
    
    #Print First Food Object
    stdscr.addstr(food[0], food[1], '*', curses.color_pair(1))                       

    #Main Game Loop. Exits when ESC is pressed
    while key != 27 or go == True:
        #Draw Border and Populate It
        stdscr.border(0)
        stdscr.addstr(0, 2, 'Score : ' + str(score) + ' ')                
        stdscr.addstr(0, 27, ' SNAKE ')
        
        #More Variables to be Declared
        stdscr.timeout(int(speed))# - (len(snake) + len(snake)%int(speed/2))))
        prevKey = key                                                  

        #Get Movement of Snake
        event = stdscr.getch()
        key = key if event == -1 else event
        
        #Check for Space Key Hit and Pause
        if key == ord(' '):                                            
            key = -1                                                   
            while key != ord(' '):
                key = stdscr.getch()
            key = prevKey
            continue
        
        #Make Key Valid If Invalid
        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     
            key = prevKey
        
        #Prevent Snake From Killing Itself By Backing Up        
        if key == KEY_LEFT and prevKey == KEY_RIGHT:
            key = prevKey
        if key == KEY_RIGHT and prevKey == KEY_LEFT:
            key = prevKey
        if key == KEY_UP and prevKey == KEY_DOWN:
            key = prevKey
        if key == KEY_DOWN and prevKey == KEY_UP:
            key = prevKey


        # Calculates New Position For Snake Head As It Grows
        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        #Make Walls Teleport Snake To Other Side. Uncomment to Enable
        #if snake[0][0] == 0: snake[0][0] = 18
        #if snake[0][1] == 0: snake[0][1] = 58
        #if snake[0][0] == 19: snake[0][0] = 1
        #if snake[0][1] == 59: snake[0][1] = 1

        #Snake Dies If It Hits A Wall. Uncomment to Enable
        if snake[0][0] == 0 or snake[0][0] == (xy[1] - 1) or snake[0][1] == 0 or snake[0][1] == (xy[0] - 1): 
            event = stdscr.getch()
            break

        #Snake Dies If It Hits Itself
        if snake[0] in snake[1:]: 
            event = stdscr.getch()
            break

        #If Snake Eats Food
        if snake[0] == food:                                    
            food = []
            score += 1
            #Get New Coords for Food
            while food == []:
                food = [randint(1, (xy[1] - 2)), randint(1, (xy[0] - 2))]                 
                if food in snake: food = []
            stdscr.addstr(food[0], food[1], '*', curses.color_pair(1))
        #If No Food Eaten, Prevent Growth
        else:
            last = snake.pop()                                          
            stdscr.addch(last[0], last[1], ' ', curses.color_pair(3))
        #Draw Snake
        stdscr.addstr(snake[0][0], snake[0][1], 'x', curses.color_pair(3))
        #^^ Go Back To Start Of Loop ^^    
    
    #Game Over Proceedings

    #Clear Screen and Pring Score
    stdscr.clear()
    stdscr.addstr(0, int(xy[0]/2-5), 'GAME  OVER', curses.A_BLINK)
    w = (len(f'SCORE: {score}')/2)
    stdscr.addstr(int(xy[1]/2), int(xy[0]/2-w), f'SCORE: {score}', curses.A_BOLD)
    stdscr.refresh()
    #Only Exit When Key Is Pressed
    while True:
        from time import sleep
        sleep(.1)
        w = stdscr.getch()
        if w != curses.ERR:
            break
    #Get Highscores
    get_highscore = False
    with open('Highscores') as Highscores:
        scores = json.load(Highscores)
    while True:
        for pscore in scores:
            if score > pscore['score']:
                get_highscore = True
                pos = scores.index(pscore)
                break
        break
    if get_highscore:
        curses.echo()
        stdscr.nodelay(0)
        scores.pop()
        stdscr.clear()
        message = f'Congratulations! You got {pos + 1} place on the Scoreboard!'
        stdscr.addstr(int(xy[1]/2 + 1), int(xy[0]/2 - len(message)/2), message)
        stdscr.addstr(int(xy[1]/2), int(xy[0]/2 - 10), 'Enter Your Name: ___')
        stdscr.refresh()
        sleep(.5)
        name = stdscr.getstr(int(xy[1]/2), int(xy[0]/2 + 7), 3)
        name = str(name.decode('utf-8'))
        scores.insert(pos, {'name':name, 'score':score} )
        with open('Highscores', 'w') as h:
            json.dump(scores, h)
    #Display Play Again Menu
    game_over = CMenu.Menu()
    go_title = 'Play Again?'
    go_options = ['Yes!', 'No']
    game_over.GetMenu(go_title, go_options)
    game_over.DoMenu()
    #Restart Game If Play Again Selected
    if game_over.selection == 0:
        curses.wrapper(main)

#Run Game
curses.wrapper(main)
