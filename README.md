# Queue backlog snapshot

Use a ticket export to reconstruct the end-of-day backlog for each service queue. The report counts open tickets and shows the age in calendar days of the oldest one.

## Run locally

Use Python 3.10+ with its standard SQLite module. Clone or download this repository and run from its root. No packages or account setup are required.

```sh
python backlog.py examples/tickets.csv 2026-11-27
python -m unittest discover -s tests -v
```

The example prints:

```csv
queue,open_tickets,oldest_days
Billing,2,7
Support,1,0
```

Supply a UTF-8 CSV with the exact header shown in examples/tickets.csv. Keep one row per ticket. Use YYYY-MM-DD calendar dates and leave closed blank for active tickets. Opening day counts as age zero. A ticket closed on the cutoff day is already closed at day end. Queues with zero open tickets are omitted. Queue assignment is assumed constant over the ticket lifetime. Use one business timezone when preparing your export.

Rows load into a temporary in-memory SQLite database. Duplicate IDs and malformed records stop the report before it writes results. Redirect stdout to save a CSV. See faq.md for supported scenarios.
