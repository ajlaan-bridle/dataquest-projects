'''
Historical data analysis and function testing
'''
import functions
import pandas as pd

lottery = pd.read_csv('./files/649.csv', parse_dates=True)

print(lottery.head().to_markdown())
print(lottery.tail().to_markdown())
print(lottery.describe().to_markdown())

winning_numbers = functions.extract_numbers(lottery)

check_historical_test = functions.check_historical_occurence([3, 11, 12, 14, 41, 43], winning_numbers)

multi_ticket_test = [1, 10, 100, 10000, 1000000, 6991908, 13983816]
for test in multi_ticket_test:
    print("\n")
    functions.multi_ticket_probability(test)

less_all_test = [1, 2, 3, 4, 5]
for test in less_all_test:
    print("\n")
    functions.probability_less_all(test)

for test in less_all_test:
    print("\n")
    functions.probability_at_least(test)