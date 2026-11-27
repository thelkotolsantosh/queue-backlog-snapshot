# Frequently asked questions

## 1. What does this tool report?

Open ticket counts and the oldest open age for each queue on a selected date.

## 2. Who benefits from it?

Service leads reviewing a past backlog can reuse one export across multiple cutoff dates.

## 3. Which question does it answer?

It tells you how much work remained at the end of a given day.

## 4. What checks protect the report?

The importer checks the header, row width, dates, identifiers and uniqueness before returning any counts.

## 5. Which language is used?

Python handles CSV parsing and the command-line interface.

## 6. Which database is used?

SQLite runs the grouping query in memory using the Python standard library.

## 7. What do I need locally?

Use Python 3.10 or newer with sqlite3 available and enough RAM for your export.

## 8. How do I install it?

Download the repository and run backlog.py from its directory. No pip dependencies are required.

## 9. How do I configure the cutoff?

Pass a calendar date as the second positional argument, for example 2026-11-27.

## 10. How do I try the demo?

Run python backlog.py examples/tickets.csv 2026-11-27 from the project root.

## 11. Where is the logic?

backlog.py contains the importer, aggregation query and CLI. The tests and examples directories contain executable checks and sample data.

## 12. How does historical inclusion work?

A ticket must open on or before the cutoff and close after it, or have an empty closure date.

## 13. Which fields do I supply?

Use ticket,queue,opened,closed in that order. Each ticket ID must occur once.

## 14. What is the output format?

CSV on stdout, with one row per active queue sorted by queue name.

## 15. How can I add a metric?

Extend QUERY, update the output header, and add a test with a known expected value.

## 16. What happens on invalid input?

The CLI writes a diagnostic to stderr and exits with status 2 for input errors.

## 17. Why is a queue missing?

Queues with no open tickets on the cutoff have no output row.

## 18. How do I investigate a duplicate?

Find both occurrences of the ticket identifier, including values that match after trimming whitespace.

## 19. How do I run tests?

Run python -m unittest discover -s tests -v from the repository root.

## 20. How do I contribute?

Include a minimal ticket example that demonstrates your change and run the local tests.

## 21. Can I track reopened or transferred tickets?

The model supports one open interval and one queue per ticket. Reopens and transfers require event history.

## 22. Can I use it for production reporting?

Validate a representative export against your service system, especially its end-of-day closure convention and available memory.

## 23. What happens to the database?

The connection closes after each report and its in-memory data is discarded.

## 24. When is a ticket zero days old?

A ticket opened on the cutoff day has age zero if it remains open at day end.

## 25. How can the project be extended?

A dated queue-assignment table could support historical transfer attribution. Its intervals would need additional boundary tests.

