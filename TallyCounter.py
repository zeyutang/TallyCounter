import os
from datetime import datetime, timedelta

# Specific timeframe
WEEKS = 0
DAYS = 0
HOURS = 3
MINUTES = 0
SECONDS = 0


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_timedelta(td):
    if td is not None:
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    else:
        hours, minutes, seconds = '-', '-', '-'

    return f"{hours}h {minutes}m {seconds}s ago"


def show_instructions():
    print('=' * 45)
    print("Tally Counter Controls:")
    print("  j: Increase counter")
    print("  k: Decrease counter (default Y/n)")
    print("  r: Reset counter (default y/N)")
    print("  q: Exit")


def update_counts(counter, timeframe):
    now = datetime.now()
    counter = {k: v for k, v in counter.items() if now - k <= timeframe}
    if len(counter) == 0:
        elapsed = None
    else:
        earliest_in_session = min(counter.keys())
        elapsed = now - earliest_in_session
    return counter, elapsed


def main():
    counter = {}
    timeframe = timedelta(weeks=WEEKS,
                          days=DAYS,
                          hours=HOURS,
                          minutes=MINUTES,
                          seconds=SECONDS)
    show_instructions()

    while True:
        # Update counts and calculate elapsed time
        counter, elapsed = update_counts(counter, timeframe)

        # Show counter status
        clear_screen()
        print(f"Counter status (in last {HOURS}h): {sum(counter.values())}")
        print(f"Earliest in current session: {format_timedelta(elapsed)}")
        show_instructions()

        # Process user input
        key = input("Enter command: ").lower()
        now = datetime.now()
        if key == 'j':
            counter[now] = counter.get(now, 0) + 1
        elif key == 'k':
            confirm = input("Decrease counter? [Y/n]: ").lower()
            if confirm == '' or confirm == 'y':
                counter[now] = counter.get(now, 0) - 1
            # If need to restart the counter.
            if sum(counter.values()) <= 0:
                counter = {}
        elif key == 'r':
            confirm = input("Reset counter? [y/N]: ").lower()
            if confirm == 'y':
                counter = {}
        elif key == 'q':
            break
        else:
            pass


if __name__ == "__main__":
    main()
