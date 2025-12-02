import pandas as pd
import numpy as np
import pm4py.discovery


def create_footprint_matrix(event_log: list[list[str]]) -> pd.DataFrame:
    activity_set = set()
    for event in event_log:
        for activity in event:
            activity_set.add(activity)

    activity_set = sorted(activity_set)

    matrix = pd.DataFrame(columns=list(activity_set), index=list(activity_set))
    matrix = matrix.fillna(' ')

    cash = []

    # fill diagonal with "#"
    for activity in activity_set:
        matrix.loc[activity, activity] = "#"

    for event in event_log:
        current = 0
        while current < len(event)-1:
            activity_a = event[current]
            activity_b = event[current + 1]

            if matrix.loc[activity_a, activity_b] != " ":
                current = current +1
                continue

            if (activity_b, activity_a) in cash:
                matrix.loc[activity_a, activity_b] = "||"
                matrix.loc[activity_b, activity_a] = "||"
                current = current +1
                continue
            else:
                cash.append((activity_a, activity_b))
                matrix.loc[activity_a, activity_b] = "->"
                current = current +1

    # invert the "->" relationships to fill in the opposite direction with " <-"
    for activity_a in activity_set:
        for activity_b in activity_set:
            if matrix.loc[activity_a, activity_b] == "->":
                if matrix.loc[activity_b, activity_a] == " ":
                    matrix.loc[activity_b, activity_a] = "<-"

    # fill in any remaining cells with "#"
    for activity_a in activity_set:
        for activity_b in activity_set:
            if matrix.loc[activity_a, activity_b] == " ":
                matrix.loc[activity_a, activity_b] = "#"


    return matrix

def get_transitions(event_log) -> list[tuple[str, str]]:
    return pm4py.discovery.discover_footprints(event_log)

def get_places(footprint_matrix: pd.DataFrame) -> list[tuple[str, str]]:
    places = []
    activities = footprint_matrix.index.tolist()

    for i in range(len(activities)):
        for j in range(len(activities)):
            activity_a = activities[i]
            activity_b = activities[j]
            if footprint_matrix.loc[activity_a, activity_b] == "||":
                places.append((activity_a, activity_b))
    return places

# --- Sample Usage ---
if __name__ == "__main__":
    # Event Log Example (List of traces)
    # Trace 1: A -> B -> C
    # Trace 2: A -> C -> B (B and C are swapped here, suggesting concurrency)
    # Trace 3: A -> D
    events = [
        ["A", "C", "F","B"],
        ["A", "E", "G","C", "F", "D", "B"],
        ["F", "D", "C", "G", "D", "B"],
    ]

    inpath = "./running-example.xes"
    event_log = pm4py.read_xes(inpath)

    activity_key = "concept:name"
    timestamp_key = "time:timestamp"
    case_id_key = "case:concept:name"
    organization_key = "org:group"
    lifecycle_key = "lifecycle:transition"

    event_log = pm4py.convert_to_event_log(event_log, case_id_key=case_id_key,
                                              activity_key=activity_key,
                                              timestamp_key=timestamp_key)



    footprint_matrix = create_footprint_matrix(events)
    print("--- Output Matrix ---")
    print(footprint_matrix)

    transitions = get_transitions(footprint_matrix)


