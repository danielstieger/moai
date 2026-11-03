"""Public building blocks: short specs (`blueprint.py build`) of the nodes the conventions use.

Import them instead of writing node JSON by hand, in a generator or in an option of one:
  types      ctype status_type list_type stub_type
  domain     business_property virtual_property spec_property key_property entity dto value_object status_decl repository
             service mapper
  ux         delegate path_delegate reference_delegate width form table grid pane page menu
  commands   command func param selected_param id_param var status_of ref dot selected param_ref rw ro
  text       literal column cap lower java_lines
"""
import re

JODA = "37fdf88a-1025-4d01-864a-0bf987f72e6f/java:org.joda.time(org.modellwerkstatt.manmap.runtime/)/~"
STUB_TYPES = {"LocalDate": JODA + "LocalDate", "DateTime": JODA + "DateTime",
              "BigDecimal": "6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.math(JDK/)/~BigDecimal"}
PUBLIC = "PublicVisibility"
DELEGATES = {"string": "StringDelegate", "int": "IntegerDelegate", "LocalDate": "LocalDateDelegate",
             "DateTime": "DateTimeDelegate", "BigDecimal": "BigDecimalDelegate", "status": "StatusDelegate"}


class SpecError(Exception):
    """The specification is wrong; the message names the place ($.aggregat...)."""


