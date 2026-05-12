# Some classic causes of code bugs

1. Reasons your code produces NaN
   1. There is a problem with the ground-truth data, so something gets divided by zero.
   2. The model uses an operation that is sensitive to numerical values, such as `log` or `softmax`.
   3. The model has diverged and the values have blown up to infinity.

   How to debug a NaN:

   ```python
   # Set breakpoints in your code. Keep using a divide-and-conquer
   # approach to home in on the source of the bug.

   if torch.isnan(number):
       __import__('ipdb').set_trace()
   ```
