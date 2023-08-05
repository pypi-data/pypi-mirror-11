getwrapspec: Get argspec of wrapped functions for side-effect-only decorators
=============================================================================

If your decorator doesn't change the order of arguments, and you want to stack
decorators, use `getwrapspec.wraps()` instead of `functools.wraps()` and
`getwrapspec.getargspec()` if you want to retrieve the argspec of the real
function.
