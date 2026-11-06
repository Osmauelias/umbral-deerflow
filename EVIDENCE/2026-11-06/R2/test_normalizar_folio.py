"""Automated tests for normalizar_folio."""

import unittest

from normalizar_folio import normalizar_folio


class NormalizarFolioTests(unittest.TestCase):
    def test_adds_prefix_and_trims_outer_spaces(self):
        self.assertEqual(normalizar_folio(" 123 "), "UMB-123")

    def test_uppercases_existing_prefix_and_preserves_zeroes(self):
        self.assertEqual(normalizar_folio("umb-00123"), "UMB-00123")

    def test_preserves_zeroes_for_unprefixed_number(self):
        self.assertEqual(normalizar_folio(" 0007 "), "UMB-0007")

    def test_rejects_internal_spaces_letters_and_extra_signs(self):
        invalid_values = ("UMB- 12", "abc", "UMB-12x", "UMB--12", "+12")
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalizar_folio(value)

    def test_rejects_empty_or_whitespace_only_input(self):
        for value in ("", "   "):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalizar_folio(value)


if __name__ == "__main__":
    unittest.main()
