from datetime import datetime, timedelta

def time_calculator():
    try:
        # Get the first time
        time_str1 = input("Enter the first time (format: HH:MM[:SS][AM/PM] or HH:MM[:SS][am/pm]): ")
        time_str1 = time_str1.replace(" ", "")
        time_format1 = "%I:%M:%S%p" if len(time_str1) > 5 else "%I:%M%p"
        time1 = datetime.strptime(time_str1, time_format1)

        # Get the second time
        time_str2 = input("Enter the second time (format: HH:MM[:SS][AM/PM] or HH:MM[:SS][am/pm]): ")
        time_str2 = time_str2.replace(" ", "")
        time_format2 = "%I:%M:%S%p" if len(time_str2) > 5 else "%I:%M%p"
        time2 = datetime.strptime(time_str2, time_format2)

        # Calculate the time difference
        time_difference = abs(time2 - time1)

        # Print the result
        print("Time difference:", time_difference)

    except ValueError:
        print("Invalid time format. Please use the format: HH:MM[:SS][AM/PM] or HH:MM[:SS][am/pm]")

# Run the time calculator
time_calculator()
