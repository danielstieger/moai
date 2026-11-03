"""scaffold.py rollen, scaffold.py app: roles and the AppUI module."""
from .bausteine import SpecError, java_lines, literal
from .registry import Ergebnis, Java, generator

DX = "org.modellwerkstatt.dataux.structure."


def _model(spec, key):
    for k in ("firma", "app"):
        if not spec.get(k):
            raise SpecError(f"$.{k} is missing")
    return (spec.get("namen") or {}).get(key + "modell", f"{spec['firma']}.{spec['app']}.{key}")


@generator("rollen", "scaffold.py rollen SPEC [-o DIR]",
           "Roles and Permissions: \"rollen\": {\"name\": .., \"liste\": [{\"name\": .., \"benutzer\": .. | \"java\": ..}]}, one static role each")
def rollen(spec, args=()):
    r = spec.get("rollen") or {}
    if not r.get("name") or not r.get("liste"):
        raise SpecError("$.rollen needs name and liste")
    model = _model(spec, "rollen")
    java = []
    roles = []
    for i, x in enumerate(r["liste"]):
        if not x.get("name"):
            raise SpecError(f"$.rollen.liste[{i}]: needs a name")
        roles.append({"concept": "StaticRole", "properties": {"name": x["name"]},
                      "children": {"staticRoleFunc": {"concept": "StaticRoleFunc", "children": {"body": "StatementList"}}}})
        body = x.get("java") or f'userEnvironment.getUserName().equals("{x.get("benutzer", x["name"].lower())}");'
        java.append(Java(f"rolle-{x['name'].lower()}", java_lines(body.splitlines()),
                         f"{r['name']} role:{x['name']}:is: parse as STATEMENTS into its body"))
    root = {"concept": "RolesAndPermissions", "properties": {"name": r["name"]}, "children": {"staticRoles": roles}}
    return Ergebnis(model, [("rollen", root)], java, [])


@generator("app", "scaffold.py app SPEC [-o DIR]",
           "AppUI module: \"anwendung\": {\"name\": .., \"config\": \"FX8\", \"version\": .., \"titel\": .., \"menue\": [commands], \"auth\": JAVA}")
def app(spec, args=()):
    a = spec.get("anwendung") or {}
    for k in ("name", "menue"):
        if not a.get(k):
            raise SpecError(f"$.anwendung.{k} is missing")
    model = _model(spec, "app")
    root = {"concept": DX + "AppUiModule", "properties": {"name": a["name"]},
            "references": {"configuration": a.get("config", "FX8")},
            "children": {"authFunction": {"concept": DX + "AppAuthenticationFunction", "children": {"body": "StatementList"}},
                         "mainMenu": [{"concept": "MenuAction", "references": {"command": n}} for n in a["menue"]],
                         "options": [{"concept": DX + "OptVersion", "children": {"exp": literal(a.get("version", "1.0"))}},
                                     {"concept": DX + "OptOfficialAppName", "children": {"exp": literal(a.get("titel", a["name"]))}}]}}
    java = []
    if a.get("auth"):
        java.append(Java("auth", java_lines(a["auth"].splitlines()), f"{a['name']} auth: parse as STATEMENTS into its body"))
    notes = ["The module imports the unit models of its menu commands and the base model of its configuration.",
             "FX8 has no login mask: FX8Application takes the user from the environment variable USERNAME; set it in the run"
             " configuration or the shell (MCP cannot set environment or VM parameters), and --enable-native-access=ALL-UNNAMED."]
    if not a.get("auth"):
        notes.append("No \"auth\": the authentication body is empty; it must set the user and end with a boolean expression.")
    return Ergebnis(model, [("app", root)], java, notes)
