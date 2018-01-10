## SquirrelTailPro

### What it is
SquirrelTailPro is a logfile viewer that runs on the Mac.  It is written in Python3 with QT5.

### Why it exists
There are two main reason why SquirrelTailPro exists:

1. I was fed up with using BareTailPro via Wine on the Mac as cut & paste did not work correctly and it occasionally crashed.
2. I wanted to learn python and having completed the basic 'Hello Word' training needed something that was a bit more of a challenge.  

### Download/Installation
Extract SquirrelTailPro and run 'python3 squirreltailpro.py'

There is also a bash srcript to start SquirrelTailPro in the background.  This script requires the source files are placed in a 'SquirrelTailProApp' directory.

SquirrelTailPro requires Python v3 and PyQt5 (QT5).
To install PyQt5 use the pip installer built into python: i.e pip3 install PyQt5 

### How to use it
The app is fairly self explanatory and works in a similar way to BareTailPro on Windows.
In the toolbar there is a 'Colour Picker' icon for configuring which keywords to highlight and what colour to highlight them with.  There is also a 'Search Keywords' icon for configuring the list search words shown in the search drop-down box. 
 
### Does it work on windows, linux etc.
As SquirrelTailPro is written in Python3 and Qt5 it should run on any system able to run Python and QT5.  However, there are some issues with font sizes, layout and with drop-n-drop that would need to be addressed first (maybe a future update)
