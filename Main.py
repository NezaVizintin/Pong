# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

score1 = 0
score2 = 0

ball_pos = [0, 0]
ball_vel = [0, 0]

paddle1_pos = [[0, 240], [0, 160], [8, 160], [8, 240]]
paddle2_pos = [[592, 240], [592, 160], [600, 160], [600, 240]]

paddle1_vel = 0
paddle2_vel = 0

# helper functions

# move paddles
def move_paddle1(a):
    paddle1_pos[a][1] += paddle1_vel

def move_paddle2(a):
    paddle2_pos[a][1] += paddle2_vel
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT  / 2
    if direction == 'left' or LEFT:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)
    elif direction == 'right' or RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball('')
    score1, score2 = 0, 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #ball bounces from upper edge
    if ball_pos[1] <= 0 + BALL_RADIUS: #top
        ball_vel[1] = -ball_vel[1]
        
    if ball_pos[1] >= HEIGHT - BALL_RADIUS: #bottom
        ball_vel[1] = -ball_vel[1]
        
    # ball falls in gutter or bounces off paddle
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS: #left
        if ball_pos[1] > paddle1_pos[2][1] and ball_pos[1] < paddle1_pos[0][1]:
            ball_vel[0] = -ball_vel[0] + 1
            ball_vel[1] += 1
        else:
            score1 += 1
            spawn_ball('right')
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS: #right
        if ball_pos[1] > paddle2_pos[2][1] and ball_pos[1] < paddle2_pos[0][1]:
            ball_vel[0] = -ball_vel[0] - 1
            ball_vel[1] -= 1
        else:
            score2 += 1
            spawn_ball('left')
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 14, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_offscreen_up = paddle1_pos[2][1] + paddle1_vel
    paddle1_offscreen_down = paddle1_pos[0][1] + paddle1_vel

    paddle2_offscreen_up = paddle2_pos[2][1] + paddle2_vel
    paddle2_offscreen_down = paddle2_pos[0][1] + paddle2_vel

    if paddle1_offscreen_up > 0 and paddle1_offscreen_down < HEIGHT:
        move_paddle1(0)
        move_paddle1(1)
        move_paddle1(2)
        move_paddle1(3)
    
    if paddle2_offscreen_up > 0 and paddle2_offscreen_down < HEIGHT:
        move_paddle2(0)
        move_paddle2(1)
        move_paddle2(2)
        move_paddle2(3)
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 12, 'White', 'White')
    canvas.draw_polygon(paddle2_pos, 12, 'White', 'White')
        
    # draw scores
    canvas.draw_text(str(score1) + ':' + str(score2), (281, 30), 30, 'Yellow')

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
def button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', button_handler)

# start frame
new_game()
frame.start()
