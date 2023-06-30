import pytrie
import numpy as np
from collections import deque
import tkinter as tk
from tkinter import messagebox
import threading
from collections import OrderedDict

trie = pytrie.StringTrie()

common_names = set([
    'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph',
    'thomas', 'charles', 'christopher', 'daniel', 'matthew', 'anthony', 'donald',
    'mark', 'paul', 'steven', 'andrew', 'kenneth', 'joshua', 'george', 'kevin',
    'brian', 'edward', 'ronald', 'timothy', 'jason', 'jeffrey', 'ryan', 'jacob',
    'gary', 'nicholas', 'eric', 'stephen', 'jonathan', 'larry', 'justin', 'scott',
    'brandon', 'frank', 'benjamin', 'gregory', 'samuel', 'raymond', 'patrick',
    'alexander', 'jack', 'dennis', 'jerry', 'tyler', 'aaron', 'jose', 'henry',
    'douglas', 'adam', 'peter', 'nathan', 'zachary', 'walter', 'kyle', 'harold',
    'carl', 'jeremy', 'keith', 'roger', 'gerald', 'ethan', 'arthur', 'terry',
    'christian', 'sean', 'lawrence', 'austin', 'joe', 'noah', 'jesse', 'albert',
    'bryan', 'billy', 'bruce', 'willie', 'jordan', 'dylan', 'alan', 'ralph',
    'gabriel', 'roy', 'juan', 'wayne', 'eugene', 'logan', 'randy', 'louis',
    'russell', 'vincent', 'philip', 'bobby', 'johnny', 'bradley',
    
    # Adding female names
    'mary', 'jennifer', 'linda', 'patricia', 'elizabeth', 'susan', 'jessica',
    'sarah', 'karen', 'nancy', 'margaret', 'lisa', 'betty', 'dorothy', 'sandra',
    'ashley', 'kimberly', 'donna', 'emily', 'michelle', 'carol', 'amanda',
    'melissa', 'deborah', 'stephanie', 'rebecca', 'laura', 'sharon', 'cynthia',
    'kathleen', 'amy', 'shirley', 'angela', 'helen', 'anna', 'brenda', 'pamela',
    'nicole', 'ruth', 'katherine', 'samantha', 'christine', 'emma', 'catherine',
    'debra', 'virginia', 'rachel', 'carolyn', 'janet', 'elaine', 'marie',
    'heather', 'diane', 'julie', 'joyce', 'victoria', 'kelly', 'christina',
    'joan', 'evelyn', 'olivia', 'phyllis', 'judy', 'cheryl', 'megan', 'andrea',
    'hannah', 'martha', 'jacqueline', 'erin', 'gloria', 'kathryn', 'ann',
    'rose', 'teresa', 'doris', 'sara', 'janice', 'julia', 'marie', 'madison',
    'grace', 'judy', 'theresa', 'beverly', 'denise', 'marilyn', 'amber', 'danielle',
    'abigail', 'brittany', 'rose', 'diana', 'natalie', 'sophia', 'alexis',
    'lori', 'kayla', 'jane'
])

valid_words = set()

def load_dictionary():
    global valid_words
    # load words from a text file and store them in a trie
    with open('filtered_words.txt', 'r') as f:
        words = [word.strip().lower() for word in f.readlines()]
        valid_words = set(words)

        for word in words:

            #continue over words with length one or two
            if len(word) <= 2:
                continue

            # Add all prefixes of the word to the trie
            for i in range(len(word)):
                prefix = word[:i + 1]
                if prefix not in trie:
                    trie[prefix] = prefix

            # Mark the complete word with a '*'
            trie[word + '*'] = word
            print(word)

# Start a thread to load the dictionary
threading.Thread(target=load_dictionary).start()

def search(i, j, grid, visited, prefix, words_found, trie):
    if prefix not in trie:
        return
    
    #stop search if prefix is a common name
    if prefix in common_names:
        return
    
    # Check if the prefix is a complete word
    if prefix + '*' in trie:
        words_found.append(prefix)

    for dx, dy in NEIGHBORS:
        ni, nj = i + dx, j + dy
        if valid(ni, nj, visited):
            visited[ni][nj] = True
            search(ni, nj, grid, visited, prefix + grid[ni][nj], words_found, trie)
            visited[ni][nj] = False


# create a list of neighbors
neighbors = []

def create_neighbors():
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                neighbors.append((dx, dy))
    return neighbors

# define possible moves
NEIGHBORS = create_neighbors()

def valid(i, j, visited):
    return 0 <= i < 4 and 0 <= j < 4 and not visited[i][j]

def search(i, j, grid, visited, prefix, words_found, trie):
    global valid_words

    if prefix not in trie:
        return

    # Check if the prefix is a complete word and exists in valid_words
    if prefix + '*' in trie and prefix in valid_words:
        words_found.append(prefix)


    for dx, dy in NEIGHBORS:
        ni, nj = i + dx, j + dy
        if valid(ni, nj, visited):
            visited[ni][nj] = True
            search(ni, nj, grid, visited, prefix + grid[ni][nj], words_found, trie)
            visited[ni][nj] = False

def solve(grid, trie):
    words_found = []
    visited = np.zeros((4, 4), dtype=bool)
    
    for i in range(4):
        for j in range(4):
            visited[i][j] = True
            search(i, j, grid, visited, grid[i][j], words_found, trie)
            visited[i][j] = False

    # Remove one and two-character words
    words_found = [word for word in words_found if len(word) > 2]

    # Remove duplicates, preserving order
    words_found = list(OrderedDict.fromkeys(words_found))

    # If no words were found, add a specific message
    if not words_found:
        words_found.append('No words found')
    else:
        # Sort words by length, longest first
        # Sort words by length (descending) then alphabetically
        words_found.sort(key=lambda word: (-len(word), word))


    return words_found


def solve_grid():
    # Get the grid from the entry fields.
    grid = [[entries[i][j].get().lower() for j in range(4)] for i in range(4)]

    # Solve the grid.
    solved = solve(grid, trie)

    print(len(solved))

    # Show the solution.
    messagebox.showinfo("Solution", ', '.join(solved))

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

def focus_previous_widget(event):
    event.widget.delete(0, 'end')  # Delete the content of the current widget
    event.widget.tk_focusPrev().focus()  # Move focus to the previous widget
    return("break")

mycolor = "#4B9CD3"

root = tk.Tk()
root.geometry("400x400")  # set initial size
root.configure(bg=mycolor)  # set background color to UNC blue

# Create a frame to hold the entries and make it resize with the window
frame = tk.Frame(root, bg="#4B9CD3")  # also set frame color to UNC blue
frame.grid(row=0, column=0, sticky='nsew')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create the entry fields.
entries = [[tk.Entry(frame, width=3, font=('Courier new', 24)) for _ in range(4)] for _ in range(4)]

for i in range(4):
    for j in range(4):
        entries[i][j].grid(row=i, column=j, sticky='nsew')
        frame.grid_columnconfigure(j, weight=1)
        frame.grid_rowconfigure(i, weight=1)
        entries[i][j].bind("<space>", focus_next_widget)  # Bind the function to spacebar press

# Create the solve button.
solve_button = tk.Button(root, text="Click to beat Jane (in word hunt)", command=solve_grid, font=('Courier new', 12), highlightbackground='black', highlightthickness=2)
solve_button.grid(row=1, column=0, sticky='nsew')


# Start the main loop.
root.mainloop()


