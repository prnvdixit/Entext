"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
"""


# For porting to Python3, just un-document the import statements and then
# "find and replace" manually.


"""
regex - sudo -H pip install regex  - https://pypi.python.org/pypi/regex
tkinter - sudo apt-get install python-tk  - http://www.tkdocs.com/tutorial/install.html
python2.7 - sudo apt-get install python2.7 - https://www.python.org/downloads/ (Download python 2.7.*)
requests - sudo -H pip install requests - https://pypi.python.org/pypi/requests/
"""

from Tkinter import *
from ScrolledText import ScrolledText
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from tkColorChooser import askcolor
from tkFont import Font, families

import os
import webbrowser
import string
import re
import regex
import requests


#These are Basic File functions - New, Open, Save.

def new() :
    os.system("python " + current_dir + "/" + os.path.basename(__file__))

def open_file() :
    try :
        file = tkFileDialog.askopenfile()
        delete_all()
        text.insert(INSERT, file.read())
    except :
        pass

def save() :
    path = tkFileDialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    content = text.get(1.0, END)
    path.write(content.strip())


# These are basic tools for general formatting - Bold, Italic, Underline.
# These modifies the formatting of 'selected text'.

def bold() :
    s = text.selection_get()
    length = len(s)
    try :
        string = text.tag_names("sel.first")

        if "bold" in string :
            text.tag_remove("bold", "sel.first", "%s + %sc" % ("sel.first", length))

        else :
            text.tag_add("bold", "sel.first", "%s + %sc" % ("sel.first", length))
            bold_font = Font(text, text.cget("font"))
            bold_font.configure(weight = "bold")
            text.tag_configure("bold", font = bold_font)

    except :
        pass

    
def italic() :
    s = text.selection_get()
    length = len(s)

    try :
        string = text.tag_names("sel.first")

        if "italic" in string :
            text.tag_remove("italic", "sel.first", "%s + %sc" % ("sel.first", length))

        else :
            text.tag_add("italic", "sel.first", "%s + %sc" % ("sel.first", length))
            italic_font = Font(text, text.cget("font"))
            italic_font.configure(slant = "italic")
            text.tag_configure("italic", font = italic_font)

    except :
        pass

    
def underline() :
    s = text.selection_get()
    length = len(s)

    try :
        string = text.tag_names("sel.first")

        if "underline" in string :
            text.tag_remove("underline", "sel.first", "%s + %sc" % ("sel.first", length))

        else :
            text.tag_add("underline", "sel.first", "%s + %sc" % ("sel.first", length))
            underline_font = Font(text, text.cget("font"))
            underline_font.configure(underline = 1)
            text.tag_configure("underline", font = underline_font)

    except :
        pass

# Rename the file: - First select the original file from the dialog box, then provide the name of the new file. 

def rename() :
    directory = current_dir
    opts = {}
    opts['title'] = "Select File to be replaced"
    orgfilename = tkFileDialog.Open(**opts).show()
    newfilename = tkSimpleDialog.askstring("Replace", "New File name?")
    os.rename(orgfilename, directory + "/" + newfilename)

    
# Ask for confirmation before closing the file.    

def close() :
    ans = tkMessageBox.askquestion(title = "Save File", message = "Would you like to save this file?")
    if ans == "Yes" :
        save()
    master.quit()

    
"""
Clip board functions - Cut, Copy, Paste.
Helper Functions - Select-all, Delete-all, Delete-Selected.
"""

def cut() :
    master.clipboard_clear()
    text.clipboard_append(string = text.selection_get())
    text.delete(SEL_FIRST, SEL_LAST)

def copy() :
    master.clipboard_clear()
    text.clipboard_append(string = text.selection_get())

def paste() :
    text.insert(INSERT, master.clipboard_get())

def delete() :
    text.delete(index=SEL_FIRST, index2=SEL_LAST)

def select_all() :
    text.tag_add(SEL, 1.0, END)

def delete_all() :
    text.delete(1.0, END)


# Edit functions - Find, Find & Replace.

def find() :
    start = 1.0
    string = tkSimpleDialog.askstring("Find", "Enter String")

    length = len(string)
    pos = text.search(string, start, stopindex=END)

    """
    'pos' is of the form - line_number.column_number
    So, splitting is necessary so as to find the starting and ending indexes of a word.
    length = Window-size (length of string - we need to search) in which we are required to move.
    """

    while pos :

        text.tag_configure("search", foreground = "green")
        text.tag_add("search", pos, "%s + %sc" % (pos, length))

        row, col = pos.split('.')
        col = int(col) + length
        end = row + '.' + str(col)
        start = end

        pos = text.search(string, start, stopindex=END)

        
def find_replace() :
    start = 1.0
    string = tkSimpleDialog.askstring("Find & Replace", "Enter string")
    replace_with = tkSimpleDialog.askstring("Find & Replace", "Replace With")

    length = len(string)
    pos = text.search(string, start, stopindex=END)

    while pos :

        text.tag_add("search", pos, "%s + %sc" % (pos, length))

        text.delete(pos, "%s + %sc" % (pos, length))
        text.insert(pos, replace_with)

        row, col = pos.split('.')
        col = int(col) + length
        end = row + '.' + str(col)
        start = end

        pos = text.search(string, start, stopindex=END)


#To reduce the verbosity, these functions are introduced to reduce the repetitive work.

def add_menu(name, function_call) :
    menu.add_cascade(label = name, menu = function_call)

def add_drop(menu, name, function_call) :
    menu.add_command(label = name, command = function_call)

def add_command_menu(name, function_call) :
    menu.add_command(label = name, command = function_call)

    
"""
The functions responsible for re-directing to the required links to find out the Synonyms and Dictionary-meanings respectively.
Tried to do these same things by exporting a dictionary, but that made the editor slow, so dropped that idea.
"""

def syn() :
    string = text.selection_get()
    webbrowser.open("http://www.thesaurus.com/browse/" + string)

def dict_() :
    string = text.selection_get()
    webbrowser.open("http://www.dictionary.com/browse/" + string + "?s=t")


#Spell-checking all document.

def spell_check_all() :

    """
    First, the text is improved so that extra spaces in between words and at the start of lines can be removed.
    Then since 'escape-characters' like new-line couldn't be accommodated as a single character themselves,
    all new-line chars are replaced by some rarely used char (This was done so as to update the 'pos' variable
    whenever a newline is encountered - Refer definition of 'pos' variable in 'find' function).
    Next, the words are searched in the dictionary maintained (by exporting inbuilt dictionary from
    "Linux - /usr/share/dict") and are appropriately marked or are left unmarked.
    """

    improve_text()
    
    # Convert whole text into lowercase characters too, as to remove any discrepancy between word in dictionary and
    # that used in the text.

    string = text.get(1.0, END)
    string = string.strip().replace('\n', ' ~ ')
    string = string.lower()
    
    # Split the string into words - which are going to be looked up in the dictionary.

    start = 1.0
    string = string.split()
    l = len(string)
    p = 0

    for i in xrange(l) :
        
        # For the first word, start variable is already initialised, so no need to repeat it.
        # If '~' is encountered, that means we have to move to a new line.
        # Finally, get the word from the relevant indices calculated.
        
        if i :
            start = str(start)[:2] + str(p)
        if string[i] == '~' :
            start = str(int(start[:1]) + 1) + ".0"
            p = 0
            continue
        end = str(start)[:2] + str(p + len(string[i]))
        word = text.get(start, end)
        word = word.lower()

        """
        Regex module was used to remove extra punctuation and other unnecessary symbols
        (which affected the look-up in the dictionary).
        """

        word = regex.sub(ur"\p{P}+", "", word)
        p += len(string[i]) + 1
        
        # If the word is in _dict, the spelling is correct.
        # Else, change the foreground of the word to red color.

        try :
            if (_dict[word]) :
                pass
        except :
            text.tag_configure("spell", foreground = "red")
            text.configure(state = "normal")
            text.tag_add("spell", start , end)


# GNU-Aspell project was used to predict the relevant string prediction nearest to the selected word.

def spell_suggest() :
    string = text.selection_get()
    webbrowser.open("http://suggest.aspell.net/index.php?word=" + string + "&spelling=american&dict=normal&sugmode=slow")

    
# General Document statistics, which sometimes is to be adhered to.

def docu_stats() :
    string = text.get(1.0, END)
    string = string.strip()
    words = "Total words : " + str(len(string.split()))
    chars = "Total Chars : " + str(len(string))
    lines = "Total Lines : " + str(string.count("\n") + 1)
    toplevel = Toplevel()
    label1 = Label(toplevel, text = words, height = 0, width = 20)
    label1.pack()
    label2 = Label(toplevel, text = chars, height = 0, width = 20)
    label2.pack()
    label3 = Label(toplevel, text = lines, height = 0, width = 20)
    label3.pack()

    
# The Help-text - To tell what this text editor is all about.
  
def help_text() :
    string1 = "A Tkinter based text editor implemented to increase the productiveness in content writing work I had been generally involved in."
    string2 = " Along with basic file functions, features like Spell-check, Synonym checker, Meaning look up, formatting options were added."
    toplevel = Toplevel()
    label1 = Label(toplevel, text = string1, height = 0, width = 75, wraplength = 500)
    label1.pack()
    label2 = Label(toplevel, text = string2, height = 0, width = 75, wraplength = 500)
    label2.pack()

    
# Link to my Github and Linkedin pages.
    
def git(event) :
    webbrowser.open("https://github.com/prnvdixit")

def linkedin(event) :
    webbrowser.open("https://in.linkedin.com/in/prnvdixit")

    
# The About-text - To tell about me.
    
def about() :
    toplevel = Toplevel()
    string1 = "Developed By :- Pranav Dixit, Undergrad at IIT (ISM), Dhanbad"
    string2 = "GitHub"
    string3 = "LinkedIn"
    label1 = Label(toplevel, text = string1, height = 0, width = 50, wraplength = 500)
    label1.pack()
    label2 = Label(toplevel, text = string2, height = 0, width = 50, wraplength = 500, fg = "blue", cursor = "hand2")
    label2.pack()
    label2.bind("<Button-1>", git)
    label3 = Label(toplevel, text = string3, height = 0, width = 50, wraplength = 500, fg = "blue", cursor = "hand2")
    label3.pack()
    label3.bind("<Button-1>", linkedin)

    
#Improving the text so that extra (more than one) spaces in between words and at the start of lines can be removed.

def improve_text() :
    
    # Cut the whole text - Improve it - Paste the improved text.
    
    string = text.get(1.0, END)
    delete_all()
    
    # Removing extra spaces in between the words.
    
    string = re.sub(' +',' ',string)
    lines = string.strip().split("\n")
    l = len(lines)
    
    # Removing spaces at the start of the lines.
    
    for i in xrange(l):
        lines[i] = lines[i].strip()
        
    string = "\n".join(lines)
    text.insert(1.0, string)
    

"""
The best match is found using requests module. For the first (i.e. best) match, the entire text of the page is stored in
variable 'res'. Then since for every recommended word on the page, a link to "Merriam-webster" is provided, we search for the
link, and return the first index wherever it was found. Next, the appropriate length of 'res' is sliced. 
Lastly, the word is extracted from the 'res' string.
"""

def best_match() :
    word = text.selection_get()
    res = requests.get('http://suggest.aspell.net/index.php?word='+ word +'&spelling=american&dict=normal&sugmode=slow')
    
    # Check for any error. If there is, report it.
    
    try :
        res.raise_for_status()
    except Exception as exc:
        print "There was a problem : %s" % (exc)

    t = res.text
    string = 'href="http://www.merriam-webster.com/dictionary/'
    l = len(string)
    r = t.find(string)
    q = t[r+l : r+l+100]

    for i in xrange(100) :
        if q[i] == '"' :
            break

    print q[: i]

    
# Creating a dictionary (The python dictionary - hashed one) out of the inbuilt one.
    
words = open("/usr/share/dict/american-english")
words = [word.strip() for word in words]
words = [word.lower() for word in words]
global _dict
_dict = {}

for word in words :
    _dict[word] = 1

    
# Remove all single characters except 'a' and 'i'.
    
for c in string.ascii_lowercase :
    del _dict[c]

_dict['a'] = 1
_dict['i'] = 1


master = Tk()
master.title("Editor")
master.geometry("840x480+300+400")


global current_dir
current_dir = os.path.dirname(os.path.abspath(__file__))
# cd /home/pranav/Desktop/

# Icon of the Editor window
image = PhotoImage(file='entext.gif')
master.tk.call('wm', 'iconphoto', master._w, image)


# To enable wrapping of text in the horizontal direction, as well as scrolling in the vertical direction.
text = ScrolledText(master, width = 400, height = 380, wrap = 'word', font = ("Verdana", 10), highlightthickness = 0, bd = 2, undo = True, pady = 2, padx = 3)

text.pack(fill = Y, expand = 1)
text.focus_set()

menu = Menu(master)
master.config(menu = menu)

# Creating Menus to work with.

file_menu = Menu(menu)
edit_menu = Menu(menu)
clip_util = Menu(menu)
format_menu = Menu(menu)
help_menu = Menu(menu)
spell_menu = Menu(menu)


# Normal-menus are those which yield a drop-down menu when clicked.
# Command-menus are those menus which are run directly on clicked.

menu_name = ["File", "Edit", "Clip Board", "Formatting", "Help", "Spell suggest"]
command_menu_name = ["Synonym", "Meaning", "Spell-Check", "Document Statistics", "Improve Text"]

menu_list = [file_menu, edit_menu, clip_util, format_menu, help_menu, spell_menu]
command_menu = [syn, dict_, spell_check_all, docu_stats, improve_text]


# Drop-down menu list corresponding to every menu_name.

drop_list = [[("New", new), ("Open", open_file), (0,), ("Close", close), ("Save", save), ("Rename", rename)], \
        [("Undo", text.edit_undo), ("Redo", text.edit_redo), (0,), ("Find", find), ("Find & Replace", find_replace)], \
        [("Cut", cut), ("Copy", copy), ("Paste", paste), (0,), ("Select All", select_all)], \
        [("Bold", bold), ("Italic", italic), ("Underline", underline)], \
        [("Help", help_text), ("About", about)], \
        [("Get best match", best_match), ("Get all matches", spell_suggest)]]

l = len(menu_list)
n = len(command_menu)

for i in xrange(l) :
    add_menu(menu_name[i], menu_list[i])

for i in xrange(n) :
    add_command_menu(command_menu_name[i], command_menu[i])

for i in xrange(l) :

    m = len(drop_list[i])

    for j in xrange(m) :

        if drop_list[i][j][0] == 0 :
            menu_list[i].add_separator()
            continue

        add_drop(menu_list[i], drop_list[i][j][0], drop_list[i][j][1])

master.mainloop()
