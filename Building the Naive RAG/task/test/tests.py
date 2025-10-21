from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re

class MovieQAToolTest(StageTest):
    # Each tuple: (movie title, expected scene count, expected info regex, expected keywords regex)
    test_data = [
        (
            "Mission Impossible",
            129,
            r"Loaded script for Mission Impossible from https://imsdb\.com/scripts/Mission-Impossible\.html\.",
            r"KITTRIDGE|ETHAN|LUTHER|CLAIRE|INT|EXT|CUT|CIA|TRAIN"
        ),
        (
            "Batman",
            127,
            r"Loaded script for Batman from https://imsdb\.com/scripts/Batman\.html\.",
            r"Gotham|Joker|Eddie|Nick|Knox|INT|CUT|EXT|Bruce Wayne"
        ),
        (
            "Titanic",
            109,
            r"Loaded script for Titanic from https://imsdb\.com/scripts/Titanic\.html\.",
            r"JACK|ROSE|CAL|FABRIZIO|INT|EXT|CUT|SHIP"
        ),
        (
            "Wonder Woman",
            55,
            r"Loaded script for Wonder Woman from https://imsdb\.com/scripts/Wonder-Woman\.html\.",
            r"WONDER WOMAN|DIANA|STEVE|Ares|EXT|INT|CUT|ISLAND|TRENCH",
        )
    ]

    @dynamic_test(time_limit=0)
    def test_movie_qa_tool(self):
        for movie, scene_count, expected_info_regex, expected_keywords_regex in self.test_data:
            program = TestedProgram()

            # Start the program (initial output is not checked here).
            program.start()

            # Simulate the user entering the movie title.
            output = program.execute(movie)

            # Check for the expected info line using the provided regex.
            if not re.search(expected_info_regex, output):
                return CheckResult.wrong(
                    f"For movie '{movie}', the expected info about the movie and script URL was not found in the output.\n\n"
                )

            # Check for the scene count information.
            expected_scene_info = f"Found {scene_count} scenes in the script for {movie}."
            if expected_scene_info not in output:
                return CheckResult.wrong(
                    f"For movie '{movie}', expected scene count info '{expected_scene_info}' was not found. Expected {scene_count} scenes. Did you use the correct scene splitter settings?\n"
                )

            # Check that at least one of the expected keywords is present.
            if not re.search(expected_keywords_regex, output, re.IGNORECASE):
                return CheckResult.wrong(
                    f"For movie '{movie}', none of the scenes matching the script for the movie were found in the output.\n\n"
                )

            # Verify that scene markers are printed with "Scene 1:".
            if "Scene 1:" not in output:
                return CheckResult.wrong(
                    f"For movie '{movie}', the marker 'Scene 1:' was not found in the scene output.\n\n"
                )
        return CheckResult.correct()

if __name__ == '__main__':
    MovieQAToolTest().run_tests()
