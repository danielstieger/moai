"""Where markers and rewrites register themselves.

New marker: a function with @marker in a module of markers/ (a new file there is found automatically):

    @marker("DATE", "DATE(y,m,d)", "fixed date", args=3)
    def date(conv, args, what):
        return node(OF + "DateLiteral", {...})

`conv` is the Converter (kern.py): conv.fix(arg) converts an argument, conv.string/integer/boolean read a literal;
`args` are the printed argument nodes, `what` the location for an error (raise Stop(f"{what}: ...")). The result is a
blueprint node (knoten.node). The argument count is checked here, the --help list is generated from these entries.
statement=True: valid only as a statement of its own. A @rewrite handles a printed concept instead of a marker.
"""
EXPRESSIONS, STATEMENTS, FORMS, REWRITES, TOPICS = {}, {}, set(), {}, {}


def _count(args):
    return (args, args) if isinstance(args, int) else args


def _topic(module, syntax, result):
    TOPICS.setdefault(module, []).append((syntax, result))


def marker(name, syntax, result, args=(0, None), statement=False):
    """Register fn(conv, args, what) as the marker `name`. args: exact count or (min, max); max None = open."""
    def register(fn):
        (STATEMENTS if statement else EXPRESSIONS)[name] = (fn, _count(args), syntax)
        _topic(fn.__module__, syntax, result)
        return fn
    return register


def form(name, syntax, result, module):
    """A marker that is no call of its own (if (VALIDATION()), switch (STATUS_SWITCH(x)), MAPPER inside SQL): help only."""
    FORMS.add(name)
    _topic(module, syntax, result)


def rewrite(*concepts):
    """Register fn(conv, n) for printed nodes of these concepts; it returns a node, or None to pass on.
    Handlers run in import order: markers first (__init__ of markers), then java.py."""
    def register(fn):
        for c in concepts:
            REWRITES.setdefault(c, []).append(fn)
        return fn
    return register


def check_args(name, args, what, entry):
    _, (low, high), syntax = entry
    if len(args) < low or (high is not None and len(args) > high):
        from .knoten import Stop
        raise Stop(f"{what}: {len(args)} argument(s) given, write {syntax}")
