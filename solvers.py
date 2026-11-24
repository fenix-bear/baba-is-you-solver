from collections.abc import Iterator

from game import State


def search(state: State, depth_first: bool) -> Iterator[str]:
    start_key = state.key()

    # the set of all states we've seen before
    visited = {start_key}

    # the list of states to still explore
    queue = [] # frontier

    # the list of states we went down to get to the current state
    path = [start_key]

    actions: list[str] = [] # the list of actions we took to get to the current state
    node = state # node always represents the current state of the game

    route = [] # list of actions to send to the game next if any
    while True:

        # the below lines in `if route:` will loop until we have reached our desired destination
        # the purpose of having this loop is because this search function has to send all of its
        # backtracking to the live game so that it can be visualized and to make the code simpler
        if route:
            action = route.pop(0)
            node = yield action # execute the next step of the route

            # keep the history in sync with the live game state
            if action == "UNDO":
                path.pop()
                actions.pop()
            else:
                path.append(node.key())
                actions.append(action)

            continue

        dirs = ["UP", "DOWN", "LEFT", "RIGHT"]
        for action in dirs: # try every direction to discover new nodes/states
            node = yield action
            k = node.key()
            if k not in visited: # do not go to a node we've already been to
                visited.add(k)

                # add the node to the queue and how to get there
                queue.append((path + [k], actions + [action]))
            node = yield "UNDO"

        if not queue:
            return # no possible route, this is currently uncaught in main() but all levels are beatable for now so that's fine
        
        # get the next node from depending on if this is bfs or dfs
        next_node = queue.pop(-1 if depth_first else 0)
        target_path = next_node[0]
        target_actions = next_node[1]

        # figure out how far we have to backtrack to get to the target node if at all
        common = 0
        while common < len(path) and common < len(target_path) and path[common] == target_path[common]:
            common += 1
        pivot = max(common - 1, 0)

        # undo back to the pivot, then replay the target's remaining actions
        route = (["UNDO"] * (len(path) - 1 - pivot)) + target_actions[pivot:]


def bfs(state: State) -> Iterator[str]:
    return search(state, False)


def dfs(state: State) -> Iterator[str]:
    return search(state, True)
