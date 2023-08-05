
What is Bridge?
===============

Bridge is a light-weight portable library for natural language processing and because of its tiny size it can be easily ported to any programming languages. As of now Bridge provides a Python Library in 50 SLOC and a JavaScript one in 78 SLOC.

How Bridge Works?
=================

Unlike other natural language processing approaches that investigate grammatical features of a language, Bridge aims the structred meaning. Bridge knows the meaningful parts of a text and instead of grammatically examining it to extract meaning, it literally understands the sentence.

A Sample Program with Bridge
============================

It's better to show the power of Bridge with an example, thus let's build a simple calculator with Bridge!

First we should construct a Bridge Object:

  Bridge = bridge();

Now, Let us add our Meaning Models to Bridge. First of all, we'll teach it what is a number. We'll use a grammar object to teach Bridge a new concept. Each grammar has one or more "type" or "role", for example our number have role "number". Also, we need some definitions to create a grammar. Each definition or model, should have a single "type" and a regex pattern to test atoms passed to it. Each grammar has a "value" that Bridge uses to create the resulting atom. Finally each grammar has a "weight" that shows the importance of the grammar.

When first Bridge examines a sentence, it breaks the sentence to atoms. Each atom shows a meaningful part of speech in Bridge, At the first examination Bridge gives all of the atoms a "word" type.

We'll teach the number model as follows::

    Bridge.add_grammar(
      grammar(
        ['number'],          # grammar type
        [definition(         # definitions
          'word',            # type of atom to accept
          r'^\d+$')],        # regex to match atoms against
        '{0}',               # grammar value
        0));                 # weight

Now let's teach it the basic mathematical operators::

    Bridge.add_grammar(grammar(['plus'], [definition('word', r'^\+$')], '{0}', 0)) # plus
    Bridge.add_grammar(grammar(['minus'], [definition('word', r'^-$')], '{0}', 0)) # minus

Now we'll teach mathematical operations and use the models we've already defined::

    Bridge.add_grammar(
      grammar(['plus-command', 'number'],
                  [definition('number', r'.*'),
                   definition('plus', r'.*'),
                   definition('number', r'.*')],
                  '(+ {0} {2})', 1));

    Bridge.add_grammar(
      grammar(['minus-command', 'number'],
                  [definition('number', r'.*'),
                   definition('minus', r'.*'),
                   definition('number', r'.*')],
                  '(- {2} {0})', 1));

Now Bridge can do simple mathematical operations, for now it can take this::

    1 - 2 + 3 - 4 + 5

And convert it to the following lisp code::

    (+ (- 4 (+ (- 2 1) 3)) 5)

(you may run this lisp using hy) It's time to teach Bridge some natural language::

    Bridge.add_grammar(
      grammar
        (['and'],
         [definition('word', r'^and$')],
        '{0}', 0));

    Bridge.add_grammar(
      grammar(
        ['numeral-and', 'number'],
        [definition('number', r'.*'),
         definition('and', r'.*'),
         definition('number', r'.*')],
        '{0} {2}', 2));

    Bridge.add_grammar(
      grammar
        (['sum-command'],
         [definition('word', r'^sum$')],
        '{0}', 0));

    Bridge.add_grammar(
      grammar(
        ['complete-function'],
        [definition('sum-command', r'.*'),
         definition('numeral-and', r'.*')],
        '(+ {1})', 3))

Using the following code::

    sentence = "sum 3 + 4 and 5 and 6 - 7 and 4"
    print(Bridge.process(sentence)[0].value))

We'll get::

    (+ (+ 3 4) 5 (- 7 6) 4)
