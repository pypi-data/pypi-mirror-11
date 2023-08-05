Like functools. Only not really.

cached:
    cachedfunction:
        a decorator that will cache-enable a function. The function will remember whatever output it's given for any given set up inputs, and return it in the future without having to actually call the original function. This behavior can reset by call the function's new "reset()" method.
