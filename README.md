# BoundedDict
A dictionary implementation whose keys are bounded rather than discrete values

# Why?

Dictionaries are great if you want to map single, discrete values, such as:

```python
from typing import Dict

map: Dict[float, str] = {
  1.0: 'blue',
  2.0: 'green',
  3.0: 'yellow'
}

for key in map:
  print(f'${key}: ${map[key]}')
```

```
1.0: blue
2.0: green
3.0: yellow
```

This is not work well for continuous streams of values, however. In the above example, if you want the value for `1.1`, you're out of luck. The solution is a Bounded Dictionary. Instead of the key being a single value, they are a *range* of values. Now, you can have code like:

```python
map = BoundedDict()
map[0.0, 1.0] = 'blue'
map[1.0, 2.0] = 'green'
map[2.0, 3.0] = 'yellow'

print(map[1.1])
print(map[2.1])
print(map[0.4])
```

and see:

```
green
yellow
blue
```

# Rules

1. Keys may **only** overlap on their bounds. Keys of [0.0, 1.0] and [1.0, 2.0] are valid, but keys of [0.0, 1.0] and [0.5, 2.0] are not.
2. If keys do *not* overlap, the bounds are considered inclusive-inclusive. If bounds *do* overlap, the value of the lesser key is returned. For instance:

```python
map = BoundedDict()
map[0.0, 1.0] = 'blue'
map[1.0, 2.0] = 'green'
map[2.0, 3.0] = 'yellow'

print(map[0.0])
print(map[1.0])
print(map[2.0])
print(map[3.0])
```

yields:

```
blue
blue
green
yellow
```

**Question**: what if one key is firmly embedded within another? Say the bounds are dates. I can have a key cover the month of December, but I want an interior section that _only_ covers the time between the 23rd and 28th (common time that people sometimes take off from work)? Should that be handled outside of the structure or would that be better tucked away in a structure within the value? Should the calling code have a bunch of `if` statements?
