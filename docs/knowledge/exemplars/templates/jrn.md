Jerry Resource Name (JRN)
============================
The Jerry Resource Name (JRN) is a standardized naming convention for uniquely identifying resources, actions, event types, and JSON schemas within the Jerry framework. It provides a clear and consistent way to reference various components across different domains and tenants.

Default Partition: `jer`.

What I would like to do in this version is introduce a URN/URI for each concept. Something following the scheme where rectangular brackets ([]) denote optional components, angle brackets/chevrons (<>) denote required component and the vertical bar (|) denotes logical disjunction (aka. OR):
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:[resource_type<:|/><resource_id>[+resource_version]

Canonical e.g.
jer+1:jer:339c4423-0ec4-4d41-9fe9-2eef9c7375bc:worktracker:eabdba39-b86e-44a9-8d72-45f585b90405+e575b531bd8197f3a1019c15ac8831dd92d082f4ce6e1a8ab92fcbefb23f154d

Omitted optional e.g.
jer:jer:339c4423-0ec4-4d41-9fe9-2eef9c7375bc:work-tracker:eabdba39-b86e-44a9-8d72-45f585b90405

We could also use this as the `$id` for JSON Schemas and as a way to represent event types.

Used to represent commands/actions:
jer[+scheme_version]:<partition>:[tenant_id]:{domain}:actions/{ActionName}

e.g.
jer:jer:work-tracker:CreateTask <-- Commands/Actions Owned by Jerry
jer:jer:victor-lau:work-tracker:CreateAlarm <-- Commands/Actions Owned by the Tenant (user) - allows for user expansion/modularity

Used to represent event types:
jer[+scheme_version]:<partition>:[tenant_id]:{domain}:facts/[path/]{ActionName}

e.g.
jer:jer:work-tracker:facts/TaskCreated <-- Event Type owned by Jerry
jer:jer:victor-lau:golf-tracker/facts/SwingLogged

Used to represent JSON Schemas:
jer[+scheme_version]:<partition>:[tenant_id]:{domain}:facts/[path/]{ActionName}[+resource_version]

e.g.
jer:jer:work-tracker:task:CreateTaskRequest+1.0.0 <-- Schema owned by Jerry
jer:jer:victor-lau:gold-tracker:task:LogSwingRequest+1.0.0 <-- Schema owned by Jerry
