# DataUX gotchas

- **Binding is not loading.** A `boundProperty` selects already available data; it does not initialize an ObjectFlow reference or list.
- **Selection is per type and PagePane.** Two tables with the same row type share the same selected object even when their row sets differ.
- **An empty selection is valid.** A bound form then shows no object. Menu actions and expressions must not assume a selection exists.
- **Parent type and row type differ.** A table can be bound through `Parent.children` while its delegates and selection operate on `Child`.
- **Includes do not create a new binding universe.** An included bindable element participates in the enclosing context and may require compatible or overridden binding.
- **Rootable does not mean top-level-only.** `DelegateForm`, `Table`, `GridLayout`, `TabLayout`, and `CustomElement` are rootable but are also commonly nested under `PagePane` or layouts.
- **PagePane has one top-level UI child.** Use a layout to host several sibling components.
- **Delegate type must match the property.** Copying a `StringDelegate` shape for a status, reference, or date property produces type/constraint problems.
- **Reference formats matter.** `boundClassifier`, `boundProperty`, commands, labels, configurations, and pair options require persistent declaration node refs (`r:...`), not `c:` concept refs.
- **Menu actions inherit context.** Actual Command arguments must be valid where the menu lives; table actions often need the selected row rather than the PagePane's parent object.
- **BaseLanguage scope is local.** Expressions valid in a delegate-color function are not automatically valid in a module lifecycle or tile expression.
- **Batch options can be pair-specific.** `OptCronPairExp`, `OptDelayPair`, and `OptNumConsumersPair` require the intended pair reference.
- **Batch auth may be UI-dependent.** The `simpleone` projection notes that authentication/user-environment adjustment runs when UI is present; do not assume it is the batch processor's sole security boundary.
- **Device layout is explicit.** Desktop and mobile/MDE interfaces may need separate PagePanes and even separate application roots.
- **API concepts are out of scope here.** `ApiDescription` and its endpoint/operation family have not yet been documented or templated.