# ---- text --------------------------------------------------------------------------------------------
def column(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def cap(name):
    return name[:1].upper() + name[1:]


def lower(name):
    return name[:1].lower() + name[1:]


def literal(text):
    return {"concept": "StringLiteral", "properties": {"value": text}}


def java_lines(lines):
    """Lines of Java as the text of a file."""
    return "\n".join(lines) + "\n"


# ---- small nodes ---------------------------------------------------------------------------------------
def ref(concept, role, target):
    return {"concept": concept, "references": {role: target}}


def dot(operand, prop):
    return {"concept": "DotExpression", "children": {"operand": operand,
                                                      "operation": ref("PropertyReference", "property", prop)}}


def ctype(cls):
    return ref("ClassifierType", "classifier", cls)


def status_type(name):
    return ref("StatusType", "status", name)


def list_type(cls):
    return {"concept": "ListType", "children": {"elementType": ctype(cls)}}


def stub_type(name):
    return ctype(STUB_TYPES[name])


def func():
    return {"concept": "CommandVoidStatementList", "children": {"body": "StatementList"}}


def selected(cls):
    return ref("SelectedObject", "object", cls)


def param_ref(name):
    return ref("ContainerParamReference", "variableDeclaration", name)


# ---- domain -----------------------------------------------------------------------------------------
def prop_type(p, where):
    t = p.get("typ")
    if t == "liste":
        if not p.get("von"):
            raise SpecError(f'{where}: typ liste needs "von": element type')
        return list_type(p["von"])
    if t == "string":
        return "StringType"
    if t == "int":
        return "IntegerType"
    if t in STUB_TYPES:
        return stub_type(t)
    if t == "status":
        if not isinstance(p.get("status"), dict) or not p["status"].get("name"):
            raise SpecError(f'{where}: typ status needs "status": {{"name": .., "werte": [..]}}')
        return status_type(p["status"]["name"])
    if t == "boolean":
        raise SpecError(f"{where}: boolean is no Business Property type; model a yes/no as a status")
    if isinstance(t, str) and t[:1].isupper() and ("felder" in p or p.get("verweis")):
        return ctype(t)
    raise SpecError(f"{where}: type '{t}' unknown; a value object needs 'felder', an entity 'verweis': true")


def business_property(name, type_node, kurz, lang, options=()):
    return {"concept": "BusinessProperty",
            "properties": {"propertyName": name, "name": name},
            "children": {"shortDesc": literal(kurz), "longDesc": literal(lang), "type": type_node,
                         "propertyImplementation": {"concept": "DefaultPropertyImplementation", "children": {
                             "defaultGetAccessor": "DefaultGetAccessor",
                             "defaultSetAccessor": {"concept": "DefaultSetAccessor", "children": {"visibility": PUBLIC}}}},
                         "visibility": PUBLIC,
                         "propertyOption": list(options)}}


def virtual_property(name, type_node, kurz, lang, options=()):
    """Business property with a get accessor of its own; the body comes as Java (get:NAME), it is not persisted."""
    bp = business_property(name, type_node, kurz, lang, ["NotPersistedOption", *options])
    bp["children"]["propertyImplementation"] = {"concept": "CustomPropertyImplementation", "children": {
        "getAccessor": {"concept": "GetAccessor", "children": {"statementList": "StatementList"}}}}
    return bp


def spec_property(p, where):
    if not p.get("name"):
        raise SpecError(f"{where}: property needs a name")
    opts = []
    if "laenge" in p:
        opts.append({"concept": "LengthOption", "properties": {"min": str(p["laenge"][0]), "max": str(p["laenge"][1])}})
    if "bereich" in p:
        opts.append({"concept": "IRangeOption", "properties": {"start": str(p["bereich"][0]), "stop": str(p["bereich"][1])}})
    if p.get("unique"):
        opts.append("UniqueOption")
    kurz = p.get("kurz", cap(p["name"]))
    make = virtual_property if p.get("virtuell") else business_property
    return make(p["name"], prop_type(p, where), kurz, p.get("lang", kurz), opts)


def key_property(entity_name, table):
    return business_property("id", "IntegerType", "Id", f"Technischer Schlüssel {entity_name}",
                             ["KeyOption", {"concept": "AutoidOption", "children": {"sequenceName": literal("S_" + table)}}])


def entity(name, props, status=None, concept="Entity"):
    return {"concept": concept,
            "properties": {"isStatic": "true", "nestedName": name, "name": name, "resolveInfo": name},
            "children": {"visibility": PUBLIC,
                         "member": {"concept": "ConstructorDeclaration",
                                    "properties": {"nestedName": name, "name": name, "resolveInfo": name},
                                    "children": {"returnType": "VoidType", "body": "StatementList", "visibility": PUBLIC}},
                         **({"status": status} if status else {}),
                         "businessProperties": props}}


def dto(name, props):
    """DTO with its default constructor: the checker needs one, and a node factory adds it only on a first insert."""
    return entity(name, props, concept="DTO")


def value_object(name, props, equal):
    """Value object; equal: names of the properties that make two values equal. Constructor and with..: Java."""
    d = entity(name, props, concept="ValueObject")
    d["children"].pop("member")
    d["children"]["equalProperties"] = [ref("EqualPropertyReference", "property", n) for n in equal]
    return d


def status_decl(s, where):
    werte = s.get("werte") or []
    if not s.get("name") or not werte:
        raise SpecError(f"{where}: status needs a name and werte")
    elems = []
    for i, w in enumerate(werte):
        if not isinstance(w, list) or len(w) < 2:
            raise SpecError(f"{where}.werte[{i}]: [NAME, wert, kurz?, lang?]")
        kurz = w[2] if len(w) > 2 else cap(w[0].lower())
        e = {"concept": "StatusElement", "properties": {"value": w[1], "name": w[0]},
             "children": {"shortDescNew": literal(kurz), "longDescNew": literal(w[3] if len(w) > 3 else kurz)}}
        if i == 0:
            e["children"]["options"] = "OnCreationStatusElemOption"
        elems.append(e)
    return {"concept": "StatusDeclaration", "properties": {"name": s["name"]}, "children": {"element": elems}}


def property_status(props, where):
    """The status declarations of the properties with typ status."""
    return [status_decl(p["status"], f"{where}[{i}].status") for i, p in enumerate(props) if p.get("typ") == "status"]


def repository(name, members=()):
    """Repository; members: mapper() nodes, they must exist before the methods that name them."""
    children = {"visibility": PUBLIC}
    if members:
        children["member"] = list(members)
    return {"concept": "Repository",
            "properties": {"name": name, "nestedName": name, "resolveInfo": name, "isStatic": "true"},
            "children": children}


def mapper(name, cls, fields):
    """Read-only map of a repository, the result of a custom SQL. fields: {property: column}."""
    return {"concept": "NoKeyMapperField", "properties": {"name": name}, "references": {"classConcept": cls},
            "children": {"atomMpig": [{"concept": "FieldMapping", "references": {"property": p},
                                       "children": {"fieldName": literal(c)}} for p, c in fields.items()]}}


def service(name):
    return {"concept": "Service",
            "properties": {"isStatic": "true", "nestedName": name, "name": name, "resolveInfo": name},
            "children": {"visibility": PUBLIC}}


# ---- ux ------------------------------------------------------------------------------------------------
def delegate(name, typ, options=()):
    if typ not in DELEGATES:
        raise SpecError(f"no delegate for '{name}' of type {typ}; only {', '.join(DELEGATES)}")
    return {"concept": DELEGATES[typ], "children": {"boundTo": {"concept": "DuxLocalPropertyReference",
                                                                "references": {"property": name}},
                                                    "option": list(options)}}


def path_delegate(first, second, typ, options=()):
    """Delegate on a property of a property: lenker.nachname."""
    if typ not in DELEGATES:
        raise SpecError(f"no delegate for '{first}.{second}' of type {typ}; only {', '.join(DELEGATES)}")
    return {"concept": DELEGATES[typ], "children": {"boundTo": {"concept": "PathDot", "children": {
        "operand": ref("DuxLocalPropertyReference", "property", first),
        "operation": ref("OperationPropertyReference", "property", second)}}, "option": list(options)}}


def reference_delegate(name, shown, options=()):
    """Selection of an entity; shown: its properties in the list. The scope comes in page:NAME:scopes: META(x.name).setScope(..)."""
    return {"concept": "ReferenceDelegate", "children": {
        "boundTo": ref("DuxLocalPropertyReference", "property", name),
        "scopeText": {"concept": "RefDelegateScopeProps", "children": {
            "paths": [ref("DuxLocalPropertyReference", "property", s) for s in shown]}},
        "option": list(options)}}


def width(percent):
    return {"concept": "WidthDOption", "properties": {"percent": str(percent)}}


def menu(names):
    return {"concept": "MenuSub", "children": {"menuItems": [{"concept": "MenuAction", "references": {"command": n}}
                                                             for n in names]}}


def label_option(text):
    return {"concept": "LabelFOption", "children": {"expression": literal(text)}}


def form(cls, delegates, disabled=False, label=None, cols=1):
    """DelegateForm. An empty options role is kept: no factory LABEL without text."""
    options = []
    if disabled:
        options.append("DisabledFOption")
    if label:
        options.append(label_option(label))
    return {"concept": "DelegateForm", "references": {"boundClassifier": cls},
            "children": {"colWeights": ["OneWeight"] * cols, "delegates": list(delegates), "options": options}}


def table(cls, prop, delegates, label=None, actions=()):
    return {"concept": "Table", "references": {"boundClassifier": cls, "boundProperty": prop},
            "children": {"options": ([label_option(label)] if label else []) + ["SelectFirstFOption"],
                         "delegates": list(delegates),
                         "menuItems": menu(actions)}}


def grid(*children):
    """GridLayout, one column. No rowWeights: on insert every child adds its own row (form -1, table 1*); named weights
    would double them and the checker reports "1 cols and 4 rows, but 2 components". Other weights: SET CHILD afterwards."""
    return {"concept": "GridLayout", "children": {"colWeights": ["OneWeight"], "uxChild": list(children)}}


def pane(name, cls, child, actions=None):
    pp = {"concept": "PagePane", "properties": {"name": name, "isNamed": "true"},
          "references": {"boundClassifier": cls}, "children": {"uxChild": child}}
    if actions:
        pp["children"]["menuItems"] = menu(actions)
    return pp


def page(name, cls, panes, conclusions, title, term=None, scopes=False):
    """PageCrtl. panes: names of page panes, conclusions: label names, term: classifier of an any cmd term handler,
    scopes: with a scope function (page:NAME:scopes)."""
    ch = {"pageInit": {"concept": "PageInitConceptFunc", "children": {"body": "StatementList"}},
          "conclusion": [{"concept": "PageConclusion", "references": {"label": lab}, "children": {"function": func()}}
                         for lab in conclusions],
          "pagePaneActionProviderLink": [ref("PagePaneActionProviderLink", "actionProviderPagePane", x) for x in panes],
          "dynamicPageTitle": literal(title)}
    if term:
        ch["cmdTermHandler"] = {"concept": "PageCmdTermHandler", "properties": {"cmdTermType": "AnyCmdTerminated"},
                                "references": {"classifier": term},
                                "children": {"func": {"concept": "PageCmdTermConceptFunction",
                                                      "children": {"body": "StatementList"}}}}
    if scopes:
        ch["scopeConceptFunc"] = {"concept": "PageScopeConceptFunc", "children": {"body": "StatementList"}}
    return {"concept": "PageCrtl", "properties": {"name": name}, "references": {"boundObject": cls}, "children": ch}


# ---- commands ------------------------------------------------------------------------------------------
def param(name, type_node, initializer):
    return {"concept": "ContainerParameter", "properties": {"name": name},
            "children": {"type": type_node, "initializer": initializer}}


def selected_param(name, cls):
    return param(name, ctype(cls), selected(cls))


def id_param(name, cls):
    """Only the key of the selection: the command checks the aggregate out itself."""
    return param(name, "IntegerType", dot(selected(cls), "id"))


def rw(role):
    return {"concept": "OpenSavePermissionCmd", "children": {"expression": ref("PermissionHasReference", "evaluatePermission", role)}}


def ro(role):
    return {"concept": "OpenPermissionCmd", "children": {"expression": ref("PermissionHasReference", "evaluatePermission", role)}}


def var(name, cls):
    return {"concept": "ContainerVariable", "properties": {"name": name}, "children": {"type": ctype(cls)}}


def command(name, typ=None, params=(), variables=(), init=False, pages=(), ok=False, final=None,
            enabled=None, revert=None, hotkey=None, no_term=False, permissions=()):
    """Command. params: param(), variables: var(), init/ok: with an empty function, final/revert: variable/parameter
    name, enabled: expression of andIsEnabledNew, no_term: NEWSTYLE_CMD_TERM_HANDLING (any cmd term handler),
    permissions: rw(role), ro(role)."""
    props = {"name": name}
    if typ:
        props["newCommandType"] = typ
    if hotkey:
        props["defaultHotkey"] = hotkey
    ch = {"permissionNew": list(permissions), "parameter": list(params), "variable": list(variables), "pages": list(pages)}
    if init:
        ch["commandInit"] = func()
    if ok:
        ch["okConclusionStatements"] = func()
    if final:
        ch["finalOkSelection"] = ref("ContainerVariableReference", "variableDeclaration", final)
    if enabled:
        ch["andIsEnabledNew"] = enabled
    if revert:
        ch["reverts"] = param_ref(revert)
    if no_term:
        ch["options"] = "CommandNoPushNewTermOption"
    return {"concept": "Command", "properties": props, "children": {k: v for k, v in ch.items() if v != []}}


def status_of(operand, names, prop="status"):
    return {"concept": "StatusOfOperator", "children": {
        "statusLeftSide": dot(operand, prop),
        "statusElements": [ref("StatusElementReference", "statusElement", x) for x in names]}}
