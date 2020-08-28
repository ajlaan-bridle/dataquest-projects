'''
Core functions for app
'''
import pandas as pd

def factorial(n: int) -> int:
    factorial = 1
    for i in range(n, 0, -1):
        factorial *= i
    return int(factorial)

assert factorial(5) == 120
assert factorial(10) == 3628800

def combinations(n: int, k: int) -> int:
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n-k)
    return int(numerator / denominator)

assert combinations(5, 2) == 10
assert combinations(10, 4) == 210

def one_ticket_probability(numbers: list, n: int=49, k: int=6):
    '''
    Prints the probability of a given set of lottery numbers winning the big prize.

    numbers = lottery ticket numbers
    n = total pool of numbers in the game, default 49
    k = number of numbers drawn in the game, default 6
    '''
    probability =  1 / combinations(n, k)
    output = f"The probability of winning the big prize with numbers {numbers} is {probability:%}."
    print(output)

def extract_numbers(lottery_results: pd.DataFrame,
    number_cols: list = [
        'NUMBER DRAWN 1',
        'NUMBER DRAWN 2',
        'NUMBER DRAWN 3',
        'NUMBER DRAWN 4',
        'NUMBER DRAWN 5',
        'NUMBER DRAWN 6'
        ]) -> pd.Series:
    '''
    Convert historical lottery numbers from separate columns into a set.
    Returns a pandas Series of sets.
    '''
    return lottery_results[number_cols].apply(lambda row: set(row), axis=1)

def check_historical_occurence(numbers: list, historical_data: pd.Series):
    '''
    Prints how many times a set of numbers has occurred in historical
    winning numbers and the probability of that number being a winning
    combination.
    '''
    occurrences = (historical_data == set(numbers)).sum()
    if occurrences == 1:
        output = f"Historically, the numbers {numbers} have been the winning numbers {occurrences} time."
    else:
        output = f"Historically, the numbers {numbers} have been the winning numbers {occurrences} times."
    print(output,"\n")
    one_ticket_probability(numbers)

def multi_ticket_probability(no_of_tickets: int, n: int=49, k: int=6):
    '''
    Prints the probability of winning the big prize from a number of tickets

    no_of_tickets = number of tickets bought with distinct lottery numbers
    n = total pool of numbers in the game, default 49
    k = number of numbers drawn in the game, default 6
    '''
    probability = no_of_tickets / combinations(n, k)
    output = f"The probability of winning the big prize with {no_of_tickets} tickets is {probability:%}."
    print(output)

def probability_less_all(num: int, n: int=49, k: int=6):
    '''
    Prints the probability of matching a specified number of numbers on a ticket,
    where num is less than k.

    num = how many numbers expected to match winning draw
    n = total pool of numbers in the game, default 49
    k = number of numbers drawn in the game, default 6
    '''
    matches = combinations(k, num)
    draws_per_match = combinations(n-k, k-num)
    successful_outcomes = matches * draws_per_match
    total_outcomes = combinations(n, k)
    probability = successful_outcomes / total_outcomes
    if num == 1:
        output = f"The probability of matching exactly {num} number in the next draw is {probability:%}"
    else:
        output = f"The probability of matching exactly {num} numbers in the next draw is {probability:%}"
    print(output)

def probability_at_least(num: int, n: int=49, k: int=6):
    '''
    Prints the probability of matching at least a specified number of numbers on a ticket,
    where num is less than k.

    num = how many numbers at minimum expected to match winning draw
    n = total pool of numbers in the game, default 49
    k = number of numbers drawn in the game, default 6
    '''
    successful_outcomes = 0
    for i in range(num, k+1, 1):
        matches = combinations(k, i)
        draws_per_match = combinations(n-k, k-i)
        successful_outcomes += matches * draws_per_match
    total_outcomes = combinations(n, k)
    probability = successful_outcomes / total_outcomes
    if num == 1:
        output = f"The probability of matching at least {num} number in the next draw is {probability:%}"
    else:
        output = f"The probability of matching at least {num} numbers in the next draw is {probability:%}"
    print(output)
