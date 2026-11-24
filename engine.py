from __future__ import annotations
from collections.abc import Iterator

class Element:
    cell: Cell

class Cell:
    elements: list[Element]
    x: int
    y: int
    grid: Grid
    def __init__(self: Cell, grid: Grid, x: int, y: int):
        self.grid = grid
        self.x = x
        self.y = y
        self.elements: list[Element] = []

    def add(self, element: Element):
        element.cell = self
        self.elements.append(element)

    def remove(self, element: Element):
        self.elements = [e for e in self.elements if e is not element]

    def render(self):
        # just render what's on top for now
        return str(self.elements[-1]) if self.elements else ""

    def get_elements(self) -> Iterator[Element]:
        for element in self.elements:
            yield element

class Grid:
    grid: list[list[Cell]]
    cells: list[Cell]
    width: int
    height: int
    elements: list[Element]

    def __init__(self: Grid, width: int, height: int):
        self.grid = [[Cell(self, i, j) for i in range(width)] for j in range(height)]
        self.cells = [c for row in self.grid for c in row]
        self.width, self.height = width, height

    def get(self, x: int, y: int) -> Cell | None:
        if 0 > x or x >= self.width or 0 > y or y >= self.height:
            return
        return self.grid[y][x]

    def get_all_elements(self) -> Iterator[Element]:
        for cell in self.cells:
            for element in cell.get_elements():
                yield element

    def add(self, x: int, y: int, element: Element):
        cell = self.get(x, y)
        cell.add(element)

    def replace(self, replacee: type, replacer: type):
        """Replace all elements of a certain type with elements of another type"""
        for element in self.find(replacee):
            element = replacer(element)

    def find(self, element: type) -> list[Element]:
        results: list[Element] = list(filter(lambda x: isinstance(x, element), self.elements))
        return results

    def move(self, element: Element, direction: tuple[int, int]) -> bool:
        """Move an element along the grid"""
        x = element.cell.x + direction[0]
        y = element.cell.y + direction[1]
        if 0 > x or x >= self.width or 0 > y or y >= self.height:
            return False
        element.cell.remove(element)
        target = self.get(x, y)
        target.add(element)
        return True

    def render(self) -> str:
        width: int = 5

        def wrap(text: str) -> list[str]:
            lines: list[str] = []
            for word in text.split():
                if lines and len(lines[-1]) + 1 + len(word) <= width:
                    lines[-1] += " " + word
                elif len(word) <= width:
                    lines.append(word)
                else:
                    for i in range(0, len(word), width):
                        lines.append(word[i:i + width])
            return lines or [""]

        lines: list[str] = ["+" + "+".join("-" * width for _ in self.grid[0]) + "+"]
        for row in self.grid:
            cell_lines: list[list[str]] = [wrap(cell.render()) for cell in row]
            body: int = max(len(cl) for cl in cell_lines)
            for i in range(body):
                lines.append("|" + "|".join((cl[i] if i < len(cl) else "").ljust(width) for cl in cell_lines) + "|")
            lines.append("+" + "+".join("-" * width for _ in row) + "+")
        return "\n".join(lines)
                