import io
import unittest
from backlog import snapshot


def report(rows, day="2026-11-27"):
    return snapshot(io.StringIO("ticket,queue,opened,closed\n" + rows), day)


class BacklogTests(unittest.TestCase):
    def test_boundaries(self):
        rows = "1,B,2026-11-27,\n2,A,2026-11-25,2026-11-28\n3,A,2026-11-26,2026-11-27\n4,A,2026-11-28,\n5,A,2026-11-26,\n"
        self.assertEqual(report(rows), [("A", 2, 2), ("B", 1, 0)])

    def test_invalid_records(self):
        for row in ["1,A,2026-02-30,", "1,A,2026-11-20,2026-11-19", "1,,2026-11-20,", "1,A"]:
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, "line 2"):
                report(row)

    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "line 3"):
            report("1,A,2026-11-20,\n" * 2)

    def test_empty_snapshot(self):
        self.assertEqual(report(""), [])

    def test_bad_header(self):
        with self.assertRaisesRegex(ValueError, "header"):
            snapshot(io.StringIO("id\n"), "2026-11-27")
