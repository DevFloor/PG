Title: 

URL Source: https://sep.turbifycdn.com/ty/cdn/paulgraham/acl2.txt?t=1748944359&

Markdown Content:
(This is Chapter 2 of ANSI Common Lisp, by Paul Graham.  
Copyright 1995, Prentice-Hall.)

Welcome to Lisp

This chapter aims to get you programming as soon as possible.
By the end of it you will know enough Common Lisp to begin writing
programs.

2.1 Form

It is particularly true of Lisp that you learn it by using it,
because Lisp is an interactive language.  Any Lisp system will
include an interactive front-end called the toplevel.  You type
Lisp expressions into the toplevel, and the system displays their
values.

Lisp usually displays a prompt to tell you that it's waiting for
you to type something.  Many implementations of Common Lisp use >
as the toplevel prompt.  That's what we'll use here.

One of the simplest kinds of Lisp expression is an integer.  If we
enter 1 after the prompt,

> 1
1
> 

the system will print its value, followed by another prompt, to
say that it's ready for more.

In this case, the value displayed is the same as what we typed.
A number like 1 is said to evaluate to itself.  Life gets more
interesting when we enter expressions that take some work to
evaluate.  For example, if we want to add two numbers together, we
type something like:

> (+ 2 3)
5

In the expression (+ 2 3), the + is called the operator, and the
numbers 2 and 3 are called the arguments.

In everyday life, we would write this expression as 2 + 3, but in
Lisp we put the + operator first, followed by the arguments, with
the whole expression enclosed in a pair of parentheses: (+ 2 3).
This is called prefix notation, because the operator comes first.
It may at first seem a strange way to write expressions, but in
fact this notation is one of the best things about Lisp.

For example, if we want to add three numbers together, in ordinary
notation we have to use + twice,

2 + 3 + 4

while in Lisp we just add another argument:

(+ 2 3 4)

The way we ordinarily use +, it must have exactly two arguments:
one on the left and one on the right.  The flexibility of prefix
notation means that, in Lisp, + can take any number of arguments,
including none:

> (+)
0
> (+ 2)
2
> (+ 2 3)
5
> (+ 2 3 4)
9
> (+ 2 3 4 5)
14

Because operators can take varying numbers of arguments, we need
parentheses to show where an expression begins and ends.

Expressions can be nested.  That is, the arguments in an expression
may themselves be complex expressions:

> (/ (- 7 1) (- 4 2))
3

In English, this is seven minus one, divided by four minus two.

Another beauty of Lisp notation is: this is all there is.  All Lisp
expressions are either atoms, like 1, or lists, which consist of
zero or more expressions enclosed in parentheses.  These are valid
Lisp expressions:

        2   (+ 2 3)   (+ 2 3 4)   (/ (- 7 1) (- 4 2))

As we will see, all Lisp code takes this form.  A language like C
has a more complicated syntax:  arithmetic expressions use infix
notation; function calls use a sort of prefix notation, with the
arguments delimited by commas; expressions are delimited by
semicolons; and blocks of code are delimited by curly brackets.
In Lisp, we use a single notation to express all these ideas.

2.2 Evaluation

In the previous section, we typed expressions into the toplevel,
and Lisp displayed their values.  In this section we take a closer
look at how expressions are evaluated.

In Lisp, + is a function, and an expression like (+ 2 3) is a
function call.  When Lisp evaluates a function call, it does so in
two steps:

  1. First the arguments are evaluated, from left to right.  In
     this case, each argument evaluates to itself, so the values
     of the arguments are 2 and 3, respectively.

  2. The values of the arguments are passed to the function named
     by the operator.  In this case, it is the + function, which
     returns 5.

If any of the arguments are themselves function calls, they are
evaluated according to the same rules.  So when (/ (- 7 1) (- 4 2)) 
is evaluated, this is what happens:

  1. Lisp evaluates (- 7 1): 7 evaluates to 7 and 1 evaluates to 1.
     These values are passed to the function -, which returns 6.

  2. Lisp evaluates (- 4 2): 4 evaluates to 4 and 2 evaluates to 2.
     These values are passed to the function -, which returns 2.

  3. The values 6 and 2 are sent to the function /, which returns 3.

Not all the operators in Common Lisp are functions, but most are.
And function calls are always evaluated this way.  The arguments
are evaluated left-to-right, and their values are passed to the
function, which returns the value of the expression as a whole.
This is called the evaluation rule for Common Lisp.

