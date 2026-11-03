"""Command bodies (command init, page init, scopes, conclusions, final conclusions, termination handlers).
Command parameters and variables are written by name; page init ends with `return x;`"""
from ..knoten import OF, node
from ..registry import marker


@marker("DONE", "DONE()", "done", statement=True)
def done(conv, args, what):
    return node(OF + "DoneCommand")


@marker("PAGE", 'PAGE("Name")', "page Name", args=1, statement=True)
def page(conv, args, what):
    return node(OF + "PageCommand", refs={"page": conv.string(args[0], "PAGE name")})


@marker("PUSH", "PUSH(x)", "pushSelection(x)", args=1, statement=True)
def push(conv, args, what):
    return node(OF + "PushObject", children={"exp": conv.fix(args[0])})


@marker("QUEUE_NEXT", 'QUEUE_NEXT("Command",args)', "queue next command", args=(1, None), statement=True)
def queue_next(conv, args, what):
    call = node(OF + "CommandCallBasis", children={"actualArgument": [conv.fix(a) for a in args[1:]]},
                refs={"command": conv.string(args[0], "QUEUE_NEXT command")})
    return node(OF + "SessionQueueNextCommand", children={"commandCall": call})


@marker("TERM_OK", "TERM_OK()", "terminatedInFinalOk (termination handler)")
def term_ok(conv, args, what):
    return node(OF + "PageCmdTermConceptFuntionParamTermOk")


@marker("PUSHED", "PUSHED()", "pushed (termination handler)")
def pushed(conv, args, what):
    return node(OF + "PageCmdTermConceptFuntionParamPushed")


@marker("WAS_CHILD", "WAS_CHILD()", "wasChild (termination handler)")
def was_child(conv, args, what):
    return node(OF + "PageCmdTermConceptFuntionParamChild")
