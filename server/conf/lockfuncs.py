"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False

def cmdLocationCheck(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdLocationCheck()
    A simple check to see if the player(accessing_obj) is in the
    same location/room as the acccessed_obj, which could be a
    vehicle, door, or anything inbetween.
    """
    accessorParent = accessing_obj.location
    accessedParent = accessed_obj.location
    # This next part checks to make sure you're not already inside the object, 
    # i.e., to prevent entering the ship when you're already inside
    if accessedParent == accessorParent and not accessed_obj.location == accessed_obj and not accessed_obj == accessed_obj.location:
        nearby = True
    else:
        nearby = False
    return nearby