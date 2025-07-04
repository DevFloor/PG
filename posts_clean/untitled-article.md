---
ESSAY_TITLE: 
URL: https://sep.turbifycdn.com/ty/cdn/paulgraham/acl1.txt?t=1748944359&
CONTENT:
(This is the first chapter of ANSI Common Lisp, by Paul Graham.  
Copyright 1995, Prentice-Hall.)

Introduction

John McCarthy and his students began work on the first Lisp
implementation in 1958.  After Fortran, Lisp is the oldest language
still in use.  (Footnote: McCarthy, John. Recursive Functions of Symbolic Expressions and their Computation by Machine, Part I. CACM, 3:4 (April 1960), pp. 184-195. McCarthy, John. History of Lisp. In Wexelblat, Richard L. (Ed.) History of Programming Languages. Academic Press, New York, 1981, pp. 173-197. Both were available at http://www-formal.stanford.edu/jmc/ at the time of printing.) What's more remarkable is that it is still in the
forefront of programming language technology.  Programmers who know
Lisp will tell you, there is something about this language that
sets it apart.

Part of what makes Lisp distinctive is that it is designed to
evolve.  You can use Lisp to define new Lisp operators.  As new
abstractions become popular (object-oriented programming, for
example), it always turns out to be easy to implement them in Lisp.
Like DNA, such a language does not go out of style.

New Tools

Why learn Lisp? Because it lets you do things that you can't do in
other languages.  If you just wanted to write a function to return
the sum of the numbers less than n, say, it would look much the
same in Lisp and C:

 ; Lisp                   /* C */
 (defun sum (n)           int sum(int n){
   (let ((s 0))             int i, s = 0;
     (dotimes (i n s)       for(i = 0; i < n; i++)
       (incf s i))))          s += i;
                            return(s);
                          }

If you only need to do such simple things, it doesn't really matter
which language you use.  Suppose instead you want to write a function
that takes a number n, and returns a function that adds n to its
argument:

 ; Lisp 
 (defun addn (n)
   #'(lambda (x)
       (+ x n)))

What does addn look like in C?  You just can't write it.

You might be wondering, when does one ever want to do things like
this?  Programming languages teach you not to want what they cannot
provide.  You have to think in a language to write programs in it,
and it's hard to want something you can't describe.  When I first
started writing programs-- in Basic-- I didn't miss recursion,
because I didn't know there was such a thing.  I thought in Basic.
I could only conceive of iterative algorithms, so why should I miss
recursion?

If you don't miss lexical closures (which is what's being made in
the preceding example), take it on faith, for the time being, that
Lisp programmers use them all the time.  It would be hard to find
a Common Lisp program of any length that did not take advantage of
closures.  By page 112 you will be using them yourself.

And closures are only one of the abstractions we don't find in
other languages.  Another unique feature of Lisp, possibly even
more valuable, is that Lisp programs are expressed as Lisp data
structures.  This means that you can write programs that write
programs.  Do people actually want to do this?  Yes-- they're called
macros, and again, experienced programmers use them all the time.
By page 173 you will be able to write your own.

With macros, closures, and run-time typing, Lisp transcends
object-oriented programming.  If you understood the preceding
sentence, you probably should not be reading this book.  You would
have to know Lisp pretty well to see why it's true.  But it is not
just words.  It is an important point, and the proof of it is made
quite explicit, in code, in Chapter 17

Chapters 2--13 will gradually introduce all the concepts that you'll
need in order to understand the code in Chapter 17.  The reward
for your efforts will be an equivocal one: you will feel as suffocated
programming in C++ as an experienced C++ programmer would feel
programming in Basic.  It's more encouraging, perhaps, if we think
about where this feeling comes from.  Basic is suffocating to
someone used to C++ because an experienced C++ programmer knows
techniques that are impossible to express in Basic.  Likewise,
learning Lisp will teach you more than just a new language-- it
will teach you new and more powerful ways of thinking about programs.

New Techniques

As the preceding section explained, Lisp gives you tools that other
languages don't provide.  But there is more to the story than this.
Taken separately, the new things that come with Lisp-- automatic
memory management, manifest typing, closures, and so on-- each make
programming that much easier.  Taken together, they form a critical
mass that makes possible a new way of programming.

