#myjokes.py
#holds joke arrays and joke return function
from jokeapi import Jokes


async def tell_joke():
  j = await Jokes()  # Initialize the class
  joke = await j.get_joke()  # Retrieve a random joke

  if joke["type"] == "single":
    return joke["joke"]
  else:
    return joke["setup"] + "\n" + joke["delivery"]