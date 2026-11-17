import random

GIFTERS = ["Marie-France", "Michel", "Phil", "Camille", "Pat", "Amanda", "Mel", "Louis"]

FORBIDDEN_PAIRINGS = list(map(sorted, [
    ("Marie-France", "Michel"),
    ("Phil", "Camille"),
    ("Mel", "Louis"),
    ("Pat", "Amanda"),
]))

def is_invalid(pair: tuple[str, str] | list[str, str]):
    return (len(set(pair)) == 1) or (sorted(pair) in FORBIDDEN_PAIRINGS)

def get_candidate(recipients):
    candidate = random.choice(recipients)
    recipients.remove(candidate)

    return candidate

def reset():
    recipients = GIFTERS.copy()
    pairs = []

    return recipients, pairs

def get_assignments():
    recipients, pairs = reset()
    for gifter in GIFTERS:

        filtered_recipients = recipients.copy()

        for recipient in recipients:
            pair = (gifter, recipient)
            if is_invalid(pair):
                filtered_recipients.remove(recipient)

        if len(filtered_recipients) == 0:
            return False, []

        if len(filtered_recipients) == 1 and is_invalid([gifter, filtered_recipients[0]]):
            return False, []

        # guaranteed valid pairing
        candidate = get_candidate(filtered_recipients)
        recipients.remove(candidate)

        pairs.append([gifter, candidate])

    return True, pairs


def pick():
    success, pairs = get_assignments()

    while not success:
        success, pairs = get_assignments()

    return pairs
