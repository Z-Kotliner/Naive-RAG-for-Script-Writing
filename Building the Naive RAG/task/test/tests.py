from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re

class MovieAppTest(StageTest):
    # Each tuple contains:
    # - the movie title as input,
    # - a regex pattern to check the expected info line with URL,
    # - a regex pattern to capture one or more expected keywords in the output.
    test_data = [
        (
            "Mission Impossible",
            r"Loaded script for Mission Impossible from https://imsdb\.com/scripts/Mission-Impossible\.html\.",
            r"KITTRIDGE|ETHAN|LUTHER|CLAIRE|INT|EXT|CUT|CIA|TRAIN"
        ),
        (
            "Batman",
            r"Loaded script for Batman from https://imsdb\.com/scripts/Batman\.html\.",
            r"Gotham|Joker|Eddie|Nick|Knox|INT|CUT|EXT|Bruce Wayne"
        ),
        (
            "Titanic",
            r"Loaded script for Titanic from https://imsdb\.com/scripts/Titanic\.html\.",
            r"JACK|ROSE|CAL|FABRIZIO|INT|EXT|CUT|SHIP"
        ),
        (
            "Wonder Woman",
            r"Loaded script for Wonder Woman from https://imsdb\.com/scripts/Wonder-Woman\.html\.",
            r"WONDER WOMAN|DIANA|STEVE|Ares|EXT|INT|CUT|ISLAND|TRENCH"
        ),
        (
            "X-Men",
            r"Loaded script for X-Men from https://imsdb\.com/scripts/X-Men\.html\.",
            r"XAVIER|MAGNETO|LOGAN|JEAN|EXT|INT|CUT|TOAD|PYRO|MYSTIQUE|NEWSCASTER|KELLY",
        )
    ]

    @dynamic_test(time_limit=0)
    def test_movie_scripts(self):
        try:
            for query, expected_info_regex, expected_keywords_regex in self.test_data:
                program = TestedProgram()
                program.start()
                output = program.execute(query).strip()

                # Check that the expected info line (with URL) is present.
                if not re.search(expected_info_regex, output, re.IGNORECASE):
                    return CheckResult.wrong(
                        f"The expected info about the movie title and script URL were not found in the output.\n\n"
                    )

                # Check that at least one of the expected keywords is present.
                if not re.search(expected_keywords_regex, output, re.IGNORECASE):
                    return CheckResult.wrong(
                        f"For query '{query}', none of the expected keywords matching the script for the movie were found in the output.\n\n"
                    )
            return CheckResult.correct()
        except Exception as e:
            return CheckResult.wrong(f"An error occurred during testing: {e}")

if __name__ == '__main__':
    MovieAppTest().run_tests()
