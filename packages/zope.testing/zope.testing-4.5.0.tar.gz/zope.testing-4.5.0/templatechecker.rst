Template checker for doctest
============================

The standard doctest checker tests whether doctest output matches
exactly, or with holes, or with whitespace differences.  The
zope.testing.renormalizing checker allows more powerful use of regulat
expressions.

The template checker takes this a step further:

- Matches can use test data,

- Matches can set test data.

Here are some examples.

    >>> x = y
    >>> print("The value of x is %s." % y)
    The value of x is ${y}

In this example, the match took the value of y into account.  It might
have been computed randomly, but we can still use the expected output
to make an assertion.

Sometimes, we may want to capture some of the output to make later
assertions. Suppose we run a function that runs some tests and prints
the number of tests run.  We want to assert that the number of tests
was between 5 and 9:

   >>> run_tests()
   Ran ${/.+/=x} tests.

   >>> 5 < x < 9
   True

Notes:

This is often useful when matching generated data structures, which
we happen to print.

Is there a more direct way to deal with this, by matching data
structures?

