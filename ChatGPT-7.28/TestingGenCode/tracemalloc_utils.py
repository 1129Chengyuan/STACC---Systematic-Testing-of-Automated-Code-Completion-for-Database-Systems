import tracemalloc

tracemalloc.start()


def clear_traces():
    tracemalloc.clear_traces()


def get_traced_memory():
    return tracemalloc.get_traced_memory()[1]
