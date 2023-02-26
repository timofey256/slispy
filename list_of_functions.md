##List of functions in the dialect

Here is a table of some standard Scheme functions and what they do:

| Function | Description |
| --- | --- |
| + | Adds its arguments together. |
| - | Subtracts its second and subsequent arguments from the first argument. |
| * | Multiplies its arguments together. |
| / | Divides its first argument by its second and subsequent arguments. |
| =, >, <, >=, <= | Numeric comparison operators. = checks if all arguments are equal, > and < check if the first argument is greater or less than the subsequent argument(s), and >= and <= check if the first argument is greater or equal to or less or equal to subsequent argument(s). |
| math functions | all math functions from Python math library |
| expt | Math power function. |
| abs | Math abs function. |
| eq? | Checks if its two arguments are the same object in memory. |
| equal? | Checks if its two arguments have the same value. |
| car | Returns the first element of a list. |
| cdr | Returns the rest of a list after its first element. |
| setcar/setcdr | Sets first/second element in the list |
| cons | Creates a new list by adding its first argument to the front of its second argument (which must be a list). |
| list | Creates a new list from its arguments. |
| list? | Checks if object is a List type. |
| null? | Checks if object is a null object. |
| number? | Checks if object is a number. |
| append | Concatenates two or more lists together into a single list. |
| length | Returns the length of a list or string. |
| null? | Returns #t if its argument is the empty list () or #f otherwise. |
| member | Searches a list for a specified value and returns the sublist starting with the first occurrence of that value, or #f if it is not found. |
| map | Applies a function to each element of a list and returns a new list of the results. |
| min/max | Returns min/max element of the expression. |
| apply | Applies a function to a list of arguments. The first argument is the function, and the subsequent arguments are the arguments to be passed to the function. |
| round | Rounds expression. |
| print | Prints expression. | 
