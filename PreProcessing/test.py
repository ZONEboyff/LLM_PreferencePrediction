from collections import deque


class state:
    def __init__(self, jug1, jug2):
        self.jug1 = jug1
        self.jug2 = jug2

    def __str__(self):
        return "({}, {})".format(self.jug1, self.jug2)

    def __eq__(self, other):
        return self.jug1 == other.jug1 and self.jug2 == other.jug2

    def __hash__(self):
        return hash((self.jug1, self.jug2))

    def fill_jug1(self, capacity1):
        return state(capacity1, self.jug2)

    def fill_jug2(self, capacity2):
        return state(self.jug1, capacity2)

    def empty_jug1(self):
        return state(0, self.jug2)

    def empty_jug2(self):
        return state(self.jug1, 0)

    def pour_jug1_to_jug2(self, capacity2):
        pour_amount = min(self.jug1, capacity2 - self.jug2)
        return state(self.jug1 - pour_amount, self.jug2 + pour_amount)

    def pour_jug2_to_jug1(self, capacity1):
        pour_amount = min(self.jug2, capacity1 - self.jug1)
        return state(self.jug1 + pour_amount, self.jug2 - pour_amount)


def water_jug(capacity1, capacity2, target):
    start = state(0, 0)
    if start.jug2 == target or start.jug1 == target:
        return [start]
    visited = set()
    stack = [start]
    visited.add(start)
    paths = []
    parent = {start: None}
    while stack:
        current = stack.pop()
        for next_state in [current.fill_jug1(capacity1), current
                .fill_jug2(capacity2), current.empty_jug1(), current.empty_jug2(), current.pour_jug1_to_jug2(capacity2),
                           current.pour_jug2_to_jug1(capacity1)]:
            if next_state in visited:
                continue
            stack.append(next_state)
            visited.add(next_state)
            parent[next_state] = current
            if next_state.jug2 == target or next_state.jug1 == target:
                path = []
                while next_state:
                    path.append(next_state)
                    next_state = parent[next_state]
                paths.append(path[::-1])

    return paths


def main():
    capacity1 = int(input("Enter capacity 1: "))
    capacity2 = int(input("Enter capacity 2: "))
    target = int(input("Enter target: "))
    result = water_jug(capacity1, capacity2, target)
    if len(result) > 0:
        print("All Possible Solution Paths:")
        for path in result:
            for state in path:
                if state == path[len(path) - 1]:
                    print(state)
                    continue
                print(state, end=" -> ")
            print()
    else:
        print("No Solution exists!")


if __name__ == "__main__":
    main()