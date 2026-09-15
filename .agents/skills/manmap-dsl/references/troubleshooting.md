# Diagnose: nicht geladene Referenz

Der wichtigste ManMap-Laufzeitfehler ist `org.modellwerkstatt.objectflow.runtime.OFXNotInitializedException` beim Zugriff auf ein Referenz-Property einer geladenen ObjectFlow-Entität. Eine vorhandene `ReferenceMapping` beschreibt die mögliche Beziehung, lädt das Zielobjekt aber nicht selbst.

1. Identifiziere das konkrete Referenz-Property und seine `ReferenceMapping` im `EntityMapping` der Quell-Entität. Folge den persistenten Referenzen, nicht nur gleichen Namen.
2. Finde die `QueryFromMap`, die diese Instanz geliefert hat. Prüfe ihre `joinOption`-Kinder.
3. Für die betreffende Referenz muss eine `RefJoinOption` mit `refMapping` auf genau diese `ReferenceMapping` und `entityMapping` auf das Ziel-Mapping vorhanden sein. Die [kompakte JSON-Form](blueprints/query-from-map-ref-join-subtree.json) zeigt beide Links.
4. Fehlt die Option, ergänze sie an der tatsächlich verwendeten Query. Prüfe danach den geänderten Repository-Root mit `mps_mcp_check_root_node_problems` und generiere die betroffene Solution. Ist die Option vorhanden, prüfe, ob die Entity-Instanz wirklich aus dieser Query stammt und ob die Links auf die beabsichtigten Mapping-Knoten zeigen.

Eine nicht explizit geladene Liste zeigt dagegen `size == 0` und wirft beim Zugriff keine `OFXNotInitializedException`. Siehe [Referenzen und Listen laden](loading.md).
