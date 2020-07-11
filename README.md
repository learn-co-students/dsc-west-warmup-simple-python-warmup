# Light Coding Practice


```python
from test_scripts.test_class import Test
test = Test()
```

# #1

**Validate a string.**

Please define a function called `alphanumeric` that validates if a user input string is alphanumeric. 

The function receives a string, and outputs either `True` or `False`. 

The given string is not nil/null/NULL/None, so you don't have to check that.

<u>The string has the following conditions to be alphanumeric:</u>

- Allowed characters are uppercase / lowercase latin letters and digits from 0 to 9
- No whitespaces / underscore


```python
def alphanumeric(string):
    pass
```

***Test your function with the cell below***


```python
test.test_alphanumeric(alphanumeric)
```

# #2

**Find the difference between two sets.**

In the following cell, we import two sets.

- `car_owners` = A set of car owners within a community
- `church_goers` A set of people from the same community who regularly attend chuch


```python
import pickle

path = os.path.join('data', 'car_owners.pkl')
with open(path, 'rb') as driver_file:
    car_owners = pickle.load(driver_file)
    
path = os.path.join('data', 'church_goers.pkl')
with open(path, 'rb') as church_file:
    church_goers = pickle.load(church_file)
```

<u>In cell below,</u> find the members of the community that do not own cars and attend church regularly.


```python
# Your code here

```

***Test the results with the cell below***


```python
test.run_test(non_driving_church_goers, 'set_problem')
```

# #3
**We want to identify the individual words within hashtags.**

Every hashtag will use `PascalCase` which means every word will begin with a capital letter.

<u>In the cell below,</u> define a function called `split_hashtag` that splits a given hashtag into individual words, and returns those words as a list of string.

>The function should not return any words with a '#' character. 


```python
# Your code here
def split_hashtag(string):
    pass
```

***Run the cell below to test your function!***


```python
test.test_hashtag(split_hashtag)
```
