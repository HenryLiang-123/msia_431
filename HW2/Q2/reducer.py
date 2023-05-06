def reducer(shuffled_data):
    max_durations = {}
    for artist, durations in shuffled_data.items():
        max_durations[artist] = max(durations)
    return max_durations