Lisp is designed to be extensible: it lets you define new operators
yourself.  This is possible because the Lisp language is made out
of the same functions and macros as your own programs.  So it's no
more difficult to extend Lisp than to write a program in it.  In
fact, it's so easy (and so useful) that extending the language is
standard practice.  As you're writing your program down toward the
language, you build the language up toward your program.  You work
bottom-up, as well as top-down.

Almost any program can benefit from having the language tailored
to suit its needs, but the more complex the program, the more
valuable bottom-up programming becomes.  A bottom-up program can
be written as a series of layers, each one acting as a sort of
programming language for the one above.  TeX was one of the earliest
programs to be written this way.  You can write programs bottom-up
in any language, but Lisp is far the most natural vehicle for this
style.

Bottom-up programming leads naturally to extensible software.  If
you take the principle of bottom-up programming all the way to the
topmost layer of your program, then that layer becomes a programming
language for the user. Because the idea of extensibility is so
deeply rooted in Lisp, it makes the ideal language for writing
extensible software.  Three of the most successful programs of the
1980s provide Lisp as an extension language: Gnu Emacs, Autocad,
and Interleaf.

Working bottom-up is also the best way to get reusable software.
The essence of writing reusable software is to separate the general
from the specific, and bottom-up programming inherently creates
such a separation.  Instead of devoting all your effort to writing
a single, monolithic application, you devote part of your effort
to building a language, and part to writing a (proportionately
smaller) application on top of it.  What's specific to this
application will be concentrated in the topmost layer.  The layers
beneath will form a language for writing applications like this
one-- and what could be more reusable than a programming language?

Lisp allows you not just to write more sophisticated programs, but
to write them faster.  Lisp programs tend to be short-- the language
gives you bigger concepts, so you don't have to use as many.  As
Frederick Brooks has pointed out, the time it takes to write a
program depends mostly on its length.  So this fact alone means
that Lisp programs take less time to write.  The effect is amplified
by Lisp's dynamic character: in Lisp the edit-compile-test cycle
is so short that programming is real-time.

Bigger abstractions and an interactive environment can change the
way organizations develop software.  The phrase "rapid prototyping"
describes a kind of programming that began with Lisp:  in Lisp,
you can often write a prototype in less time than it would take to
write the spec for one.  What's more, such a prototype can be so
abstract that it makes a better spec than one written in English.
And Lisp allows you to make a smooth transition from prototype to
production software.  When Common Lisp programs are written with
an eye to speed and compiled by modern compilers, they run as fast
as programs written in any other high-level language.

Unless you already know Lisp quite well, this introduction may seem
a collection of grand and possibly meaningless claims.  Lisp
transcends object-oriented programming? You build the language up
toward your programs? Lisp programming is real-time?  What can such
statements mean? At the moment, these claims are like empty lakes.
As you learn more of the actual features of Lisp, and see examples
of working programs, they will fill with real experience and take
on a definite shape.

A New Approach

One of the aims of this book is to explain not just the Lisp
language, but the new approach to programming that Lisp makes
possible.  This approach is one that you will see more of in the
future.  As programming environments grow in power, and languages
become more abstract, the Lisp style of programming is gradually
replacing the old plan-and-implement model.

In the old model, bugs are never supposed to happen.  Thorough
specifications, painstakingly worked out in advance, are supposed
to ensure that programs work perfectly.  Sounds good in theory.
Unfortunately, the specifications are both written and implemented
by humans.  The result, in practice, is that the plan-and-implement
method does not work very well.

