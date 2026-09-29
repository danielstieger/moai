# Blueprint index

Except for the explicitly named `CustomContainers` skeleton, these are subtree templates rather than standalone roots. Replace every `$TARGET_*` reference in the destination model before a real write.

- [custom-containers-root-skeleton.json](blueprints/custom-containers-root-skeleton.json) — the language's specialized rootable registry, initially empty.
- [list-string-type-subtree.json](blueprints/list-string-type-subtree.json) — `list<string>` type node.
- [arraylist-string-creator-subtree.json](blueprints/arraylist-string-creator-subtree.json) — `new arraylist<string>` as a complete `GenericNewExpression`.
- [hashmap-string-creator-subtree.json](blueprints/hashmap-string-creator-subtree.json) — `new hashmap<string,string>` as a complete `GenericNewExpression`.
- [where-operation-subtree.json](blueprints/where-operation-subtree.json) — a complete `DotExpression` with a structurally valid inferred closure and neutral `true` predicate.
- [translate-operation-subtree.json](blueprints/translate-operation-subtree.json) — a `TranslateOperation`/`selectMany` chain whose closure yields its input item.
- [foreach-statement-skeleton.json](blueprints/foreach-statement-skeleton.json) — Collections foreach with an empty body.
- [map-element-subtree.json](blueprints/map-element-subtree.json) — `map["key"]` read expression.
- [list-element-access-subtree.json](blueprints/list-element-access-subtree.json) — `list[0]` read expression.

The templates intentionally use primitive BaseLanguage literals or clearly named destination placeholders. They contain no project path or application-project reference.

