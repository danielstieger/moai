"""Persistence description and the Java of the aggregate repository."""
from .bausteine import column, literal


def field(prop, col):
    return {"concept": "FieldMapping", "references": {"property": prop}, "children": {"fieldName": literal(col)}}


def atom(p):
    """The mapping of a specified property: field, embedded value object or reference."""
    col = p.get("spalte", column(p["name"]))
    if "felder" in p:
        return {"concept": "EmbeddedMapping", "references": {"property": p["name"]},
                "children": {"atomMpig": [field(k, v) for k, v in p["felder"].items()]}}
    if p.get("verweis"):
        return {"concept": "ReferenceMapping", "references": {"property": p["name"]},
                "children": {"keyMapping": field("id", p.get("spalte", column(p["name"]) + "_ID"))}}
    return field(p["name"], col)


def entity_mapping(name, ent, table, atoms):
    return {"concept": "EntityMapping", "properties": {"name": name}, "references": {"classConcept": ent},
            "children": {"tableName": literal(table), "tableOption": "OptimisticOption", "atomMpig": atoms}}


def repository_java(agg, var, positions):
    """get, checkout and checkin of the aggregate with its position lists."""
    m = "Map" + agg
    lines = []
    for meth, ro in (("get", "true"), ("checkout", "false")):
        lines.append(f"public {agg} {meth}(int id) {{")
        lines.append(f'  {agg} {var} = GET("{m}", id, {ro});')
        for pos in positions:
            pm, sort = "Map" + pos["entity"], pos["sort"]
            lines.append(f'  {var}.{pos["property"]} = WHERE("{pm}", {ro}, FIELD("{pm}", "{pos["key"]}") == id)'
                         f'.SORTBY(FIELD("{pm}", "{sort}"), true);')
        lines.append(f"  return {var};")
        lines.append("}")
    lines.append(f"public void checkin({agg} {var}) {{")
    lines.append(f'  SAVE("{m}", {var});')
    for pos in positions:
        lines.append(f'  for ({pos["entity"]} p : {var}.{pos["property"]}) {{')
        lines.append(f'    p.{pos["key"]} = {var}.id;')
        lines.append(f'    SAVE("Map{pos["entity"]}", p);')
        lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"
