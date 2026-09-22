# DataUX workflows

## Inspect an existing PagePane

1. Resolve the intended project with `mps_mcp_list_open_projects`.
2. Locate the `PagePane` root through a scoped project-structure query or `FIND_INSTANCES` for `org.modellwerkstatt.dataux.structure.PagePane`.
3. Print the root in `PLAIN TEXT` to understand the editor-visible binding and layout.
4. Print only the relevant root/subtree in deep JSON when a reusable shape is required.
5. Resolve the bound classifier/property targets and the corresponding ObjectFlow Command/Page.
6. Trace nested bindable elements. Record where the binding switches from a parent object to a list row or referenced object.

## Create a PagePane

1. Load `mps-node-editing`; load `objectflow-dsl` when creating or changing the corresponding Command/Page or bound declarations.
2. Resolve the target model, bound classifier, optional bound property, and any commands used by menus.
3. Choose the smallest top-level element that fits the UI:
   - `DelegateForm` for one selected object,
   - `Table` for a list,
   - `GridLayout` for master/detail or multi-panel UI,
   - `TabLayout` for tabbed UI.
4. Start from `page-pane-form-skeleton.json`, replace placeholders, and dry-run the root.
5. Insert the root. Add delegates and options incrementally; use focused samples for their exact shapes.
6. Add menus only after the selection context and Command parameters are clear.
7. Validate the root. Test single-object, multi-object, and empty-selection cases in the consuming flow.

## Add a Table to a master/detail PagePane

1. Identify the selected parent type and its list property.
2. Resolve the list-property declaration node and its element type.
3. Add a `Table` under a layout `uxChild` role.
4. Bind the table to the parent classifier/property pair and set the table's row classifier if the inherited binding is insufficient.
5. Add type-compatible delegates as columns.
6. Bind dependent forms to the table's row type so they follow the shared selection.
7. Verify that an empty row selection produces the intended empty detail state.

## Create an AppUiModule

1. Resolve the ObjectFlow configuration, Commands, labels, and any configured components.
2. Start from `app-ui-module-skeleton.json`; replace the module name and authentication result.
3. Add configuration, version, and official-name metadata.
4. Add lifecycle statements and an optional startup command only when required.
5. Add menu actions and tiles incrementally. Supply all required Command arguments from module parameters/variables or suitable expressions.
6. Validate, make/generate the solution, and test application startup and shutdown.

## Create a BatchJobModule

1. Load `objectflow-dsl` and resolve the configuration, exception strategy shape, and producer/consumer pairs.
2. Inspect `PrintingJob` or the closest live batch example rather than guessing ObjectFlow child shapes.
3. Create the batch root skeleton with required authentication and exception strategy.
4. Add pairs, then attach pair-specific CRON, delay, and consumer-count options with explicit references.
5. Decide whether the module runs console-only or is included in an application UI.
6. Validate, make/generate, and exercise the trigger plus exception behavior.

## Editing policy

- Use `mps_mcp_update_node` for property, reference, and focused child changes.
- Use a full-root update only when intentionally replacing the entire shape and after preserving the root ID.
- For large roots, insert the skeleton first, then attach one layout/menu/pair subtree at a time.
- Validate after each meaningful structural step so a broken binding or missing required role is localized.