As manager of the OS/360 project, Frederick Brooks was well acquainted
with the traditional approach. He was also acquainted with its
results:

  Any OS/360 user is quickly aware of how much better it should
  be...  Furthermore, the product was late, it took more memory
  than planned, the costs were several times the estimate, and it
  did not perform very well until several releases after the
  first.  (Footnote: Brooks, Frederick P. The Mythical Man-Month. Addison-Wesley, Reading (MA), 1975, p. 16. Rapid prototyping is not just a way to write programs faster or better. It is a way to write programs that otherwise might not get written at all. Even the most ambitious people shrink from big undertakings. It's easier to start something if one can convince oneself (however speciously) that it won't be too much work. That's why so many big things have begun as small things. Rapid prototyping lets us start small.)

And this is a description of one of the most successful systems of
its era.

The problem with the old model was that it ignored human limitations.
In the old model, you are betting that specifications won't contain
serious flaws, and that implementing them will be a simple matter
of translating them into code.  Experience has shown this to be a
very bad bet indeed.  It would be safer to bet that specifications
will be misguided, and that code will be full of bugs.

This is just what the new model of programming does assume.  Instead
of hoping that people won't make mistakes, it tries to make the
cost of mistakes very low.  The cost of a mistake is the time
required to correct it.  With powerful languages and good programming
environments, this cost can be greatly reduced.  Programming style
can then depend less on planning and more on exploration.

Planning is a necessary evil.  It is a response to risk:  the more
dangerous an undertaking, the more important it is to plan ahead.
Powerful tools decrease risk, and so decrease the need for planning.
The design of your program can then benefit from what is probably
the most useful source of information available: the experience of
implementing it.

Lisp style has been evolving in this direction since the 1960s.
You can write prototypes so quickly in Lisp that you can go through
several iterations of design and implementation before you would,
in the old model, have even finished writing out the specifications.
You don't have to worry so much about design flaws, because you
discover them a lot sooner.  Nor do you have to worry so much about
bugs.  When you program in a functional style, bugs can only have
a local effect.  When you use a very abstract language, some bugs
(e.g. dangling pointers) are no longer possible, and what remain
are easy to find, because your programs are so much shorter.  And
when you have an interactive environment, you can correct bugs
instantly, instead of enduring a long cycle of editing, compiling,
and testing.

Lisp style has evolved this way because it yields results.  Strange
as it sounds, less planning can mean better design.  The history
of technology is full of parallel cases.  A similar change took
place in painting during the fifteenth century.  Before oil paint
became popular, painters used a medium, called tempera, that cannot
be blended or overpainted.  The cost of mistakes was high, and this
tended to make painters conservative.  Then came oil paint, and with 
it a great change in style.  Oil "allows for second thoughts."  (Footnote: Murray, Peter and Linda. The Art of the Renaissance. Thames and Hudson, London, 1963, p. 85.)
This proved a decisive advantage in dealing with difficult subjects
like the human figure.

The new medium did not just make painters' lives easier.  It made
possible a new and more ambitious kind of painting.  Janson writes:

  Without oil, the Flemish Masters' conquest of visible reality
  would have been much more limited.  Thus, from a technical point
  of view, too, they deserve to be called the "fathers of modern
  painting," for oil has been the painter's basic medium ever 
  since.   (Footnote: Janson, W. J. History of Art, 3rd Edition. Abrams, New York, 1986, p. 374. The analogy applies, of course, only to paintings done on panels and later on canvases. Wall-paintings continued to be done in fresco. Nor do I mean to suggest that painting styles were driven by technological change; the opposite seems more nearly true.)

As a material, tempera is no less beautiful than oil.  But the
flexibility of oil paint gives greater scope to the imagination--
that was the deciding factor.

Programming is now undergoing a similar change.  The new medium is
the "object-oriented dynamic language"-- in a word, Lisp.  This is
not to say that all our software is going to be written in Lisp
within a few years.  The transition from tempera to oil did not
happen overnight; at first, oil was only popular in the leading
art centers, and was often used in combination with tempera.  We
seem to be in this phase now.  Lisp is used in universities, research
labs, and a few leading-edge companies.  Meanwhile, ideas borrowed
from Lisp increasingly turn up in the mainstream: interactive
programming environments, garbage collection, and run-time typing,
to name a few.

More powerful tools are taking the risk out of exploration.  That's
good news for programmers, because it means that we will be able
to undertake more ambitious projects.  The use of oil paint certainly
had this effect.  The period immediately following its adoption
was a golden age for painting.  There are signs already that
something similar is happening in programming.

-------------------------------------------------------------------
Available at: http://www.amazon.com/exec/obidos/ASIN/0133708756

Notes
---
