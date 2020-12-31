
# Light Coding Practice


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

from test_scripts.test_class import Test
test = Test()

test.save()



### END SOLUTION
```


```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
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
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

def alphanumeric(string):
    return string.isalnum()

test.save()



### END SOLUTION
```


```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

***Test your function with the cell below***


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

test.test_alphanumeric(alphanumeric)

test.save()



### END SOLUTION
```


✅ **Hey, you did it.  Good job.**



```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

# #2

**Find the difference between two sets.**

In the following cell, we import two sets.

- `car_owners` = A set of car owners within a community
- `church_goers` A set of people from the same community who regularly attend chuch


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

import pickle
import os

path = os.path.join('data', 'car_owners.pkl')
with open(path, 'rb') as driver_file:
    car_owners = pickle.load(driver_file)
    
path = os.path.join('data', 'church_goers.pkl')
with open(path, 'rb') as church_file:
    church_goers = pickle.load(church_file)

test.save()



### END SOLUTION
```


```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

<u>In cell below,</u> find the members of the community that do not own cars and attend church regularly.


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()


non_driving_church_goers = church_goers.difference(car_owners)

test.save()



### END SOLUTION
```


```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

***Test the results with the cell below***


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

test.run_test(non_driving_church_goers, 'set_problem')

test.save()



### END SOLUTION
```


✅ **Hey, you did it.  Good job.**



```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

# #3
**We want to identify the individual words within hashtags.**

Every hashtag will use `PascalCase` which means every word will begin with a capital letter.

<u>In the cell below,</u> define a function called `split_hashtag` that splits a given hashtag into individual words, and returns those words as a list of string.

>The function should not return any words with a '#' character. 


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

def split_hashtag(string):
    data = string.replace('#', '')
    first_letter = 0
    collected = []
    for idx in range(len(data)):
        if data[idx].isupper():
            if idx == 0:
                    continue
            else:
                collected.append(data[first_letter:idx])
                first_letter = idx
        if idx == len(data) - 1:
            collected.append(data[first_letter:])
    return collected
                

test.save()



### END SOLUTION
```


```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```

***Run the cell below to test your function!***


```python
### BEGIN SOLUTION


from test_scripts.test_class import Test
test = Test()

test.test_hashtag(split_hashtag)

test.save()



### END SOLUTION
```


✅ **Hey, you did it.  Good job.**



```python
# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS

### BEGIN HIDDEN TESTS

from test_scripts.test_class import Test
test = Test()

test.run_test()


### END HIDDEN TESTS
```
