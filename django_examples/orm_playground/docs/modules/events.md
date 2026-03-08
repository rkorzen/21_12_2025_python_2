# Events

- `EventLog` z `GenericForeignKey`
- pseudo-join `EventLog.actor_email` ↔ `Person.email`
- `EventLogQuerySet.with_actor_match()`
