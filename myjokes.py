import random

jokes = [
  "A lawyer dies and goes to Heaven. 'There must be some mistake,' the lawyer argues. 'I'm too young to die. I'm only 55.' 'Fifty-five?' says Saint Peter. 'No, according to out calculations, you're 82.' 'How'd you get that?' the lawyer asks. Answers St. Peter, 'We added up your time sheets.'",
  "What's the difference between a good lawyer and a bad lawyer?\nA bad lawyer can let a case drag out for several years. A good lawyer can make it last even longer.",
  "One day in Contract Law class, the professor asked one of his better students, 'Now if you were to give someone an orange, how would you go about it?'\nThe student replied, 'Here's an orange.'\nThe professor was livid. 'No! No! Think like a lawyer!'\nThe student then recited, 'Okay, I'd tell him, 'I hereby give and convey to you all and singular, my estate and interests, rights, claim, title, claim and advantages of and in, said orange, together with all its rind, juice, pulp, and seeds, and all rights and advantages with full power to bite, cut, freeze and otherwise eat, the same, or give the same away with and without the pulp, juice, rind and seeds, anything herein before or hereinafter or in any deed, or deeds, instruments of whatever nature or kind whatsoever to the contrary in anywise notwithstanding...'",
  "As the lawyer awoke from surgery, he asked, 'Why are all the blinds drawn?' The nurse answered, 'There's a fire across the street, and we didn't want you to think you had died.'",
  "A woman and her little girl were visiting the grave of the little girl's grandmother. On their way through the cemetery back to the car, the little girl asked, 'Mummy, do they ever bury two people in the same grave?'\n'Of course not, dear,' replied the mother, 'Why would you think that?'\n'The tombstone back there said... 'Here lies a lawyer and an honest man.''",
  "Santa Claus, the tooth fairy, an honest lawyer and an old drunk are walking down the street together when they simultaneously spot a hundred dollar bill. Who gets it? The old drunk, of course, the other three are fantasy creatures.",
  "At a convention of biological scientists, one researcher remarks to another, 'Did you know that in our lab we have switched from mice to lawyers for our experiments?' 'Really?' the other replied, 'Why did you switch?' 'Well, for three reasons. First we found that lawyers are far more plentiful, second, the lab assistants don't get so attached to them, and thirdly there are some things even a rat won't do.'",
  "What does a lawyer get when you give him Viagra?\nTaller.",
  "The lawyer's son wanted to follow in his father's footsteps, so he went to law school and graduated with honors. Then he went home to join his father's firm.\nAt the end of his first day at work, he rushed into his father's office and said, 'Father, father! In one day I broke the Smith case that you've been working on for so long!'\nHis father yelled, 'You idiot! We've been living on the funding of that case for ten years!'",
  "How many lawyer jokes are in existence?\n\nOnly three. All the rest are true stories.",
  "What's the difference between a Scotsman and a Rolling Stone? A Rolling Stone says, \"hey you, get off of my cloud!\" while a Scotsman says, \"Hey McLeod, get off of my ewe!\""
]

rare_jokes = [
  "Did you know that black people are just regular people with night mode on?",
  "Did you know that dolphis use puffer fish to get high and commit r***? Well can you guess what a land dolphin is?",
  "Why do jews have big noses? Because air is free!"
]

last_three_jokes = []


def tell_joke():
  available_jokes = [joke for joke in jokes if joke not in last_three_jokes]
  if len(available_jokes) == 0:
    available_jokes = jokes
  if random.randint(1, 50) == 1 and len(rare_jokes) > 0:
    joke = random.choice(rare_jokes)
  else:
    joke = random.choice(available_jokes)
  last_three_jokes.append(joke)
  if len(last_three_jokes) > 3:
    last_three_jokes.pop(0)
  return joke
