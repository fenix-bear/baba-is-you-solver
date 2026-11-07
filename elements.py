from __future__ import annotations

from dataclasses import dataclass

from engine import Element


@dataclass
class Rule:
    subject: GameObjectReference
    verb: Verb
    object: GameObjectReference | Action



class WordType:
    def __str__(self):
        return self.__class__.__name__

class GameObjectReference(WordType): 
    referred: type
    def __init__(self, referred: type):
        self.referred = referred

    def __str__(self):
        return "Ref: " + self.referred.__name__

class Verb(WordType): ...
class Is(Verb): ...

class Action(WordType): ...

# movement-like actions that occur first
class ActiveAction(Action):
    
    @staticmethod
    def execute_action(element: Element, delta: tuple[int, int], rules: list[Rule]):
        return

    @staticmethod
    def move(element: Element, delta: tuple[int, int], rules: list[Rule], skip: list[Element] = []) -> bool:
        if delta == (0, 0):
            return True
        moved: list[Element] = []
        neighbor = element.cell.grid.get(element.cell.x + delta[0], element.cell.y + delta[1])
        if neighbor is None:
            return False
        for element_to_move in filter(lambda x: x not in skip, neighbor.get_elements()):
            for rule in rules:
                if (isinstance(element_to_move, rule.subject.referred) and isinstance(rule.object, ActiveAction) 
                and not isinstance(rule.object, You) # this is kind of a hack and should probably be done more elegantly within the You class
                ):
                    if not rule.object.move(element_to_move, delta, rules, skip + moved):
                        for moved_element in moved: # backtrack
                            moved_element.cell.grid.move(moved_element, (0 - delta[0], 0 - delta[1]))
                        break
                    else:
                        moved.append(element_to_move)
            else:
                continue
            break
        else:
            return element.cell.grid.move(element, delta)
        return False
        

# effects that occur second
class PassiveAction(Action):
    @staticmethod
    def execute_action(element: Element) -> bool:
        return False

class You(ActiveAction):
    @staticmethod
    def execute_action(element: Element, delta: tuple[int, int], rules: list[Rule]):
        ActiveAction.move(element, delta, rules)

class Push(ActiveAction): ...
class Stop(ActiveAction):
    @staticmethod
    def move(element: Element, delta: tuple[int, int], rules: list[Rule], skip: list[Element] = []):
        if delta == (0, 0):
            return True
        return False


class Win(PassiveAction):
    @staticmethod
    def execute_action(element: Element, rules: list[Rule]) -> bool:
        for rule in rules:
            if isinstance(rule.object, You):
                if rule.subject.referred in [type(el) for el in element.cell.get_elements()]:
                    return True
        return False




class Prefix(WordType): ...
class Suffix(WordType): ...
class Negation(WordType): ...
class Conjunction(WordType): ...


class Text(Element):
    word_type: WordType

    def __str__(self):
        return str(self.word_type)

class GameObject(Element):
    object_name: str

    def __str__(self):
        return self.__class__.__name__

    def __init__(self, object_name: str):
        self.object_name = object_name

        # it's truly messed up that python lets me do this
        self.__class__ = get_object_class(object_name)

object_classes: dict[str, type] = {}

def get_object_class(name: str) -> type:
    if name not in object_classes:
        object_classes[name] = type(name, (GameObject, ), {})
    return object_classes[name]
