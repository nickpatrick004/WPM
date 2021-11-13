import curses
from curses import wrapper
import time
import random

# Create Start Screen
def start_screen(stdscr):
    # Clear Screen, Add Welcome Text
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    # Display Screen
    stdscr.refresh()
    # Wait for Keyboard Entry
    stdscr.getkey()

# Display the text after a key is pressed
def display_text(stdscr, target, current, wpm=0):
    # First Add the Target Text
    stdscr.addstr(target)
    # Display the WPM
    stdscr.addstr(1, 0, f"WPM: {wpm }")

    # Loop through characters typed, add to screen
    for i, char in enumerate(current):
        # Find the correct character to compare to
        correct_char = target[i]
        # Set color to correct color
        color = curses.color_pair(1)
        # If wrong, change to incorrrect color
        if char != correct_char:
            color = curses.color_pair(2)
        # Add newly typed character to the screen
        stdscr.addstr(0, i, char, color)

# Read in a txt file, and choose a line to display
def load_text():
    # Open the file
    with open("text.txt", "r") as f:
        # Read one line at a time
        lines = f.readlines()
        # Randomly choose a line, strip off the newline characters
        return random.choice(lines).strip()


# Compute the WPM
def wpm_test(stdscr):
    # Load Target Text from a file
    target_text = load_text()
    # Initiate current text to and empty list
    current_text = []
    # Set default WPM
    wpm = 0
    # Grab the beginning time
    start_time = time.time()
    # Ensure that the counter will display with no keys pressed
    stdscr.nodelay(True)

    #
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        # Clear Screen
        stdscr.clear()
        # Display the target text, overwritten by typed text, and wpm
        display_text(stdscr, target_text, current_text, wpm)
        # Refresh the screen
        stdscr.refresh()

        # Join out list of current text into a string, compare to target text
        # If they match, stop looking for key press, quit
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # If they don't match, wait look for key press
        try:
            key = stdscr.getkey()
        except:
            continue

        # If ESCAPE pressed, exit
        # ESCAPE has ordinal value of 27
        if ord(key) == 27:
            break
        # Look for BACKSPACE/Delete(MacOS)
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            # If you have current text
            if len(current_text) > 0:
                # Remove the last character
                current_text.pop()
        # If any other key is pressed, and we have target text remaining, append the new character
        elif len(current_text) < len(target_text):
            current_text.append(key)

# Main program
def main(stdscr):
    # Set up curses color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Display Startup Screen
    start_screen(stdscr)

    # Loop to run test
    while True:
        # Run test to completion
        wpm_test(stdscr)

        # Once complete, ask for another round
        stdscr.addstr(2, 0, "You completed the test! Press any key to continue... ")
        # Wait on Input
        key = stdscr.getkey()

        # If ESCAPE, exit
        if ord(key) == 27:
            break


wrapper(main)
