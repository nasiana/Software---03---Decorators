# %% [markdown]
# # Decorators

# %% [markdown]
# ## Flying first class
# Functions are first class citizens in Python - what does that mean?

# %%
# Can assign to variable - first

# What does this function do?
def add(x, y):
    return x + y


# What does this do?
operation = add

print(add(2, 3))
print(operation(2, 3))

# %%
# Can pass as argument - second

# Write just an alias (without print)
# result_a and result_b

# kinda useless


def operate(func, x, y):
    # print("Don't blame it on the sunshine")
    return func(x, y)


result_a = operate(add, 1, 2)
result_b = add(1, 2)

# %%
# Can return function - third


def outer():
    def inner():
        print("Don't blame it on the moonlight")

    return inner


result = outer()

print(type(result))

# %%
import time


def pet_shop(pet):
    def dog_treats():
        time.sleep(5)
        return ["slippers", "bone", "stick", "mr snuggles"]

    def cat_costumes():
        time.sleep(10)
        return ["superman", "hello kitty", "albert einstein"]

    if pet == "dog":
        return dog_treats
    elif pet == "cat":
        return cat_costumes


def operate_on_items_without_knowning_type_of_shop(get_items_func):
    # if weekday:
    #    items = get_items_func()
    #    ## do some work
    None


get_shop_items = pet_shop("dog")
operate_on_items_without_knowning_type_of_shop(get_shop_items)


# %%
# Start with simple function
# Create jazz_it_up
# Wrap it with jazz_it_up


def jazz_it_up(func):
    def inner_wrapper():
        print("Don't blame it on the good times")
        func()
        print("🎵🎵 Blame it on the boogie! 🎵🎵")

    return inner_wrapper


def simple_func():
    print("💃")


# simple_func()

decorated = jazz_it_up(simple_func)

type(decorated)

decorated()


# %%
@jazz_it_up
def what_should_i_blame_it_on():
    print("...not on the good times")


what_should_i_blame_it_on()


# %%
def divide(a, b):
    return a / b


def clever_divide(func):
    def inner_wrapper(a, b):
        print("Let's divide ", a, " by ", b)
        if b == 0:
            print("Whoops! cannot divide by zero")
            return
        return func(a, b)

    return inner_wrapper


@clever_divide
def divide(a, b):
    print(a / b)


divide(22, 2)
divide(22, 0)

# %%
@jazz_it_up
def what_should_i_blame_it_on(n):
    print(f"...not on the good times x {n}")


what_should_i_blame_it_on(3)

# %% [markdown]
# ## Accept all the things - General decorators

# %%
def universal_decorator(func):
    def inner_wrapper(*args, **kwargs):
        print("I can decorate any function 🌍")
        return func(*args, **kwargs)

    return inner_wrapper


@universal_decorator
def what_should_i_blame_it_on(n):
    print(f"...not on the good times x {n}")


what_should_i_blame_it_on(3)

# %%
def borderify(func):
    def inner_wrapper(*args, **kwargs):
        print("*" * 50)
        func(*args, **kwargs)
        print("*" * 50)

    return inner_wrapper


def customizable_decorator(symbol):
    def actual_decorator(func):
        def inner_wrapper(*args, **kwargs):
            print(symbol * 50)
            func(*args, **kwargs)
            print(symbol * 50)

        return inner_wrapper

    return actual_decorator


@borderify
@customizable_decorator("=")
def display_message(message):
    print(message)


display_message("WELCOME TO THE RUMBLEEE!!")

# %% [markdown]
# ## Class decorators

# %%
class Example:
    def __init__(self) -> None:
        pass

    def __call__(self, x, y):
        print(f"Print calling instance of a class like a method with {x} and {y}")


x = Example()
x(1, 2)

# %%
class SquareDecoratorWithMemory:
    def __init__(self, simple_function):
        self.function = simple_function
        self._memory = []

    def __call__(self, *args, **kwargs):
        result = self.function(*args, **kwargs) ** 2
        self._memory.append(result)
        return result

    def memory(self):
        print("_" * 10)
        return self._memory


@SquareDecoratorWithMemory
def multiply(a, b):
    print("Your numbers are:", a, " and ", b)
    return a * b


print("Result with SquareDecoratorWithMemory is:", multiply(2, 3))
print("Result with SquareDecoratorWithMemory is:", multiply(2, 2))
print("Result with SquareDecoratorWithMemory is:", multiply(3, 3))
print("Memory:", multiply.memory())

# %% [markdown]
# ## Exercises

# %% [markdown]
# ### Exercise 1 - How long did it take?
# Create a @timer decorator.
# It will measure how long the decorated function takes to execute and print the duration to the console.

# %% [markdown]
# #### Solution

# %%
# Starter pack

import time

## Finished 'worker_function_numbers' in 0.00008740 secs


def timer(func):
    def inner_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("-" * 20)
        print(f"Finished {func.__name__!r} in {run_time:.8f} secs")
        return value

    return inner_wrapper


@timer
def worker_function_numbers(num):
    total_sum = 0
    for n in range(num):
        total_sum = total_sum + sum([(i / 2 + 5) for i in range(1000)])
    return total_sum


@timer
def worker_function_strings(word):
    print("going for a nap.. 😴")
    time.sleep(3)
    new_word = ""
    for char in word:
        new_word = new_word + "".join("ZZZ-" + char + "-ZZZ-")
    return new_word.rstrip("-")


print(worker_function_numbers(1))
print(worker_function_numbers(80))

print(worker_function_strings("CFG"))
print(worker_function_strings("supercalifragilisticexpialidocious"))

# %% [markdown]
# ### Exercise 2 - Remember, why dontcha?
# Create a @MemoizeDecorator.
# It will cache results of a function with specific parameters and would instantaneously provide an answer instead

# %% [markdown]
# #### Solution

# %%
import time


class MemoizeDecorator:
    def __init__(self, function):
        self.cache = {}
        self.function = function

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key in self.cache:
            print("I did not run a function, just fetched a result for you! :)")
            return self.cache[key]

        value = self.function(*args, **kwargs)
        self.cache[key] = value
        return value


@MemoizeDecorator
def worker_function_numbers(num):
    time.sleep(1)
    total_sum = 0
    for n in range(num):
        total_sum = total_sum + sum([(i / 2 + 5) for i in range(1000)])
    return total_sum


## run worker function many times with different arguments

for i in range(5):
    print(worker_function_numbers(i))

print(worker_function_numbers.cache)

## run again to see check a value was cached
print(worker_function_numbers(3))