One operator that doesn't follow the Common Lisp evaluation rule
is quote.  The quote operator is a special operator, meaning that
it has a distinct evaluation rule of its own.  And the rule is: do
nothing.  The quote operator takes a single argument, and just
returns it verbatim:

> (quote (+ 3 5))
(+ 3 5)

For convenience, Common Lisp defines ' as an abbreviation for quote.
You can get the effect of calling quote by affixing a ' to the
front of any expression:

> '(+ 3 5)
(+ 3 5)

It is much more common to use the abbreviation than to write out
the whole quote expression.

Lisp provides the quote as a way of protecting expressions from
evaluation.  The next section will explain how such protection can
be useful.

---------------------------------------------------------------------
Getting Out of Trouble

If you type something that Lisp can't understand, it will display
an error message and put you into a version of the toplevel called
a break loop.  The break loop gives experienced programmers a chance
to figure out what caused an error, but initially the only thing
you will want to do in a break loop is get out of it.  What you
have to type to get back to the toplevel depends on your implementation
of Common Lisp.  In this hypothetical implementation, :abort does
it:

> (/ 1 0)
Error: Division by zero.
       Options: :abort, :backtrace
>> :abort
>

Appendix A shows how to debug Lisp programs, and gives examples of
some of the most common errors.
---------------------------------------------------------------------

2.3 Data

Lisp offers all the data types we find in most other languages,
along with several others that we don't.  One data type we have
used already is the integer, which is written as a series of digits:
256.  Another data type Lisp has in common with most other languages
is the string, which is represented as a series of characters
surrounded by double-quotes: "ora et labora".  Integers and strings
both evaluate to themselves.

Two Lisp data types that we don't commonly find in other languages
are symbols and lists.  Symbols are words.  Ordinarily they are
converted to uppercase, regardless of how you type them:

> 'Artichoke
ARTICHOKE

Symbols do not (usually) evaluate to themselves, so if you want to
refer to a symbol, you should quote it, as above.

Lists are represented as zero or more elements enclosed in parentheses.
The elements can be of any type, including lists.  You have to
quote lists, or Lisp would take them for function calls:

> '(my 3 "Sons")
(MY 3 "Sons")
> '(the list (a b c) has 3 elements)
(THE LIST (A B C) HAS 3 ELEMENTS)

Notice that one quote protects a whole expression, including
expressions within it.

You can build lists by calling list.  Since list is a function,
its arguments are evaluated.  Here we see a call to + within a call
to list:

> (list 'my (+ 2 1) "Sons")
(MY 3 "Sons")

We are now in a position to appreciate one of the most remarkable
features of Lisp.  Lisp programs are expressed as lists.  If the
arguments of flexibility and elegance did not convince you that
Lisp notation is a valuable tool, this point should.  It means that
Lisp programs can generate Lisp code.  Lisp programmers can (and
often do) write programs to write their programs for them.

Such programs are not considered till Chapter 10, but it is important
even at this stage to understand the relation between expressions
and lists, if only to avoid being confused by it.  This is why we
need the quote.  If a list is quoted, evaluation returns the list
itself; if it is not quoted, the list is treated as code, and
evaluation returns its value:

> (list '(+ 2 1) (+ 2 1))
((+ 2 1) 3)

Here the first argument is quoted, and so yields a list.  The second
argument is not quoted, and is treated as a function call, yielding
a number.

In Common Lisp, there are two ways of representing the empty list.
You can represent it as a pair of parentheses with nothing between
them, or you can use the symbol nil.  It doesn't matter which way
you write the empty list, but it will be displayed as nil:

> ()
NIL
> nil
NIL

You don't have to quote nil (though it wouldn't hurt) because nil
evaluates to itself.

2.4 List Operations

The function cons builds lists.  If its second argument is a list,
it returns a new list with the first argument added to the front:

> (cons 'a '(b c d))
(A B C D)

We can build up lists by consing new elements onto an empty list.
The list function that we saw in the previous section is just a
more convenient way of consing several things onto nil:

> (cons 'a (cons 'b nil))
(A B)
> (list 'a 'b)
(A B)

The primitive functions for extracting the elements of lists are
car and cdr. [1] The car of a list is the first element, and the
cdr is everything after the first element:

