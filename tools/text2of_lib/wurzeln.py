"""Which nodes of a root are converted: members, bodies of test methods, getters, functions of commands and modules."""
from blueprint import Structure

from . import markers  # noqa: F401  registers the markers
from . import java     # noqa: F401  registers the rewrites, after the markers
from .kern import Converter
from .knoten import BL, MM, OF, Stop, fq, kid, kids, ref, walk

METHOD_ROOT_CONCEPTS = {OF + "Service": OF + "ServiceInstanceMethodDeclaration",
                        MM + "Repository": MM + "RepositoryInstanceMethodDeclaration"}
BODY_ONLY = (BL + "ConstructorDeclaration", OF + "OFXTestMethod")
# Selector of a function of a command, module or roles root: the role it sits in. Longer paths are built in `functions`.
SELECTOR_OF_ROLE = {"commandInit": "init", "okConclusionStatements": "ok", "authFunction": "auth",
                    "pageInit": "init", "scopeConceptFunc": "scopes", "func": "term", "staticRoleFunc": "is"}


def is_class_root(root):
    return bool(kids(root, "member") or kids(root, "content") or kids(root, "businessProperties")) \
        or fq(root) in METHOD_ROOT_CONCEPTS or fq(root).endswith(("Entity", "DTO", "ValueObject", "OFXTestSuit"))


def functions(root):
    """(selector, owner, body role, body) of every function of a command, module or roles root.

    Selectors: init, ok, auth, page:NAME:init, page:NAME:scopes, page:NAME:term, page:NAME:conc:N, role:NAME:is;
    any other function: its path of roles."""
    st = Structure()
    out = []

    def visit(n, path, prefix):
        for c in n.get("children", []):
            for i, x in enumerate(c.get("nodes", [])):
                role = c["role"]
                here = prefix
                if fq(x) == OF + "PageCrtl":
                    here = f"page:{x.get('name')}"
                elif fq(x) == OF + "PageConclusion":
                    here = f"{prefix}:conc:{i}"
                elif fq(x) == OF + "StaticRole":
                    here = f"role:{x.get('name')}"
                body = kid(x, "body")
                if body is not None and st.fits(fq(x), BL + "ConceptFunction"):
                    if fq(n) == OF + "PageConclusion":
                        sel = prefix
                    else:
                        sel = SELECTOR_OF_ROLE.get(role, role)
                        sel = f"{prefix}:{sel}" if prefix else sel
                    out.append((sel, x, "body", body))
                visit(x, path + [role], here)
    visit(root, [], "")
    return out


def bodies(root):
    """(selector, owner reference, role, body reference): where Java text goes (mps_mcp_parse_java_and_insert, insert.mode
    child, parentRef = owner, role)."""
    if is_class_root(root):
        out = []
        for m in kids(root, "member") + kids(root, "content"):
            if fq(m) in BODY_ONLY and kid(m, "body") is not None:
                out.append((m.get("name"), m["reference"], "body", kid(m, "body")["reference"]))
        out += [(f"get:{bp.get('name')}", g["reference"], "statementList", kid(g, "statementList")["reference"])
                for bp, g in getters(root)]
        return out
    return [(sel, f["reference"], role, body["reference"]) for sel, f, role, body in functions(root)]


def getters(root):
    """(business property, GetAccessor) of the virtual properties."""
    out = []
    for bp in kids(root, "businessProperties"):
        impl = kid(bp, "propertyImplementation")
        g = kid(impl, "getAccessor") if impl is not None else None
        if g is not None and kid(g, "statementList") is not None:
            out.append((bp, g))
    return out


def _safely(errors, label, convert):
    """Run one conversion; what stops it is reported for its member, the others go on."""
    try:
        return convert()
    except Stop as e:
        errors.append(f"{label}: {e}")
    except (IndexError, KeyError, TypeError, AttributeError, ValueError) as e:
        errors.append(f"{label}: this tool failed ({type(e).__name__}: {e}); a marker or Java form it does not handle, "
                      "change text2of_lib/")
    return None


def field_refs(persistence):
    """(mapping name, property name) -> reference of the mapping's own FieldMapping, from a printed PersistenceDescription
    or repository. Nested key fields of reference mappings are left out: that is what makes a name ambiguous."""
    out = {}
    for m in walk(persistence):
        if fq(m).endswith(("EntityMapping", "NoKeyMapperField")):
            for a in kids(m, "atomMpig"):
                if fq(a) == MM + "FieldMapping":
                    r = ref(a, "property")
                    if r is not None:
                        out[(m.get("name"), r.get("target"))] = a["reference"]
    return out


def convert_root(root, repo_types, only, fields=None):
    """(rows, errors); a row is (label, reference of the node to replace, blueprint)."""
    root_refs = {x["reference"]: fq(x) for x in walk(root)}
    rc = fq(root)
    if not is_class_root(root):
        return convert_functions(root, root_refs, only)
    rows, errors = [], []
    members = [m for m in kids(root, "member") + kids(root, "content") if not only or m.get("name") in only]
    replaced = set()
    for m in members:
        if fq(m) in BODY_ONLY:
            replaced |= {x["reference"] for x in walk(kid(m, "body"))}
        elif fq(m).endswith("MethodDeclaration"):
            replaced |= {x["reference"] for x in walk(m)}
    props = kids(root, "businessProperties")
    root_props = {bp.get("name") for bp in props}
    bigdec_props = set()
    for bp in props:
        t = kid(bp, "type")
        if t is not None and fq(t) == BL + "ClassifierType" and (ref(t, "classifier") or {}).get("target") == "BigDecimal":
            bigdec_props.add(bp.get("name"))
    make = lambda n: Converter(n, root_refs, replaced, bigdec_props, root_props=root_props, fields=fields)

    for m in members:
        mc, name = fq(m), m.get("name")
        if mc in BODY_ONLY:
            body = kid(m, "body")
            out = _safely(errors, name, lambda: make(m).fix(body))
            if out is not None:
                rows.append((name + " (body)", body["reference"], out))
        elif mc.endswith("MethodDeclaration"):
            out = _safely(errors, name, lambda: make(m).fix(m))
            if out is None:
                continue
            if mc == BL + "InstanceMethodDeclaration" and rc in METHOD_ROOT_CONCEPTS:
                out["concept"] = METHOD_ROOT_CONCEPTS[rc]
                if rc == MM + "Repository":
                    out.setdefault("properties", []).append({"name": "repoMethodType", "value": repo_types.get(name, "READONLY")})
            rows.append((name, m["reference"], out))
    for bp, g in getters(root):
        sel, body = f"get:{bp.get('name')}", kid(g, "statementList")
        if kids(body, "statement") and (not only or sel in only):
            out = _safely(errors, sel, lambda: make(g).fix(body))
            if out is not None:
                rows.append((sel, body["reference"], out))
    return rows, errors


def convert_functions(root, root_refs, only):
    """Replace the body of every function of a command, module or roles root (command init, page init, scopes, ...)."""
    containers = {}
    for role, concept in (("parameter", OF + "ContainerParamReference"), ("variable", OF + "ContainerVariableReference")):
        for d in kids(root, role):
            containers[d.get("name")] = (d["reference"], concept)
    found = functions(root)
    replaced = {y["reference"] for _, _, _, body in found for y in walk(body)}
    rows, errors = [], []
    for sel, f, _, body in found:
        if not kids(body, "statement") or (only and sel not in only):
            continue
        out = _safely(errors, sel, lambda: Converter(f, root_refs, replaced, set(), containers).fix(body))
        if out is not None:
            rows.append((sel, body["reference"], out))
    return rows, errors
