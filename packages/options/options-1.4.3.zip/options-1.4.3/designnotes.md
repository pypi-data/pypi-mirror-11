

# Concurrency

Concurrent programs can use options, but options are not inherently
thread-safe. Options represent arbitrary context, and changes would not be
coordinated between threads.

Using a with statement and OptionsContext can effectively reduce the thread
safety of an object to nil because the object is modified for an
indeterminate period in an unlocked sense. It is probably not feasible to
increase the thread safety of optioned objects in the general case; thread
safety is orthogonal to parameter design, and probably cannot be
transparently or automatically fixed by anything options can do.

# Alternate Use Cases

with module quoter have found some interesting use cases like abbreviation
args (MultiSetter), and have further explored how subclasses will integrate
with the delegation-based options. Have discovered that some subclasses will
want flat args, prohibit superclass args. Also, some args could potentially
allow setting at instantiation time but not call/use time.

Finding more graceful and systematic ways to express these different
use cases is an ongoing task.

Definite need for per-method args, and even the styling of methods,
separate from method calls. Have begun to explore these with `show`.
Need to map those features back to the base. Decorators for "stylable
methods" seem a good start.

# Attribute Access

We can currently get options values from attributes, but not set them
that way. Should we attempt a `__setattr__` implementation?

Even more interesting and also dicey, should we try to integrate
option values with class/instance `__dict__` values? This would allow
very direct attribute setting and greater transparency,
but would require some VERY fancy dancing around Python's
standard argument handling. A metaclass, decorators, and/or specialized
property managment would have to be built out and meticulously tested.
See `testprop.py` for some early work there.

# Test Cases

`say`, `show`, and `quoter` are all proving to be good test cases
in slightly different ways.  Keep mapping back their learnings here.

# Input and Output

Currently have implemented write-to-JSON and read-from-JSON files.
Might extend to YAML and INI styles. There is a separate repo
devoted to some of that work.

Also might consider integration with `os.environ` getters. While
I hate that style of configuration and its inummerable failure modes,
it's still possible and not a great stretch to connect into the
options family.

Similarly, connecting from `argparse` based `Namespace` objects
could be a nice simplification for some.