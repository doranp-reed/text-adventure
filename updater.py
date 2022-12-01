updates = []


def update_all():
    for u in updates:
        u.update()


def register(thing: object):
    updates.append(thing)


def deregister(thing: object):
    updates.remove(thing)
