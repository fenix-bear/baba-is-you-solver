from dataclasses import dataclass
from typing import Iterable

from engine import Grid, Element, Cell
import elements
from elements import Rule

INPUT_MAP = {
    "UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0), "SKIP": (0, 0)
}

class State:
    grid: Grid
    won: bool
    rules: list[Rule]

    def __init__(self):
        self.won = False
        self.grid = Grid(0, 0)
        self.rules: list[Rule] = []

    def game_input(self, input):
        for element in list(self.grid.get_all_elements()):
            for rule in self.rules:
                if isinstance(element, rule.subject.referred):
                    if isinstance(rule.object, elements.ActiveAction):
                        rule.object.execute_action(element, INPUT_MAP[input], self.rules)

        self.update_rules()

        for element in list(self.grid.get_all_elements()):
            for rule in self.rules:
                if isinstance(element, rule.subject.referred):
                    if isinstance(rule.object, elements.PassiveAction):
                        if rule.object.execute_action(element, self.rules):
                            self.won = True
                    elif isinstance(rule.object, elements.GameObjectReference):
                        for override_rule in self.rules: # X is X overrides replacement
                            if isinstance(override_rule.object, type(rule.subject)):
                                break
                        else:
                            continue
                        assert isinstance(element, Element)
                        element.cell.grid.replace(rule.subject.referred, rule.object.referred)

    def update_rules(self):
        self.rules = []
        for element in self.grid.get_all_elements():
            try:
                if isinstance(element, elements.Text):
                    for word_cells in [
                        self.grid.grid[element.cell.y][element.cell.x:], # horizontal
                        [row[element.cell.x] for row in self.grid.grid[element.cell.y:]] # vertical
                    ]:
                        rule_candidate: list[elements.WordType] = []
                        for cell in word_cells:
                            for element in cell.elements:
                                if isinstance(element, elements.Text):
                                    rule_candidate.append(element.word_type)
                                    break #TODO: check if the real game actually just only considers the first word of each cell
                            else:
                                break
                        
                        #Game object is Action
                        if (isinstance(rule_candidate[0], elements.GameObjectReference) and
                            isinstance(rule_candidate[1], elements.Is) and
                            isinstance(rule_candidate[2], elements.Action)):
                            self.rules.append(Rule(rule_candidate[0], rule_candidate[1], rule_candidate[2]))
            except Exception:
                pass # there will be errors caused by checking for rules out of bounds

        # global rule that always applies so that the main game mechanic is always accessible
        self.rules.append(Rule(elements.GameObjectReference(elements.Text), elements.Is(), elements.Push()))

    def key(self) -> tuple[bool, tuple[tuple[str, ...], ...]]:
        return (
            self.won,
            tuple(
                tuple(str(e) for e in cell.elements)
                for row in self.grid.grid
                for cell in row
            ),
        )

    # custom equals function that compares only the values of the current State instead of their instances
    # so that solve algorithms can know if they've already seen this state before
    def __eq__(self, other: "State") -> bool:
        return self.key() == other.key()
