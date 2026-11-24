"""표준 라이브러리만으로 판정, 최소 폐포, 동치류, 입력 동작을 검증한다."""
import itertools
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import relation as r


def pairs(m):
    return {(i, j) for i, row in enumerate(m) for j, v in enumerate(row) if v}


def matrix(rows):
    return [[int(v) for v in row] for row in rows.split()]


class RelationTests(unittest.TestCase):
    def test_all_three_element_relations(self):
        # 원소 3개 위의 관계 512개에 대해 집합식으로 독립적인 정답을 만든다.
        n = 3
        identity = {(i, i) for i in range(n)}
        for bits in itertools.product((0, 1), repeat=n*n):
            m = [list(bits[i:i+n]) for i in range(0, n*n, n)]
            original = pairs(m)
            reverse = {(j, i) for i, j in original}
            two_steps = {(i, j) for i, k in original for h, j in original if k == h}
            reach = set(original)
            while True:
                longer = reach | {(i,j) for i,k in reach for h,j in original if k == h}
                if longer == reach:
                    break
                reach = longer
            self.assertEqual(r.is_reflexive(m), identity <= original)
            self.assertEqual(r.is_symmetric(m), original == reverse)
            self.assertEqual(r.is_transitive(m), two_steps <= original)
            self.assertEqual(pairs(r.reflexive_closure(m)), original | identity)
            self.assertEqual(pairs(r.symmetric_closure(m)), original | reverse)
            self.assertEqual(pairs(r.transitive_closure(m)), reach)
            self.assertEqual(pairs(m), original)

    def test_lecture_classes(self):
        m = matrix("10001 01100 01100 00010 10001")
        self.assertEqual([r.equivalence_class(m, a) for a in range(1, 6)],
                         [[1,5], [2,3], [2,3], [4], [1,5]])

    def test_chain_and_isolated_vertex(self):
        m = matrix("01000 00100 00010 00000 00000")
        t = r.transitive_closure(m)
        self.assertEqual(r.added_pairs(m, t), [(1,3), (1,4), (2,4)])
        eq = r.transitive_closure(r.symmetric_closure(r.reflexive_closure(m)))
        self.assertEqual(eq, matrix("11110 11110 11110 11110 00001"))

    def test_input_retries_and_output(self):
        rows = ["0 0", "0 1 2 0 1", "1 0 0 0 1", "0 1 1 0 0",
                "0 1 1 0 0", "0 0 0 1 0", "1 0 0 0 1"]
        out = StringIO()
        with patch("builtins.input", side_effect=rows), redirect_stdout(out):
            r.main()
        self.assertEqual(out.getvalue().count("입력 오류"), 2)
        self.assertIn("[5] = {1, 5}", out.getvalue())
        self.assertNotIn("폐포", out.getvalue())


if __name__ == "__main__":
    unittest.main()
