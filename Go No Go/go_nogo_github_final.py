##go no go
# Import pychopy libraries
import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Rect, TextBox, DotStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy import event, data
from psychopy.visual.circle import Circle
import random

# Participant information popup box
exp_info = {'participant_nr': '', 'age': '21'}
dlg = DlgFromDict(exp_info)

p_name= exp_info['participant_nr']

# Initialize a fullscreen window 
win = Window(size=(1200, 800), fullscr=False, checkTiming=False)

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=False)

# Initialize a (global) clock
clock = Clock()

# Initialize keyboard
kb=Keyboard()
kb.clearEvents()

# 1 (hi fat) and 0 (low fat) dictates fat content of foods
# Change this path to your own Go No Go folder location
f_list = f"/Users/Go No Go/HF_LF_60.csv"
foods = pd.read_csv(f_list)
hf = foods[foods['fat']==1]
lf = foods[foods['fat']==0]

# Each participant will get a random selection every trial
lf = lf.sample(frac=0.4)
hf = hf.sample(frac=0.4)
trial_foods=pd.concat([lf,lf,lf,lf,hf])
trial_foods = trial_foods.sample(frac=1)

### WELCOME ROUTINE ###
# Create a welcome screen and show for 2 seconds
welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0, -1), font='Calibri')
welcome_txt_stim.draw()
win.flip()
wait(2)

### INSTRUCTION ROUTINE ###
instruct_txt = """ 
In this experiment, you will make choices between different types of food.

On each trial you will be presented with a food item.

Above this item you will either see a green dot or a red dot.

For items with the green dot press the 'space' bar, for items with the red dot 
do NOT press the 'space' bar.

(Press the ‘space’ bar to start the experiment!)
 """
     
# Show instructions and wait until response
instruct_txt = TextStim(win, instruct_txt, alignText='left', height=0.085)
instruct_txt.draw()
win.flip()
event.waitKeys(keyList=['space'])
kb.clearEvents()

for i in range(0,len(trial_foods)):
    trial=trial_foods.iloc[i]
    print(trial)
    
    # Adding a fixation for 0.5 mil
    t=TextStim(win,"+")
    t.draw()
    win.flip()
    wait(0.5)
 
    # Change this path to your own stimuli folder location
    path = "/Users/Go No Go/stimuli/" + trial.food
    print(trial.fat)
    if trial.fat==1:
        correct = "nogo"
    else: 
        correct = "go"
    im=ImageStim(win, path)
    
    # New clock 
    t_clock=Clock()
    response = "nogo"
    rt="NA"
   
    if correct == "go":
        circle_color = 'green'
    else: 
        circle_color = 'red'
    
    circle = Circle(win, radius=0.05, fillColor=circle_color, pos=(0,0.9))
   
    # If participant doesn't respond in .75 seconds then it will go onto the next image
    while t_clock.getTime() < .75:
        im.draw()
        circle.draw()
        win.flip()
        keys = kb.getKeys(['space','escape'], waitRelease=False)
        
        if keys:
            resp = keys[0].name
            rt = keys[0].rt
            if resp == 'escape':
                win.close()
                quit()
            else:
                response = "go"

    win.flip()
    wait(.5)
    
    # Adds response and reaction time to spreadsheet 
    trial_foods['response']=response
    trial_foods['rt']= rt
    trial_foods['correct_response'] = correct

# Change this path to where you want to save your data
trial_foods.to_csv('/Users/Go No Go/' + f"{p_name}_gonogo.csv", index=False)