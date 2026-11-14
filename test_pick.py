from pick import pick, FORBIDDEN_PAIRINGS

runs = 10

def test_no_self_gifting():
    for run in range(runs):

        pairs = pick()

        for pair in pairs:
            if pair[0] == pair[1]:
                raise
        print(f"run #{run} was a success")

    print(f"{runs} runs of test_no_self_gifting ran successfully")

def test_no_partner_gifting():
    for run in range(runs):

        pairs = pick()

        assert not any(pair in FORBIDDEN_PAIRINGS for pair in pairs), "partner gifting !!!"
        print(f"run #{run} was a success")

    print(f"{runs} runs of test_no_partner_gifting ran successfully")

def test_one_recipient_per_gifter():
    for run in range(runs):
        pairs = pick()

        seen_gifters = []
        seen_recipients = []

        for pair in pairs:
            seen_gifters.append(pair[0])
            seen_recipients.append(pair[1])

        if len(seen_gifters) != len(set(seen_gifters)):
            raise

        if len(seen_recipients) != len(set(seen_recipients)):
            raise

        print(f"run #{run} was a success")

    print(f"{runs} runs of test_one_recipient_per_gifter ran successfully")

test_no_self_gifting()
test_no_partner_gifting()
test_one_recipient_per_gifter()