> (car '(a b c))
A
> (cdr '(a b c))
(B C)

You can use combinations of car and cdr to reach any element of a
list.  If you want to get the third element, you could say:

> (car (cdr (cdr '(a b c d))))
C

However, you can do the same thing more easily by calling third:

> (third '(a b c d))
C

2.5 Truth

In Common Lisp, the symbol t is the default representation for
truth.  Like nil, t evaluates to itself.  The function listp returns
true if its argument is a list:

> (listp '(a b c))
T

A function whose return value is intended to be interpreted as
truth or falsity is called a predicate.  Common Lisp predicates
often have names that end with p.

Falsity in Common Lisp is represented by nil, the empty list.  If
we give listp an argument that isn't a list, it returns nil:

> (listp 27)
NIL

Because nil plays two roles in Common Lisp, the function null,
which returns true of the empty list,

> (null nil)
T

and the function not, which returns true if its argument is false,

> (not nil)
T

do exactly the same thing.

The simplest conditional in Common Lisp is if.  It usually takes
three arguments: a test expression, a then expression, and an else
expression.  The test expression is evaluated.  If it returns true,
the then expression is evaluated and its value is returned.  If
the test expression returns false, the else expression is evaluated
and its value is returned:

> (if (listp '(a b c))
      (+ 1 2)
      (+ 5 6))
3
> (if (listp 27)
      (+ 1 2)
      (+ 5 6))
11

Like quote, if is a special operator.  It could not possibly be
implemented as a function, because the arguments in a function call
are always evaluated, and the whole point of if is that only one
of the last two arguments is evaluated.

The last argument to if is optional.  If you omit it, it defaults
to nil:

> (if (listp 27) 
      (+ 2 3))
NIL

Although t is the default representation for truth, everything
except nil also counts as true in a logical context:

> (if 27 1 2)
1

The logical operators and and or resemble conditionals.  Both take
any number of arguments, but only evaluate as many as they need to
in order to decide what to return.  If all its arguments are true
(that is, not nil), then and returns the value of the last one:

> (and t (+ 1 2))
3

But if one of the arguments turns out to be false, none of the
arguments after that get evaluated.  Similarly for or, which stops
as soon as it finds an argument that is true.
    
These two operators are macros.  Like special operators, macros
can circumvent the usual evaluation rule.  Chapter 10 explains how
to write macros of your own.
 

2.6 Functions

You can define new functions with defun.  It usually takes three
or more arguments: a name, a list of parameters, and one or more
expressions that will make up the body of the function.  Here is
how we might define third:

> (defun our-third (x)
    (car (cdr (cdr x))))
OUR-THIRD

The first argument says that the name of this function will be
our-third.  The second argument, the list (x), says that the function
will take exactly one argument: x.  A symbol used as a placeholder
in this way is called a variable.  When the variable represents an
argument to a function, as x does, it is also called a parameter.

The rest of the definition, (car (cdr (cdr x))), is known as the
body of the function.  It tells Lisp what it has to do to calculate
the return value of the function.  So a call to our-third returns
(car (cdr (cdr x))), for whatever x we give as the argument:

> (our-third '(a b c d))
C

Now that we've seen variables, it's easier to understand what
symbols are.  They are variable names, existing as objects in their
own right.  And that's why symbols, like lists, have to be quoted.
A list has to be quoted because otherwise it will be treated as
code; a symbol has to be quoted because otherwise it will be treated
as a variable.

You can think of a function definition as a generalized version of
a Lisp expression.  The following expression tests whether the sum
of 1 and 4 is greater than 3:

> (> (+ 1 4) 3)
T

By replacing these particular numbers with variables, we can write
a function that will test whether the sum of any two numbers is
greater than a third:

> (defun sum-greater (x y z)
    (> (+ x y) z))
SUM-GREATER
> (sum-greater 1 4 3)
T

Lisp makes no distinction between a program, a procedure, and a
function.  Functions do for everything (and indeed, make up most
of the language itself).  If you want to consider one of your
functions as the main function, you can, but you will ordinarily
be able to call any function from the toplevel.  Among other things,
this means that you will be able to test your programs piece by
piece as you write them.

2.7 Recursion

The functions we defined in the previous section called other
functions to do some of their work for them.  For example, sum-greater
called + and >.  A function can call any function, including itself.

A function that calls itself is recursive.  The Common Lisp function
member tests whether something is an element of a list.  Here is
a simplified version defined as a recursive function:

(defun our-member (obj lst)
  (if (null lst)
      nil
      (if (eql (car lst) obj)
          lst
          (our-member obj (cdr lst)))))

The predicate eql tests whether its two arguments are identical;
aside from that, everything in this definition is something we have
seen before.  Here it is in action:

> (our-member 'b '(a b c))
(B C)
> (our-member 'z '(a b c))
NIL

The definition of our-member corresponds to the following English
description.  To test whether an object obj is a member of a list
lst, we

  1. First check whether lst is empty.  If it is, then obj is
     clearly not a member of it, and we're done.

  2. Otherwise, if obj is the first element of lst, it is a member.

  3. Otherwise obj is only a member of lst if it is a member of
     the rest of lst.

When you want to understand how a recursive function works, it can
help to translate it into a description of this kind.

Many people find recursion difficult to understand at first.  A
lot of the difficulty comes from using a mistaken metaphor for
functions.  There is a tendency to think of a function as a sort
of machine.  Raw materials arrive as parameters; some of the work
is farmed out to other functions; finally the finished product is
assembled and shipped out as the return value.  If we use this
metaphor for functions, recursion becomes a paradox.  How can a
machine farm out work to itself?  It is already busy.

A better metaphor for a function would be to think of it as a
process one goes through.  Recursion is natural in a process.  We
often see recursive processes in everyday life.  For example,
suppose a historian was interested in population changes in European
history.  The process of examining a document might be as follows:

  1. Get a copy of the document.
  
  2. Look for information relating to population changes.

  3. If the document mentions any other documents that might be
     useful, examine them.

This process is easy enough to understand, yet it is recursive,
because the third step could entail one or more applications of
the same process.

So don't think of our-member as a machine that tests whether
something is in a list.  Think of it instead as the rules for
determining whether something is in a list.  If we think of functions
in this light, the paradox of recursion disappears. [2]

2.8 Reading Lisp

The pseudo-member defined in the preceding section ends with five
parentheses.  More elaborate function definitions might end with
seven or eight.  People who are just learning Lisp find the sight
of so many parentheses discouraging.  How is one to read, let alone
write, such code? How is one to see which parenthesis matches which?

The answer is, one doesn't have to.  Lisp programmers read and
write code by indentation, not by parentheses.  When they're writing
code, they let the text editor show which parenthesis matches which.
Any good editor, particularly if it comes with a Lisp system, should
be able to do paren-matching.  In such an editor, when you type a
parenthesis, the editor indicates the matching one.  If your editor
doesn't match parentheses, stop now and figure out how to make it,
because it is virtually impossible to write Lisp code without it.

[In vi, you can turn on paren-matching with :set sm.  In Emacs,
M-x lisp-mode is a good way to get it.]

With a good editor, matching parentheses ceases to be an issue when
you're writing code.  And because there are universal conventions
for Lisp indentation, it's not an issue when you're reading code
either.  Because everyone uses the same conventions, you can read
code by the indentation, and ignore the parentheses.

Any Lisp hacker, however experienced, would find it difficult to
read the definition of our-member if it looked like this:

(defun our-member (obj lst) (if (null lst) nil (if 
(eql (car lst) obj) lst (our-member obj (cdr lst)))))

But when the code is properly indented, one has no trouble.  You
could omit most of the parentheses and still read it:

defun our-member (obj lst)
  if null lst
     nil
     if eql (car lst) obj
        lst
        our-member obj (cdr lst)

Indeed, this is a practical approach when you're writing code on
paper.  Later, when you type it in, you can take advantage of
paren-matching in the editor.

2.9 Input and Output

So far we have done i/o implicitly, by taking advantage of the
toplevel.  For real interactive programs this is not likely to be
enough.  In this section we look at a few functions for input and
output.

The most general output function in Common Lisp is format.  It
takes two or more arguments: the first indicates where the output
is to be printed, the second is a string template, and the remaining
arguments are usually objects whose printed representations are to
be inserted into the template.  Here is a typical example:

> (format t "~A plus ~A equals ~A.~%" 2 3 (+ 2 3))
2 plus 3 equals 5.
NIL

Notice that two things get displayed here.  The first line is
displayed by format.  The second line is the value returned by the
call to format, displayed in the usual way by the toplevel.
Ordinarily a function like format is not called directly from the
toplevel, but used within programs, so the return value is never
seen.

The first argument to format, t, indicates that the output is to
be sent to the default place.  Ordinarily this will be the toplevel.
The second argument is a string that serves as a template for
output.  Within this string, each ~A indicates a position to be
filled, and the ~% indicates a newline.  The positions are filled
by the values of the remaining arguments, in order.

The standard function for input is read.  When given no arguments,
it reads from the default place, which will usually be the toplevel.
Here is a function that prompts the user for input, and returns
whatever is entered:

(defun askem (string)
  (format t "~A" string)
  (read))

It behaves as follows:

> (askem "How old are you? ")
How old are you? 29
29

Bear in mind that read will sit waiting indefinitely until you type
something and (usually) hit return.  So it's unwise to call read
without printing an explicit prompt, or your program may give the
impression that it is stuck, while in fact it's just waiting for
input.

The second thing to know about read is that it is very powerful:
read is a complete Lisp parser.  It doesn't just read characters
and return them as a string.  It parses what it reads, and returns
the Lisp object that results.  In the case above, it returned a
number.

Short as it is, the definition of askem shows something we haven't
seen before in a function.  Its body contains more than one
expression.  The body of a function can have any number of expressions.
When the function is called, they will be evaluated in order, and
the function will return the value of the last one.

In all the sections before this, we kept to what is called "pure"
Lisp---that is, Lisp without side-effects.  A side-effect is some
change to the state of the world that happens as a consequence of
evaluating an expression.  When we evaluate a pure Lisp expression
like (+ 1 2), there are no side-effects; it just returns a value.
But when we call format, as well as returning a value, it prints
something.  That's one kind of side-effect.

When we are writing code without side-effects, there is no point
in defining functions with bodies of more than one expression.
The value of the last expression is returned as the value of the
function, but the values of any preceding expressions are thrown
away.  If such expressions didn't have side-effects, you would have
no way of telling whether Lisp bothered to evaluate them at all.

2.10 Variables

One of the most frequently used operators in Common Lisp is let,
which allows you to introduce new local variables:

> (let ((x 1) (y 2))
    (+ x y))
3

A let expression has two parts.  First comes a list of instructions
for creating variables, each of the form (variable expression).
Each variable will initially be set to the value of the corresponding
expression.  So in the example above, we create two new variables,
x and y, which are initially set to 1 and 2, respectively.  These
variables are valid within the body of the let.

After the list of variables and values comes a body of expressions,
which are evaluated in order.  In this case there is only one, a
call to +.  The value of the last expression is returned as the
value of the let.  Here is an example of a more selective version
of askem written using let:

(defun ask-number ()
  (format t "Please enter a number. ")
  (let ((val (read)))
    (if (numberp val)
        val
        (ask-number))))

This function creates a variable val to hold the object returned
by read.  Because it has a handle on this object, the function can
look at what you entered before deciding whether or not to return
it.  As you probably guessed, numberp is a predicate that tests
whether its argument is a number.

If the value entered by the user isn't a number, ask-number calls
itself.  The result is a function that insists on getting a number:

> (ask-number)
Please enter a number. a
Please enter a number. (ho hum)
Please enter a number. 52
52

Variables like those we have seen so far are called local variables.
They are only valid within a certain context.  There is another
kind of variable, called a global variable, that can be visible
everywhere.

[The real distinction here is between lexical and special variables,
but we will not need to consider this until Chapter 6.]

You can create a global variable by giving a symbol and a value to
defparameter:

> (defparameter *glob* 99)
*GLOB*

Such a variable will then be accessible everywhere, except in
expressions that create a new local variable with the same name.
To avoid the possibility of this happening by accident, it's
conventional to give global variables names that begin and end with
asterisks.  The name of the variable we just created would be
pronounced "star-glob-star".

You can also define global constants, by calling defconstant:

(defconstant limit (+ *glob* 1))

There is no need to give constants distinctive names, because it
will cause an error if anyone uses the same name for a variable.
If you want to check whether some symbol is the name of a global
variable or constant, use boundp:

> (boundp '*glob*)
T

2.11 Assignment

In Common Lisp the most general assignment operator is setf.  We
can use it to do assignments to either kind of variable:

> (setf *glob* 98)
98
> (let ((n 10))
    (setf n 2)
    n)
2

When the first argument to setf is a symbol that is not the name
of a local variable, it is taken to be a global variable:

> (setf x (list 'a 'b 'c))
(A B C)

That is, you can create global variables implicitly, just by
assigning them values.  In source files, at least, it is better
style to use explicit defparameters.

You can do more than just assign values to variables.  The first
argument to setf can be an expression as well as a variable name.
In such cases, the value of the second argument is inserted in the
place referred to by the first:

> (setf (car x) 'n) 
N
> x
(N B C)

The first argument to setf can be almost any expression that refers
to a particular place.  All such operators are marked as "settable"
in Appendix D.

You can give any (even) number of arguments to setf.  An expression
of the form

(setf a b 
      c d 
      e f)

is equivalent to three separate calls to setf in sequence:

(setf a b)
(setf c d)
(setf e f)

2.12 Functional Programming

Functional programming means writing programs that work by returning
values, instead of by modifying things.  It is the dominant paradigm
in Lisp.  Most built-in Lisp functions are meant to be called for
the values they return, not for side-effects.

The function remove, for example, takes an object and a list and
returns a new list containing everything but that object:

> (setf lst '(c a r a t))
(C A R A T)
> (remove 'a lst)
(C R T)

Why not just say that remove removes an object from a list?  Because
that's not what it does.  The original list is untouched afterwards:

> lst
(C A R A T)

So what if you really do want to remove something from a list? In
Lisp you generally do such things by passing the list as an argument
to some function, and using setf with the return value.  To remove
all the as from a list x, we say:

(setf x (remove 'a x))

Functional programming means, essentially, avoiding setf and things
like it.  At first sight it may be difficult to imagine how this
is even possible, let alone desirable.  How can one build programs
just by returning values?

It would be inconvenient to do without side-effects entirely.
However, as you read further, you may be surprised to discover how
few you really need.  And the more side-effects you do without,
the better off you'll be.

One of the most important advantages of functional programming is
that it allows interactive testing.  In purely functional code,
you can test each function as you write it.  If it returns the
values you expect, you can be confident that it is correct.  The
added confidence, in the aggregate, makes a huge difference.  You
have instant turnaround when you make changes anywhere in a program.
And this instant turnaround enables a whole new style of programming,
much as the telephone, as compared to letters, enabled a new style
of communication.

2.13 Iteration

When we want to do something repeatedly, it is sometimes more
natural to use iteration than recursion.  A typical case for
iteration is to generate some sort of table.  This function

(defun show-squares (start end)
  (do ((i start (+ i 1)))
      ((> i end) 'done)
    (format t "~A ~A~%" i (* i i))))

prints out the squares of the integers from start to end:

> (show-squares 2 5)
2 4
3 9 
4 16
5 25
DONE

The do macro is the fundamental iteration operator in Common Lisp.
Like let, do can create variables, and the first argument is a list
of variable specifications.  Each element of this list can be of
the form

                   (variable initial update)

where variable is a symbol, and initial and update are expressions.
Initially each variable will be set to the value of the corresponding
initial; on each iteration it will be set to the value of the
corresponding update. The do in show-squares creates just one
variable, i.  On the first iteration i will be set to the value of
start, and on successive iterations its value will be incremented
by one.

The second argument to do should be a list containing one or more
expressions.  The first expression is used to test whether iteration
should stop.  In the case above, the test expression is (> i end).
The remaining expressions in this list will be evaluated in order
when iteration stops, and the value of the last will be returned
as the value of the do.  So show-squares will always return done.

The remaining arguments to do comprise the body of the loop.  They
will be evaluated, in order, on each iteration.  On each iteration
the variables are updated, then the termination test is evaluated,
and then (if the test failed) the body is evaluated.

For comparison, here is a recursive version of show-squares:

(defun show-squares (i end)
  (if (> i end)
      'done
      (progn
        (format t "~A ~A~%" i (* i i))
        (show-squares (+ i 1) end))))

The only thing new in this function is progn.  It takes any number
of expressions, evaluates them in order, and returns the value of
the last.

Common Lisp has simpler iteration operators for special cases.  To
iterate through the elements of a list, for example, you would be
more likely to use dolist.  Here is a function that returns the
length of a list:

(defun our-length (lst)
  (let ((len 0))
    (dolist (obj lst)
      (setf len (+ len 1)))
    len))

Here dolist takes an argument of the form (variable expression),
followed by a body of expressions. The body will be evaluated with
variable bound to successive elements of the list returned by
expression.  So the loop above says, for each obj in lst, increment
len.

The obvious recursive version of this function would be:

(defun our-length (lst)
  (if (null lst)
      0
      (+ (our-length (cdr lst)) 1)))

Or, if the list is empty, its length is zero; otherwise it is the
length of the cdr plus one.  This version of our-length is cleaner,
but because it's not tail-recursive (Section 13.2), it won't be as
efficient.

2.14 Functions as Objects

In Lisp, functions are regular objects, like symbols or strings or
lists.  If we give the name of a function to function, it will
return the associated object.  Like quote, function is a special
operator, so we don't have to quote the argument:

> (function +)
# This strange-looking return value is the way a function might be displayed in a typical Common Lisp implementation. Until now we have only dealt with objects that look the same when Lisp displays them as when we typed them in. This convention does not apply to functions. Internally, a built-in function like + is likely to be a segment of machine language code. A Common Lisp implementation may choose whatever external representation it likes. Just as we can use ' as an abbreviation for quote, we can use \#' as an abbreviation for function: > #'+ # This abbreviation is known as sharp-quote. Like any other kind of object, we can pass functions as arguments. One function that takes a function as an argument is apply. It takes a function and a list of arguments for it, and returns the result of applying the function to the arguments: > (apply #'+ '(1 2 3)) 6 > (+ 1 2 3) 6 It can be given any number of arguments, so long as the last is a list: > (apply #'+ 1 2 '(3 4 5)) 15 The function funcall does the same thing but does not need the arguments to be packaged in a list: > (funcall #'+ 1 2 3) 6 The defun macro creates a function and gives it a name. But functions don't have to have names, and we don't need defun to define them. Like most other kinds of Lisp objects, we can refer to functions literally. To refer literally to an integer, we use a series of digits; to refer literally to a function, we use what's called a lambda expression. A lambda expression is a list containing the symbol lambda, followed by a list of parameters, followed by a body of zero or more expressions. Here is a lambda expression representing a function that takes two numbers and returns their sum: (lambda (x y) (+ x y)) The list (x y) is the parameter list, and after it comes the body of the function. A lambda expression can be considered as the name of a function. Like an ordinary function name, a lambda expression can be the first element of a function call, > ((lambda (x) (+ x 100)) 1) 101 and by affixing a sharp-quote to a lambda expression, we get the corresponding function, > (funcall #'(lambda (x) (+ x 100)) 1) 101 Among other things, this notation allows us to use functions without naming them. ----------------------------------------------------------------- What is Lambda? The lambda in a lambda expression is not an operator. It is just a symbol. [3] In earlier dialects of Lisp it had a purpose: functions were represented internally as lists, and the only way to tell a function from an ordinary list was to check if the first element was the symbol lambda. In Common Lisp, you can express functions as lists, but they are represented internally as distinct function objects. So lambda is no longer really necessary. There would be no inconsistency in requiring that functions be denoted as ((x) (+ x 100)) instead of (lambda (x) (+ x 100)) but Lisp programmers were used to beginning functions with the symbol lambda, so Common Lisp retained it for the sake of tradition. ----------------------------------------------------------------- 2.15 Types Lisp has an unusually flexible approach to types. In many languages, variables are what have types, and you can't use a variable without specifying its type. In Common Lisp, values have types, not variables. You could imagine that every object had a label attached to it, identifying its type. This approach is called manifest typing. You don't have to declare the types of variables, because any variable can hold objects of any type. Though type declarations are never required, you may want to make them for reasons of efficiency. Type declarations are discussed in Section 13.3. The built-in Common Lisp types form a hierarchy of subtypes and supertypes. An object always has more than one type. For example, the number 27 is of type fixnum, integer, rational, real, number, atom, and t, in order of increasing generality. (Numeric types are discussed in Chapter 9.) The type t is the supertype of all types, so everything is of type t. The function typep takes an object and a type specifier, and returns true if the object is of that type: > (typep 27 'integer) T We will mention the various built-in types as we encounter them. 2.16 Looking Forward In this chapter we have barely scratched the surface of Lisp. And yet a portrait of a very unusual language is beginning to emerge. To start with, the language has a single syntax to express all program structure. This syntax is based on the list, which is a kind of Lisp object. Functions, which are Lisp objects in their own right, can be expressed as lists. And Lisp is itself a Lisp program, made almost entirely of Lisp functions no different from the ones you can define yourself. Don't worry if the relations between all these ideas are not entirely clear. Lisp introduces so many novel concepts that it takes some time to get used to all the new things you can do with it. One thing should be clear at least: there are some startlingly elegant ideas here. Richard Gabriel once half-jokingly described C as a language for writing Unix. [4] We could likewise describe Lisp as a language for writing Lisp. But this is a different kind of statement. A language that can be written in itself is fundamentally different from a language good for writing some particular class of applications. It opens up a new way of programming: as well as writing your program in the language, you can improve the language to suit your program. If you want to understand the essence of Lisp programming, this idea is a good place to begin. Summary 1. Lisp is an interactive language. If you type an expression into the toplevel, Lisp will display its value. 2. Lisp programs consist of expressions. An expression can be an atom, or a list of an operator followed by zero or more arguments. Prefix syntax means that operators can take any number of arguments. 3. The evaluation rule for Common Lisp function calls: evaluate the arguments left to right, and pass them to the function denoted by the operator. The quote operator has its own evaluation rule, which is to return the argument unchanged. 4. Along with the usual data types, Lisp has symbols and lists. Because Lisp programs are expressed as lists, it's easy to write programs that write programs. 5. The three basic list functions are cons, which builds a list; car, which returns the first element; and cdr, which returns everything after the first element. 6. In Common Lisp, t represents true and nil represents false. In a logical context, anything except nil counts as true. The basic conditional is if. The and and or operators resemble conditionals. 7. Lisp consists mainly of functions. You can define new ones with defun. 8. A function that calls itself is recursive. A recursive function should be considered as a process rather than a machine. 9. Parentheses are not an issue, because programmers read and write Lisp by indentation. 10. The basic i/o functions are read, which includes a complete Lisp parser, and format, which generates output based on templates. 11. You can create new local variables with let, and global variables with defparameter. 12. The assignment operator is setf. Its first argument can be an expression. 13. Functional programming, which means avoiding side-effects, is the dominant paradigm in Lisp. 14. The basic iteration operator is do. 15. Functions are regular Lisp objects. They can be passed as arguments, and denoted by lambda expressions. 16. In Lisp, values have types, not variables. Problems 1. Describe what happens when the following expressions are evaluated: a. (+ (- 5 1) (+ 3 7)) b. (list 1 (+ 2 3)) c. (if (listp 1) (+ 1 2) (+ 3 4)) d. (list (and (listp 3) t) (+ 1 2)) 2. Give three distinct cons expressions that return (a b c). 3. Using car and cdr, define a function to return the fourth element of a list. 4. Define a function that takes two arguments and returns the greater of the two. 5. What do these functions do? a. (defun enigma (x) (and (not (null x)) (or (null (car x)) (enigma (cdr x))))) b. (defun mystery (x y) (if (null y) nil (if (eql (car y) x) 0 (let ((z (mystery x (cdr y)))) (and z (+ z 1)))))) 6. What could occur in place of the x in each of the following exchanges? a. > (car (x (cdr '(a (b c) d)))) B b. > (x 13 (/ 1 0)) 13 c. > (x #'list 1 nil) (1) 7. Using only operators introduced in this chapter, define a function that takes a list as an argument and returns true if one of its elements is a list. 8. Give iterative and recursive definitions of a function that a. takes a positive integer and prints that many dots. b. takes a list and returns the number of times the symbol a occurs in it. 9. A friend is trying to write a function that returns the sum of all the non-nil elements in a list. He has written two versions of this function, and neither of them work. Explain what's wrong with each, and give a correct version: a. (defun summit (lst) (remove nil lst) (apply #'+ lst)) b. (defun summit (lst) (let ((x (car lst))) (if (null x) (summit (cdr lst)) (+ x (summit (cdr lst)))))) Notes [1] The names car and cdr derive from the internal representation of lists in the first Lisp implementation: car stood for "contents of the address part of the register" and cdr stood for "contents of the decrement part of the register." [2] Readers who have trouble with the concept of recursion may want to consult either of the following: Touretzky, David S. Common Lisp: A Gentle Introduction to Symbolic Computation. Benjamin/Cummings, Redwood City (CA), 1990, Chapter 8. Friedman, Daniel P., and Matthias Felleisen. The Little Lisper. MIT Press, Cambridge, 1987. [3] In Ansi Common Lisp there is also a lambda macro that allows you to write (lambda (x) x) for #'(lambda (x) x). Since the use of this macro obscures the symmetry between lambda expressions and symbolic function names (where you still have to use sharp-quote), it yields a specious sort of elegance at best. [4] Gabriel, Richard P. Lisp: Good News, Bad News, How to Win Big. AI Expert, June 1991, p. 34. ------------------------------------------------------------------- Available at: http://www.amazon.com/exec/obidos/ASIN/0133708756

