import time
import re

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def parse_time(input_time):
    match = re.match(r'(\d+)(h|m|s)?', input_time)
    if match:
        time_value = int(match.group(1))
        time_unit = match.group(2)

        if time_unit == 'h':
            return time_value * 3600
        elif time_unit == 'm':
            return time_value * 60
        else:
            return time_value

    raise ValueError('Invalid time format')

def progress_bar(iterations, total, length=50):
    progress = iterations / total
    filled_length = int(length * progress)
    bar = '█' * filled_length + ' ' * (length - filled_length)
    remaining_time = format_time(total - iterations)

    print(f'Progress: |{bar}| {remaining_time} left', end='\r')

# Ask the user for the time to wait
input_time = input("Enter the time to wait (e.g., 5m, 2h, 30s): ")

# Parse the input time into seconds
total_seconds = parse_time(input_time)

# Perform the countdown
for i in range(total_seconds, 0, -1):
    # Perform a task
    time.sleep(1)
    progress_bar(total_seconds - i + 1, total_seconds, length=30)

print('\nTime\'s up')
