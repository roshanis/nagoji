"""Tests for scan_slop.py (stdlib unittest only).

Run from anywhere:
    python3 book1_horse_servant_2e/audit/tools/test_scan_slop.py

Every fixture is inline so the tests never depend on the manuscript.
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scan_slop as ss  # noqa: E402


def chapter(body, number=1, title="Test"):
    """Parse a tiny chapter made of the given body text."""
    text = "# Chapter %d: %s\n\n%s\n" % (number, title, body)
    return ss.parse_chapter(text, name="book1_chapter%02d_test.md" % number)


def hits(body, key):
    """Number of hits for one marker in a one-chapter fixture."""
    return len(ss.count_markers(chapter(body))[key])


class TestParsing(unittest.TestCase):
    def test_html_comments_are_skipped(self):
        ch = chapter("<!-- editor note\nstill a note -->\n\nReal text here.\n\n<!-- one line -->")
        self.assertEqual([p.text for p in ch.paragraphs], ["Real text here."])

    def test_heading_images_and_rules_are_not_prose(self):
        ch = chapter("![Map](map.jpg)\n\nOne two three.\n\n---\n\nFour five.")
        self.assertEqual(ch.number, 1)
        self.assertEqual(ch.label, "Ch01")
        self.assertEqual(ch.title, "Test")
        self.assertEqual([p.text for p in ch.paragraphs], ["One two three.", "Four five."])
        self.assertEqual(ch.words, 5)

    def test_line_numbers_point_at_source_lines(self):
        ch = chapter("First para.\n\nSecond para.")
        # line 1 heading, 2 blank, 3 first para, 4 blank, 5 second para
        self.assertEqual([p.line for p in ch.paragraphs], [3, 5])

    def test_multiline_paragraph_joins_and_maps_lines(self):
        ch = chapter("One line here.\nSecond line here.")
        self.assertEqual(len(ch.paragraphs), 1)
        sents = ch.paragraphs[0].sentences
        self.assertEqual([s.line for s in sents], [3, 4])

    def test_emphasis_markers_are_stripped(self):
        ch = chapter("He rode with *huzurat* cavalry and **no** fear.")
        self.assertEqual(ch.paragraphs[0].text, "He rode with huzurat cavalry and no fear.")

    def test_chapter_number_from_filename_when_no_heading(self):
        ch = ss.parse_chapter("Just prose.\n", name="book2_chapter08_estate.md")
        self.assertEqual(ch.number, 8)
        self.assertEqual(ch.label, "Ch08")

    def test_sentence_split_keeps_dialogue_tags_together(self):
        ch = chapter("\u201cHow long?\u201d he asked. \u201cTwo days.\u201d She left. No. It ended.")
        texts = [s.text for s in ch.paragraphs[0].sentences]
        self.assertEqual(texts, ["\u201cHow long?\u201d he asked.", "\u201cTwo days.\u201d",
                                 "She left.", "No.", "It ended."])

    def test_quote_mask_curly_and_straight(self):
        mask = ss.quote_mask('a \u201cb\u201d c "d" e')
        inside = "".join(ch for ch, m in zip('a \u201cb\u201d c "d" e', mask) if m)
        self.assertIn("b", inside)
        self.assertIn("d", inside)
        self.assertNotIn("a", inside)
        self.assertNotIn("e", inside)

    def test_narration_flag(self):
        ch = chapter("\u201cGo,\u201d he said. I went.")
        s1, s2 = ch.paragraphs[0].sentences
        self.assertFalse(s1.narration)
        self.assertTrue(s2.narration)
        self.assertTrue(ch.paragraphs[0].has_dialogue)

    def test_tokenize(self):
        self.assertEqual(ss.tokenize("Jo\u00e3o's twenty-five men, in 1738."),
                         ["jo\u00e3o's", "twenty-five", "men", "in", "1738"])


class TestCoreMarkers(unittest.TestCase):
    CASES = [
        # (marker, text, expected count)
        ("not_but", "It was not fear but calculation.", 1),
        ("not_but", "Not in threat, but in promise.", 1),
        ("not_but", "Not for the stake, not for the scaffold, but for transport.", 1),
        ("not_but", "I could not hear the words, but I saw his face.", 0),
        ("not_but", "He did not answer, but he smiled.", 0),
        ("not_but", "It was not fear. But calculation came later.", 0),
        ("not_but", "It was not a place that I had ever wanted to see again in my life, but I went.", 0),
        ("not_but", "His voice had not yet broken, but it carried clearly.", 0),
        ("not_but", "She was not young, but no one would call her old.", 0),
        ("not_but", "He was not a large man, but he was quick.", 0),
        ("not_but", "I took him alive, not out of mercy, but because we needed prisoners.", 1),
        ("not_opener", "Not yet. The gate held.", 1),
        ("not_opener", "\u201cNot now,\u201d he said.", 1),
        ("not_opener", "Not in threat, but in promise.", 0),
        ("not_opener", "Nothing moved. Notice was given.", 0),
        ("comma_not", "He came for the pepper, not the people.", 1),
        ("comma_not", "I asked him, not knowing why.", 0),
        ("comma_not", "Not for the stake, not for the scaffold, but for transport.", 0),
        ("comma_not", "It was a village, not yet a town.", 0),
        ("comma_not", "I took him alive, not out of mercy, but because we needed prisoners.", 0),
        ("comma_not", "No bodies, not that I could see. No one, not even the Company, came.", 0),
        ("as_if", "The sea moved as if it breathed. As if it knew.", 2),
        ("as_if", "He has if nothing else a horse.", 0),
        ("as_though", "It moved as though alive.", 1),
        ("like_a", "He moved like a tiger and struck like the hand of God, like an omen.", 3),
        ("like_a", "Like a hawk, he watched.", 1),
        ("like_a", "I would like the rice. He did not like the look of it.", 0),
        ("like_a", "Unlike the others, he was likely the first.", 0),
        ("soft_adverbs", "He rode slowly, spoke quietly, sang softly and packed carefully.", 4),
        ("soft_adverbs", "The slow horse was quiet.", 0),
        ("weight_of", "I felt the weight of years. A weight of iron.", 1),
        ("something_x", "Something older stirred, something deeper, something else.", 3),
        ("something_x", "Something moved.", 0),
        ("first_time", "For the first time I smiled. The first time I saw him.", 1),
        ("etched", "Lines were etched in his face. Etching was an art. He fetched water.", 2),
        ("somehow", "Somehow he knew.", 1),
        ("in_that_moment", "In that moment I knew. In this instant he fell. In a moment he left.", 2),
        ("sense_of", "I had a sense of dread. The sense of it escaped me.", 1),
        ("triad", "Horses. Guns. Storms.", 1),
        ("triad", "I decided belief did not matter. Numbers did. Chains did. Ships did.", 1),
        ("triad", "Horses. Guns. Storms. Salt.", 1),
        ("triad", "Horses. Guns.", 0),
        ("triad", "\u201cYes. No. Maybe.\u201d", 0),
        ("one_sentence_para", "Storms do not ask permission.", 1),
        ("one_sentence_para", "\u201cBring him,\u201d Father Duarte said.", 0),
        ("one_sentence_para", "He rode out. He came back.", 0),
        ("short_para_final", "He walked to the gate and looked out over the long road. Nothing moved.", 1),
        ("short_para_final", "He walked to the gate. Then he looked out over the long road to the south.", 0),
        ("short_para_final", "Short one.", 0),
        ("short_para_final", "\u201cWe ride at dawn and we do not stop,\u201d he said. I nodded.", 0),
        ("rhetorical_q", "Did I believe in anything? I did not know.", 1),
        ("rhetorical_q", "\u201cDid you?\u201d he asked.", 0),
        ("rhetorical_q", "\u201cWhere?\u201d I asked. What else could I ask?", 1),
    ]

    def test_cases(self):
        for key, text, expected in self.CASES:
            with self.subTest(key=key, text=text):
                self.assertEqual(hits(text, key), expected)

    def test_every_core_marker_has_a_case(self):
        covered = {key for key, _, _ in self.CASES}
        self.assertEqual(covered, {m.key for m in ss.CORE_MARKERS})

    def test_hit_records_location_and_dialogue_flag(self):
        ch = chapter("Plain line.\n\n\u201cIt was not fear, but sense,\u201d he said.")
        hit = ss.count_markers(ch)["not_but"][0]
        self.assertEqual(hit.chapter, "Ch01")
        self.assertEqual(hit.line, 5)
        self.assertTrue(hit.dialogue)
        self.assertIn("not fear, but", hit.snippet)

    def test_marker_counts_are_per_chapter_and_rate_per_1000(self):
        ch = chapter("As if one. As if two. " + "word " * 96)
        rows = ss.chapter_marker_table([ch])
        self.assertEqual(rows[0]["counts"]["as_if"], 2)
        self.assertAlmostEqual(rows[0]["rates"]["as_if"], 2 * 1000.0 / ch.words)


class TestExtendedMarkers(unittest.TestCase):
    CASES = [
        ("fragment", "Together. He rode out across the long plain.", 1),
        ("fragment", "Only the sea. Fresh men. Blue coats.", 3),
        ("fragment", "I nodded. Ships did. Movement meant chances. The sacred grove.", 1),
        ("kind_of", "He was the sort of man who smiled. A kind of peace.", 2),
        ("stock_atmosphere", "Smoke hung in the air, thick with ash, a chill that had nothing to do with the wind.", 3),
        ("gently_silently", "He spoke gently and left silently.", 2),
        ("somewhere", "Somewhere a dog barked.", 1),
        ("perhaps", "Perhaps he knew.", 1),
        ("nodded", "He nodded. She nodded once.", 2),
        ("jaw", "His jaw tightened. Her jaw set.", 2),
        ("eyes_verb", "His eyes narrowed. Her gaze moved to me.", 2),
        ("appraising", "He studied me. She was measuring him.", 2),
        ("long_moment", "For a long moment nobody spoke.", 1),
        ("said_nothing", "I said nothing. He did not answer.", 2),
        ("something_in", "There was something in his eyes.", 1),
        ("noticing", "I saw the way he held the reins.", 1),
        ("lesson", "I learned that fear lies. That was the lesson.", 2),
        ("provisional_close", "For now, that was enough.", 2),
        ("modern_register", "Risk assessment: HIGH. Leverage: significant. She navigated the court.", 3),
        ("modern_register", "The procession moved on. He processed nothing.", 1),
    ]

    def test_cases(self):
        for key, text, expected in self.CASES:
            with self.subTest(key=key, text=text):
                self.assertEqual(hits(text, key), expected)

    def test_every_extended_marker_has_a_case(self):
        covered = {key for key, _, _ in self.CASES}
        self.assertEqual(covered, {m.key for m in ss.EXTENDED_MARKERS})


class TestRepeatedNgrams(unittest.TestCase):
    def make(self, bodies):
        return [chapter(b, number=i + 1) for i, b in enumerate(bodies)]

    def test_cross_chapter_phrase_reported_once_at_maximal_length(self):
        chs = self.make([
            "The river ran cold and deep beneath the old stone bridge.",
            "Far away, the river ran cold and deep beneath the hills.",
        ])
        reps = ss.repeated_ngrams(chs)
        self.assertEqual(len(reps), 1)
        self.assertEqual(reps[0].phrase, "the river ran cold and deep beneath the")
        self.assertEqual(sorted(reps[0].chapters), ["Ch01", "Ch02"])
        self.assertEqual([o[1] for o in reps[0].occurrences], [3, 3])

    def test_three_times_in_one_chapter_counts_twice_does_not(self):
        three = self.make(["Salt dried on the black rope. " * 3])
        two = self.make(["Salt dried on the black rope. " * 2])
        self.assertEqual([r.phrase for r in ss.repeated_ngrams(three)],
                         ["salt dried on the black rope"])
        self.assertEqual(ss.repeated_ngrams(two), [])

    def test_ngrams_do_not_cross_sentences(self):
        chs = self.make(["Salt dried on. The black rope burned.",
                         "Salt dried on. The black rope burned."])
        self.assertEqual(ss.repeated_ngrams(chs), [])

    def test_names_break_phrases(self):
        chs = self.make([
            "Then Eustachius de Lannoy rode past the old wooden gate at dusk. Lannoy smiled.",
            "Later Eustachius de Lannoy rode past the old wooden gate at noon. Eustachius waved.",
        ])
        names = ss.detect_names(chs)
        self.assertIn("lannoy", names)
        self.assertIn("eustachius", names)
        phrases = [r.phrase for r in ss.repeated_ngrams(chs, names=names)]
        self.assertEqual(phrases, ["rode past the old wooden gate at"])

    def test_extra_names_can_be_supplied(self):
        chs = self.make(["We saw the red pepper boats at dawn.",
                         "They saw the red pepper boats at night."])
        self.assertEqual(len(ss.repeated_ngrams(chs)), 1)
        self.assertEqual(ss.repeated_ngrams(chs, names={"pepper"}), [])

    def test_function_word_only_phrases_are_dropped(self):
        chs = self.make(["It was as if it were so.", "It was as if it were so."])
        self.assertEqual(ss.repeated_ngrams(chs), [])

    def test_headings_are_excluded(self):
        chs = [ss.parse_chapter("# The river ran cold and deep\n\nNothing here.\n", name="a_chapter01.md"),
               ss.parse_chapter("# The river ran cold and deep\n\nOther words.\n", name="a_chapter02.md")]
        self.assertEqual(ss.repeated_ngrams(chs), [])

    def test_long_repeat_extends_past_ten_words(self):
        line = "the old horse walked slowly down the long red road toward the distant salt marsh"
        chs = self.make([line.capitalize() + ".", "Then " + line + "."])
        reps = ss.repeated_ngrams(chs)
        self.assertEqual(len(reps), 1)
        self.assertEqual(reps[0].phrase, line)
        self.assertEqual(reps[0].length, 15)

    def test_detect_names_ignores_sentence_initial_words(self):
        chs = self.make(["Storms came. The storms passed. Ramayyan spoke to Ramayyan's men."])
        names = ss.detect_names(chs)
        self.assertNotIn("storms", names)
        self.assertNotIn("the", names)
        self.assertIn("ramayyan", names)


class TestImagesAndSimiles(unittest.TestCase):
    def test_family_counts_and_figurative_flag(self):
        ch = chapter("The storm came. Arrows fell like a storm of hail.")
        fams = {f["family"]: f for f in ss.image_report([ch])}
        self.assertEqual(fams["storm"]["total"], 2)
        self.assertEqual(len(fams["storm"]["figurative"]), 1)

    def test_of_construction_is_figurative(self):
        ch = chapter("A tide of men poured in.")
        fams = {f["family"]: f for f in ss.image_report([ch])}
        self.assertEqual(len(fams["tide"]["figurative"]), 1)

    def test_simile_vehicle_grouped_across_chapters(self):
        chs = [chapter("He moved like a hawk.", number=1),
               chapter("She watched like a hawk circling.", number=2)]
        vehicles = ss.simile_vehicles(chs)
        self.assertIn("hawk", vehicles)
        self.assertEqual(len(vehicles["hawk"]), 2)

    def test_as_if_continuations(self):
        chs = [chapter("He paused as if weighing me.", number=1),
               chapter("She looked up as if weighing the words.", number=2)]
        conts = ss.as_if_continuations(chs)
        self.assertEqual(len(conts["weighing"]), 2)


class TestRhythmAndTypography(unittest.TestCase):
    def test_sentence_stats(self):
        ch = chapter("One two three. One two three four five.\n\nSix seven eight nine.")
        st = ss.sentence_stats(ch)
        self.assertEqual(st["sentences"], 3)
        self.assertAlmostEqual(st["mean"], 4.0)
        self.assertAlmostEqual(st["stdev"], 1.0)
        self.assertEqual(st["paragraphs"], 2)
        self.assertAlmostEqual(st["one_sentence_share"], 50.0)
        self.assertEqual(st["standalone_one"], 1)

    def test_standalone_one_liners_exclude_speech_beats(self):
        ch = chapter("\u201cGo,\u201d he said.\n\nI went.\n\n\u201cGood,\u201d he said.")
        self.assertEqual(ss.sentence_stats(ch)["standalone_one"], 0)
        self.assertEqual(len(ss.count_markers(ch)["one_sentence_para"]), 1)

    def test_typography_counts(self):
        text = ("# Title\n\nHe came \u2014 then left \u2014 fast. Wait " + "-" * 2 + " no.\n\n---\n\n"
                "| a | b |\n|---|---|\n\u201cHi,\u201d he said. \"Yo.\" It\u2019s done, isn't it.\n")
        t = ss.typography(text)
        self.assertEqual(t["em_dash"], 2)
        self.assertEqual(t["double_hyphen"], 1)
        self.assertEqual(t["curly_double"], 2)
        self.assertEqual(t["straight_double"], 2)
        self.assertEqual(t["curly_apostrophe"], 1)
        self.assertEqual(t["straight_apostrophe"], 1)


class TestEndingsAndSentences(unittest.TestCase):
    def test_ending_flags(self):
        ch = chapter("A long paragraph of plain narration sits here for a while.\n\nFor now, that was enough.")
        row = ss.chapter_endings([ch])[0]
        self.assertIn("opens 'For now'", row["flags"])
        self.assertIn("one-sentence", row["flags"])
        self.assertIn("summary word", row["flags"])

    def test_repeated_whole_sentences(self):
        chs = [chapter("He nodded. The horse ran. Ramayyan.", number=1),
               chapter("Rain fell. He nodded. Ramayyan.", number=2)]
        reps = ss.repeated_sentences(chs, names={"ramayyan"})
        self.assertEqual([r["sentence"] for r in reps], ["he nodded"])
        self.assertEqual(len(reps[0]["locations"]), 2)

    def test_ending_echoes_merge_plurals(self):
        chs = [chapter("Storms do not ask permission.", number=1),
               chapter("The storm was here.", number=2),
               chapter("Another storm came.", number=3)]
        echoes = dict(ss.ending_echoes(chs, names=set()))
        self.assertEqual(echoes["storm"], ["Ch01", "Ch02", "Ch03"])


class TestHotSpots(unittest.TestCase):
    def test_paragraph_with_most_hits_comes_first(self):
        ch = chapter("It rose slowly.\n\nSomehow, as if etched in that moment, it rose slowly.\n\nThe plain text stayed here.")
        spots = ss.hot_spots([ch])
        self.assertEqual(spots[0]["location"], "Ch01:5")
        self.assertEqual(spots[0]["hits"], 5)
        self.assertIn("somehow", spots[0]["markers"])
        self.assertEqual(spots[1]["location"], "Ch01:3")
        self.assertEqual(len(spots), 2)


class TestRankingAndCli(unittest.TestCase):
    def test_single_rare_hit_does_not_hit_the_cap(self):
        rare = chapter("Somehow it rose. " + "plain words here " * 30, number=1)
        others = [chapter("plain words here " * 31, number=n) for n in range(2, 6)]
        ranking = {x["label"]: x for x in ss.density_ranking([rare] + others)}
        # unsmoothed, one 'somehow' would hit the 3x cap and push the index to 2.0
        self.assertLess(ranking["Ch01"]["index"], 1.5)
        self.assertGreater(ranking["Ch01"]["index"], ranking["Ch02"]["index"])

    def test_density_ranking_orders_by_index(self):
        dense = chapter("Somehow, as if etched, slowly. " + "plain words here " * 10, number=1)
        clean = chapter("plain words here " * 12, number=2)
        ranking = ss.density_ranking([dense, clean])
        self.assertEqual(ranking[0]["label"], "Ch01")
        self.assertGreater(ranking[0]["index"], ranking[1]["index"])
        self.assertGreater(ranking[0]["per_1000"], ranking[1]["per_1000"])

    def write(self, folder, number, body):
        path = os.path.join(folder, "book1_chapter%02d_x.md" % number)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# Chapter %d: X\n\n%s\n" % (number, body))

    def run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ss.main(argv)
        return code, buf.getvalue()

    def test_cli_prints_markdown_report(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, 1, "The river ran cold and deep beneath the bridge. Somehow it rose.")
            self.write(d, 2, "Again the river ran cold and deep beneath the hill.")
            code, out = self.run_main([d])
        self.assertEqual(code, 0)
        self.assertIn("Density ranking", out)
        self.assertIn("the river ran cold and deep beneath the", out)
        self.assertIn("Ch01", out)
        self.assertNotIn("\u2014", out)

    def test_cli_hits_and_glob(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, 1, "It moved as if alive.")
            self.write(d, 2, "Nothing here.")
            code, out = self.run_main([d, "--glob", "*chapter01*", "--hits", "as_if"])
        self.assertEqual(code, 0)
        self.assertIn("Ch01:3", out)
        self.assertNotIn("Ch02", out)

    def test_cli_baseline_comparison(self):
        with tempfile.TemporaryDirectory() as before, tempfile.TemporaryDirectory() as after:
            self.write(before, 1, "Somehow, as if etched, it rose slowly.")
            self.write(after, 1, "It rose.")
            code, out = self.run_main([after, "--baseline", before])
        self.assertEqual(code, 0)
        self.assertIn("Before and after", out)
        self.assertIn("-4", out)

    def test_cli_file_options(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as out:
            self.write(d, 1, "We saw the red pepper boats at dawn.")
            self.write(d, 2, "They saw the red pepper boats at night.")
            names, preface = os.path.join(out, "names.txt"), os.path.join(out, "pre.md")
            report, data = os.path.join(out, "r.md"), os.path.join(out, "r.json")
            with open(names, "w", encoding="utf-8") as fh:
                fh.write("pepper\n")
            with open(preface, "w", encoding="utf-8") as fh:
                fh.write("## Editor's summary\n\nRead me first.\n")
            code, printed = self.run_main([d, "-o", report, "-p", preface, "--json", data, "-n", names])
            self.assertEqual(code, 0)
            self.assertEqual(printed, "")
            with open(report, encoding="utf-8") as fh:
                text = fh.read()
            with open(data, encoding="utf-8") as fh:
                payload = json.load(fh)
        self.assertLess(text.index("Read me first."), text.index("## 1. Density ranking"))
        self.assertIn("0 phrases qualify overall", text)   # names file breaks the only phrase
        self.assertIn("_None found._", text)
        self.assertEqual([c["label"] for c in payload["chapters"]], ["Ch01", "Ch02"])
        self.assertEqual(payload["ranking"][0]["rank"], 1)

    def test_cli_hits_images_all_and_unknown(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, 1, "The storm came like a storm of hail.")
            code, out = self.run_main([d, "-k", "img:storm,bogus"])
            _, everything = self.run_main([d, "-k", "all"])
        self.assertIn("## img:storm (2 hits)", out)
        self.assertIn("## bogus: unknown key", out)
        self.assertIn("## like_a (1 hits)", everything)

    def test_cli_empty_directory_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            with contextlib.redirect_stderr(buf):
                code, _ = self.run_main([d])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
