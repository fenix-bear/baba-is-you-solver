# baba-is-you-solver
Algorithmic Solver for Baba is You

I plan for this to be a reimplementation of the 2019 videogame *Baba is You* in Python, with a program that can algorithmically solve some of its levels.

Currently, I have a simple clone of it working that you can interact with via a curses TUI by running main.py.
It puts you in a winnable demo level that shows the 4 implemented actions of this game: You, Win, Push, and Stop.

Game object replacement (like Rock Is Wall, for example) and all other actions and other word types are currently not implemented.

I have also implemented two classic solving algorithms, BFS and DFS, which you can run and visualize from the TUI.
These algorithms work on the two levels that are currently in this project, the demo level and the recreation of level 00 from the actual game,
because they can both be trivially solved by moving directly to the Win Flag. These algorithms will likely not be sufficient for later levels I will
add that actually have puzzle elements to them.