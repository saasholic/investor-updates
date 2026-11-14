import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.check_zip_parity import check_parity, main, rebuild_zip


class CheckZipParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.skill_dir = self.root / "investor-updates"
        self.skill_dir.mkdir()
        (self.skill_dir / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
        (self.skill_dir / "references").mkdir()
        (self.skill_dir / "references" / "guide.md").write_text("Guide\n", encoding="utf-8")
        self.zip_path = self.root / "investor-updates.zip"
        rebuild_zip(self.skill_dir, self.zip_path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_default_check_passes_after_deterministic_rebuild(self) -> None:
        first_bytes = self.zip_path.read_bytes()
        rebuild_zip(self.skill_dir, self.zip_path)
        second_bytes = self.zip_path.read_bytes()
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(
            main(["--skill-dir", str(self.skill_dir), "--zip", str(self.zip_path)]),
            0,
        )

    def test_detects_modified_file(self) -> None:
        (self.skill_dir / "SKILL.md").write_text("# Modified\n", encoding="utf-8")
        errors = check_parity(self.skill_dir, self.zip_path)
        self.assertTrue(any("Byte mismatch" in err for err in errors), errors)
        self.assertEqual(
            main(["--check", "--skill-dir", str(self.skill_dir), "--zip", str(self.zip_path)]),
            1,
        )

    def test_detects_missing_and_stale_entries(self) -> None:
        (self.skill_dir / "new.md").write_text("New\n", encoding="utf-8")
        errors = check_parity(self.skill_dir, self.zip_path)
        self.assertTrue(any("Missing from" in err for err in errors), errors)

        shutil.rmtree(self.skill_dir / "references")
        (self.skill_dir / "new.md").unlink()
        errors_stale = check_parity(self.skill_dir, self.zip_path)
        self.assertTrue(any("Stale/extra entry" in err for err in errors_stale), errors_stale)

    def test_detects_outside_prefix_entry(self) -> None:
        with zipfile.ZipFile(self.zip_path, "a") as zf:
            zf.writestr("other/file.txt", "bad")
        errors = check_parity(self.skill_dir, self.zip_path)
        self.assertTrue(any("outside" in err for err in errors), errors)


if __name__ == "__main__":
    unittest.main()
