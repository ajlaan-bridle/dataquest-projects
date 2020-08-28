# Providing Lottery Addicts Objectivity on Winning Chances

## Introduction

While playing the lottery is a common family pastime, it has the potential to illicit escalating compulsive gambling behaviours, such as spending of savings and loans, accumulating debt, or even more desperate behaviours like theft. A fictional medical institute that works to prevent and treat gambling addictions is looking to build a mobile app to help lottery addicts better estimate their chances of winning.

The first version is intended to build functionality that allows users to answer questions like:

- What is the probability of winning the big prize with a single ticket?
- What is the probability of winning the big prize if we play 40 different tickets (or any other number)?
- What is the probability of having at least five (or four, or three, or two) winning numbers on a single ticket?

The focus of the first version will be on the [6/49 Lottery in Canada](https://en.wikipedia.org/wiki/Lotto_6/49), including [historical data](https://www.kaggle.com/datascienceai/lottery-dataset) dating from 1982 to 2018, which has been stored as [649.csv](./files/649.csv).

The Python code for all functions defined in this project is stored in [functions.py](./functions.py). Any non-standard libraries required are listed in [requirements.txt](./requirements.txt)

The file [analyse_data.py](./analyse_data.py) contains any scripting Python code that tests or uses the functions.

## Core Functions

Two core functions for this app to be able to calculate probabilities are an 'n factorial' calculation, and 'n choose k' combinations calculation. These have been coded as follows, including a couple of quick tests on each to confirm correct functionality.

```py
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
```

## Probability of Winning with a Single Ticket

The next function to add is one that prints the theoretical probability of a single ticket winning the big prize. It takes in a list of 6 distinct integer numbers and prints a statement on the probability. In reality the theoretical probability is always the same for a single ticket: it is one outcome in the number of combinations of 6 numbers sampled without replacement from a pool of 49, i.e. approximately 0.000007%.

While the initial focus is on the 6/49 Lottery, the function has been implemented to be flexible to other lottery games where `k` numbers are drawn from a pool of `n`. `n` and `k` are defaulted to the 6/49 Lottery setup.

```py
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
```

There can be some erroneous inputs to consider for this function, such as the user not providing 6 distinct numbers between 1 and 49, or mixing integers, floats or strings in the inputs. For the scope of this project it is assumed that the main app handles these scenarios, and that the interface between the app and these Python functions means that a list of 6 distinct integer numbers between 1 and 49 is always passed to this function.

## Exploring Historical Lottery Draw Data

Importing the data set:

```py
import pandas as pd

lottery = pd.read_csv('./files/649.csv', parse_dates=True)
```

Inspecting the first few rows and last few rows:

```py
print(lottery.head().to_markdown())
print(lottery.tail().to_markdown())
```

|    |   PRODUCT |   DRAW NUMBER |   SEQUENCE NUMBER | DRAW DATE   |   NUMBER DRAWN 1 |   NUMBER DRAWN 2 |   NUMBER DRAWN 3 |   NUMBER DRAWN 4 |   NUMBER DRAWN 5 |   NUMBER DRAWN 6 |   BONUS NUMBER |
|---:|----------:|--------------:|------------------:|:------------|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|---------------:|
|  0 |       649 |             1 |                 0 | 6/12/1982   |                3 |               11 |               12 |               14 |               41 |               43 |             13 |
|  1 |       649 |             2 |                 0 | 6/19/1982   |                8 |               33 |               36 |               37 |               39 |               41 |              9 |
|  2 |       649 |             3 |                 0 | 6/26/1982   |                1 |                6 |               23 |               24 |               27 |               39 |             34 |
|  3 |       649 |             4 |                 0 | 7/3/1982    |                3 |                9 |               10 |               13 |               20 |               43 |             34 |
|  4 |       649 |             5 |                 0 | 7/10/1982   |                5 |               14 |               21 |               31 |               34 |               47 |             45 |

|      |   PRODUCT |   DRAW NUMBER |   SEQUENCE NUMBER | DRAW DATE   |   NUMBER DRAWN 1 |   NUMBER DRAWN 2 |   NUMBER DRAWN 3 |   NUMBER DRAWN 4 |   NUMBER DRAWN 5 |   NUMBER DRAWN 6 |   BONUS NUMBER |
|-----:|----------:|--------------:|------------------:|:------------|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|---------------:|
| 3660 |       649 |          3587 |                 0 | 6/6/2018    |               10 |               15 |               23 |               38 |               40 |               41 |             35 |
| 3661 |       649 |          3588 |                 0 | 6/9/2018    |               19 |               25 |               31 |               36 |               46 |               47 |             26 |
| 3662 |       649 |          3589 |                 0 | 6/13/2018   |                6 |               22 |               24 |               31 |               32 |               34 |             16 |
| 3663 |       649 |          3590 |                 0 | 6/16/2018   |                2 |               15 |               21 |               31 |               38 |               49 |              8 |
| 3664 |       649 |          3591 |                 0 | 6/20/2018   |               14 |               24 |               31 |               35 |               37 |               48 |             17 |

This shows that the data set contains data for lottery draws between 12 June 1982 and 20 June 2018. For each draw 6 distinct numbers are drawn, followed by a bonus number. The functionality of the app focuses only on the 6 numbers drawn.

Using the `DataFrame.describe()` method shows that all 3665 rows contain non-null entries.

```py
print(lottery.describe().to_markdown())
```

|       |   PRODUCT |   DRAW NUMBER |   SEQUENCE NUMBER |   NUMBER DRAWN 1 |   NUMBER DRAWN 2 |   NUMBER DRAWN 3 |   NUMBER DRAWN 4 |   NUMBER DRAWN 5 |   NUMBER DRAWN 6 |   BONUS NUMBER |
|:------|----------:|--------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|---------------:|
| count |      3665 |       3665    |      3665         |       3665       |       3665       |       3665       |       3665       |       3665       |       3665       |      3665      |
| mean  |       649 |       1819.49 |         0.0308322 |          7.32769 |         14.5681  |         21.8909  |         28.9784  |         36.1626  |         43.099   |        24.5995 |
| std   |         0 |       1039.24 |         0.237984  |          5.81167 |          7.55694 |          8.17007 |          8.06972 |          7.19096 |          5.50642 |        14.36   |
| min   |       649 |          1    |         0         |          1       |          2       |          3       |          4       |         11       |         13       |         0      |
| 25%   |       649 |        917    |         0         |          3       |          9       |         16       |         23       |         31       |         40       |        12      |
| 50%   |       649 |       1833    |         0         |          6       |         14       |         22       |         30       |         37       |         45       |        25      |
| 75%   |       649 |       2749    |         0         |         10       |         20       |         28       |         35       |         42       |         47       |        37      |
| max   |       649 |       3591    |         3         |         38       |         43       |         45       |         47       |         48       |         49       |        49      |

## Functions to Compare with Historical Data

Two functions are added to compare a set of 6 numbers with the historical data. The first produces a pandas Series of sets from the columns containing the winning numbers.

This function is implemented in a generic way to combine a list of columns into a single series of sets. It is defaulted to the column naming in the historical data explored above.

```py
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
```

The second function compares a list of 6 numbers from a ticket to a pandas Series containing sets of historical winning numbers. It prints how many times that combination was a winning ticket in the past, and the probability that it would be the winning ticket in a future draw.

```py
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
```

Testing this fuction:

```py
import functions

check_historical_test = functions.check_historical_occurence([3, 11, 12, 14, 41, 43], winning_numbers)
```

```
Historically, the numbers [3, 11, 12, 14, 41, 43] have been the winning numbers 1 time. 

The probability of winning the big prize with numbers [3, 11, 12, 14, 41, 43] is 0.000007%.
```

## Probability of Winning with Multiple Tickets

This function calculates and outputs the probability of winning the big prize with a number of _different_ tickets, i.e. each ticket is a unique combination of numbers. As with other functions, it has been implemented to be agnostic to the specific lottery game, but is defaulted to calculate probabilities for the 6/49 Lottery.

```py
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
```

Testing this function:
```py
import functions

multi_ticket_test = [1, 10, 100, 10000, 1000000, 6991908, 13983816]
for test in multi_ticket_test:
    print("\n")
    functions.multi_ticket_probability(test)
```

```
The probability of winning the big prize with 1 tickets is 0.000007%.


The probability of winning the big prize with 10 tickets is 0.000072%.


The probability of winning the big prize with 100 tickets is 0.000715%.


The probability of winning the big prize with 10000 tickets is 0.071511%.


The probability of winning the big prize with 1000000 tickets is 7.151124%.


The probability of winning the big prize with 6991908 tickets is 50.000000%.


The probability of winning the big prize with 13983816 tickets is 100.000000%.
```

## Probability of Matching Fewer Than All Numbers

Lotteries typically have smaller prizes for matching some, but not all of the numbers in the draw.

This first function determines the probability of matching an exact number of numbers in a draw. The user provides the number of numbers expected to match, and the function prints the calculated probability. Once again, it is implemented to be more generic, but defaults to the 6/49 Lottery setup.

The key to this calculation is to correctly determine the number of successful possible outcomes, which for the 6/49 Lottery is:

'6 choose num' x '43 choose (6-num)'

The function genericises this calculation for a lottery game of `n` numbers in which `k` are drawn and the user is interested in the probability of matching exactly `num` numbers.

```py
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
```

Testing this function:

```py
import functions

less_all_test = [1, 2, 3, 4, 5]
for test in less_all_test:
    print("\n")
    functions.probability_less_all(test)
```

```
The probability of matching exactly 1 number in the next draw is 41.301945%


The probability of matching exactly 2 numbers in the next draw is 13.237803%


The probability of matching exactly 3 numbers in the next draw is 1.765040%


The probability of matching exactly 4 numbers in the next draw is 0.096862%


The probability of matching exactly 5 numbers in the next draw is 0.001845%
```

This final function for this project builds on the previous one to calculate the probability of matching at least a certain number of numbers in a draw. It shares the majority of its implementation content with the previous function, so there may be scope to simplify the definition of the two together, but this is not explored for the first version of this lottery app.

```py
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
```

Testing this function:

```py
import functions

less_all_test = [1, 2, 3, 4, 5]
for test in less_all_test:
    print("\n")
    functions.probability_at_least(test)
```

```
The probability of matching at least 1 number in the next draw is 56.403502%


The probability of matching at least 2 numbers in the next draw is 15.101557%


The probability of matching at least 3 numbers in the next draw is 1.863755%


The probability of matching at least 4 numbers in the next draw is 0.098714%


The probability of matching at least 5 numbers in the next draw is 0.001852%
```