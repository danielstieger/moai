"""The Converter: dispatch over the printed nodes; everything specific lives in markers/, java.py and methoden.py."""
from .knoten import BL, Stop, fq, kid, kids, node, prop, ref, short, unresolved, walk
from .registry import EXPRESSIONS, FORMS, REWRITES, STATEMENTS, check_args

SKIP_PROPS = {"resolveInfo", "shortDescription", "virtualPackage"}


class Converter:
    def __init__(self, member, root_refs, replaced, bigdec_props, containers=None, root_props=(), fields=None):
        self.member = member
        self.inside = {x["reference"] for x in walk(member)}
        self.root_refs = root_refs          # every node reference of the root -> concept
        self.replaced = replaced            # references of nodes this run re-creates (new IDs): refer by name
        self.bigdec_props = bigdec_props    # BigDecimal business properties of the root
        self.containers = containers or {}  # command parameters / variables: name -> (reference, concept of the reference)
        self.root_props = set(root_props)   # business properties of the root
        self.fields = fields or {}          # (mapping, field) -> node reference, from --persistenz
        self.locals = {x.get("name") for x in walk(member)
                       if fq(x) in (BL + "ParameterDeclaration", BL + "LocalVariableDeclaration")}
        self.bigdec_names = set()           # parameters / locals / closure params known as BigDecimal
        self.in_sql_block = False           # SQLTEXT is valid only inside the block of a SQL(..)
        for x in walk(member):
            if fq(x) in (BL + "ParameterDeclaration", BL + "LocalVariableDeclaration"):
                t = kid(x, "type")
                if t is not None and fq(t) == BL + "ClassifierType" and (ref(t, "classifier") or {}).get("target") == "BigDecimal":
                    self.bigdec_names.add(x.get("name"))

    # ---- reading literal arguments -------------------------------------------------------------------
    def string(self, n, what):
        if n is None or fq(n) != BL + "StringLiteral":
            raise Stop(f"{what}: a string literal is expected, found {short(n) if n else 'nothing'}")
        return prop(n, "value") or ""

    def integer(self, n, what):
        if n is None or fq(n) != BL + "IntegerConstant":
            raise Stop(f"{what}: an integer literal is expected, found {short(n) if n else 'nothing'}")
        return int(prop(n, "value") or 0)

    def boolean(self, n, what):
        if n is None or fq(n) != BL + "BooleanConstant":
            raise Stop(f"{what}: true or false is expected, found {short(n) if n else 'nothing'}")
        return (prop(n, "value") or "false") == "true"

    def marker(self, n):
        """(name, args) for an unresolved call written as a marker, else (None, None)."""
        if n is None:
            return None, None
        c = fq(n)
        if c in (BL + "LocalMethodCall", BL + "LocalStaticMethodCall", BL + "LocalInstanceMethodCall") \
                and unresolved(ref(n, "baseMethodDeclaration")):
            return n.get("name"), kids(n, "actualArgument")
        if c == BL + "UnknownLocalCall":
            return prop(n, "callee"), kids(n, "actualArgument")
        return None, None

    def split_property(self, n, what):
        """x.prop written inside a marker -> (operand node, property name)."""
        c = fq(n)
        if c == BL + "DotExpression" and fq(kid(n, "operation")) == BL + "FieldReferenceOperation":
            return self.fix(kid(n, "operand")), kid(n, "operation").get("name")
        if c == BL + "UnknownNameRef":
            tokens = prop(n, "tokens") or ""
            if "." in tokens:
                head, _, last = tokens.rpartition(".")
                return self.tokens(head), last
        raise Stop(f"{what}: x.property is expected, found {short(n)}")

    def is_bigdec(self, n):
        if n is None:
            return False
        name, _ = self.marker(n)
        if name == "BD":
            return True
        c = fq(n)
        if c == BL + "VariableReference" and n.get("name") in self.bigdec_names:
            return True
        r = ref(n, "variableDeclaration")
        if c == BL + "VariableReference" and r is not None and r.get("target") in self.bigdec_names:
            return True
        if c == BL + "VariableReference" and unresolved(r) and n.get("name") in self.bigdec_props:
            return True  # own business property written as a bare name
        if c == BL + "DotExpression":
            op = kid(n, "operation")
            if op is not None and fq(op) == BL + "FieldReferenceOperation" and op.get("name") in self.bigdec_props:
                return True
        return False

    # ---- dispatch ------------------------------------------------------------------------------------
    def statement_marker(self, name, args):
        """The node of a statement marker, or None when `name` is none (it stays an expression statement)."""
        entry = STATEMENTS.get(name)
        if entry is None:
            return None
        check_args(name, args, name, entry)
        return entry[0](self, args, name)

    def expression_marker(self, name, args, n):
        what = f"{name}(..) at {n.get('reference', '')}"
        entry = EXPRESSIONS.get(name)
        if entry is not None:
            check_args(name, args, what, entry)
            return entry[0](self, args, what)
        if name in STATEMENTS or name in FORMS:
            raise Stop(f"{what} is a statement marker; write it as a statement of its own")
        raise Stop(f"unknown marker or unresolved method {what}")

    def fix(self, n):
        """A printed node -> blueprint node."""
        c = fq(n)
        name, args = self.marker(n)
        if name is not None:
            return self.expression_marker(name, args, n)
        for handler in REWRITES.get(c, ()):
            out = handler(self, n)
            if out is not None:
                return out
        if c.startswith(BL + "Unknown"):
            raise Stop(f"the parser could not read {short(n)}; rewrite the expression")
        return self.copy(n)

    def tokens(self, text):
        """a.b.c the parser left as one name: local, command parameter or own property, then property references."""
        parts = (text or "").split(".")
        if parts[0] in self.locals or parts[0] in self.bigdec_names:
            e = node(BL + "VariableReference", refs={"variableDeclaration": parts[0]})
        elif parts[0] in self.containers:
            target, concept = self.containers[parts[0]]
            e = node(concept, refs={"variableDeclaration": target})
        else:
            e = node(BL + "LocalPropertyReference", refs={"property": parts[0]})
        for p in parts[1:]:
            e = node(BL + "DotExpression", children={"operand": e, "operation": node(BL + "PropertyReference", refs={"property": p})})
        return e

    def copy(self, n):
        """A node the parser got right: the same node, its children converted."""
        d = {"concept": fq(n)}
        props = [{"name": p["name"], "value": p["value"]} for p in n.get("properties", [])
                 if p.get("value") is not None and p["name"] not in SKIP_PROPS and p.get("declared", True) is not False
                 and not p.get("isDefault")]
        if props:
            d["properties"] = props
        refs = []
        for r in n.get("references", []):
            if unresolved(r):
                raise Stop(f"unresolved {r['role']} -> '{r.get('target')}' at {short(n)}")
            tr = r["targetReference"]
            by_name = tr in self.inside or tr in self.replaced
            refs.append({"role": r["role"], "target": r.get("target") if by_name else tr})
        if refs:
            d["references"] = refs
        ch = []
        for c in n.get("children", []):
            nodes = [self.fix(x) for x in c.get("nodes", [])]
            if nodes:
                ch.append({"role": c["role"], "nodes": nodes})
        if ch:
            d["children"] = ch
        return d
