import curses
from engine import Grid, Element
from elements import GameObject, GameObjectReference, Text, get_object_class
from elements import Is, You, Push, Win, Stop
from game import INPUT_MAP, State

KEY_TO_ACTION = {
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
    ord(" "): "SKIP",
}


def ref(name: str) -> GameObjectReference:
    return GameObjectReference(get_object_class(name))

LEVELS = [[
    [[],  [],            [],       [],       ["wall"], [],       [],            [],       [],       [],       [],       []],
    [[],  ["baba"],      ["rock"], [],       ["wall"], [],       [],            [],       [],       [],       [],       []],
    [[],  [],            [],       [],       ["wall"], [],       [ref("rock")], [Is],     [Push],   [],       [],       []],
    [[],  [],            [],       [],       [],       [],       [],            [],       [],       [],       [],       []],
    [[],  [ref("baba")], [Is],     [You],    [],       [],       [],            [],       [],       [],       ["flag"], []],
    [[],  [],            [],       [],       [],       [],       [ref("wall")], [Is],     [Stop],   [],       [],       []],
    [[],  [ref("flag")], [Is],     [Win],    [],       [],       [],            [],       [],       [],       [],       []],
    [[],  [],            [],       [],       [],       [],       [],            [],       [],       [],       [],       []],
],[
    [[],  [],            [],       [],       [],       [],       [],       [],       [],       [],            [],       [],       [],],
    [[],  [ref("baba")], [Is],     [You],    [],       [],       [],       [],       [],       [ref("flag")], [Is],     [Win],    [],],
    [[],  [],            [],       [],       [],       [],       [],       [],       [],       [],            [],       [],       [],],
    [[],  ["wall"],      ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"],      ["wall"], ["wall"], [],],
    [[],  [],            [],       [],       [],       [],       ["rock"], [],       [],       [],            [],       [],       [],],
    [[],  [],            [],       ["baba"], [],       [],       ["rock"], [],       [],       ["flag"],      [],       [],       [],],
    [[],  [],            [],       [],       [],       [],       ["rock"], [],       [],       [],            [],       [],       [],],
    [[],  ["wall"],      ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"],      ["wall"], ["wall"], [],],
    [[],  [],            [],       [],       [],       [],       [],       [],       [],       [],            [],       [],       [],],
    [[],  [ref("wall")], [Is],     [Stop],   [],       [],       [],       [],       [],       [ref("rock")], [Is],     [Push],   [],],
    [[],  [],            [],       [],       [],       [],       [],       [],       [],       [],            [],       [],       [],],
]
]


def make_element(spec: str | GameObjectReference | type) -> Element:
    if isinstance(spec, str):
        return GameObject(spec)
    if isinstance(spec, GameObjectReference):
        text = Text()
        text.word_type = spec
        return text
    text = Text()
    text.word_type = spec()
    return text


def load_level(level: int) -> Grid:
    grid = Grid(len(LEVELS[level][0]), len(LEVELS[level]))
    for y, row in enumerate(LEVELS[level]):
        for x, cell in enumerate(row):
            for spec in cell:
                grid.add(x, y, make_element(spec))
    return grid

def main(stdscr) -> None:
    for level in range(len(LEVELS)):
        curses.curs_set(0)
        grid = load_level(level)

        state = State()
        state.grid = grid
        state.rules = []
        state.update_rules()

        while True:
            stdscr.erase()
            stdscr.addstr(0, 0, state.grid.render())
            if state.won:
                stdscr.addstr("You win! Press any key to continue to next level")
            else:
                stdscr.addstr("arrows: move, space: skip, q: quit")
            key = stdscr.getch()
            if key == ord("q"):
                break
            action = KEY_TO_ACTION.get(key)
            if action is not None:
                if not state.won:
                    state.game_input(action)
                else:
                    break


if __name__ == "__main__":
    curses.wrapper(main)
