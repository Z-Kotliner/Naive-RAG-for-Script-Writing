import qdrant_client.http.exceptions
from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re
import requests
import json

class MovieQAToolTest(StageTest):
    test_data = [
        (
            "Mission Impossible",
            129,
            r"Loaded script for Mission Impossible from https://imsdb\.com/scripts/Mission-Impossible\.html\.",
            "All scenes involving trains",
            r"Scene \d+:.*(train|trains|conductor|railway|station|car|Ethan|Claire|terminus)"
        ),
        (
            "Titanic",
            109,
            r"Loaded script for Titanic from https://imsdb\.com/scripts/Titanic\.html\.",
            "All scenes involving ships",
            r"Scene \d+:.*(ship|abyss|lizzy|dreams|renault|leviathan|wreck|titanic|Brock|Rose)"
        ),
    ]

    @staticmethod
    def check_qdrant_connection():
        """Checks connectivity with the Qdrant server."""
        try:
            response = requests.get("http://localhost:6333/collections")
            if response.status_code != 200:
                return "Cannot connect to the Qdrant server. Make sure it is running."
        except (requests.ConnectionError, requests.exceptions.RequestException):
            return "Cannot connect to the Qdrant server. Make sure it is running."
        except Exception as e:
            return f"An error occurred while connecting to the Qdrant server. Encountered: {e}!"
        return None

    @staticmethod
    def verify_qdrant_collection(collection):
        """Validates the Qdrant collection for the given movie."""
        try:
            response = requests.get(f"http://localhost:6333/collections/{collection}")
            data = response.json()
        except qdrant_client.http.exceptions.UnexpectedResponse as e:
            return f"Unable to create a collection for the script of {collection.replace('-', ' ')}. Encountered: {e}"
        except qdrant_client.http.exceptions.ResponseHandlingException as e:
            return f"Cannot connect to the Qdrant server. Make sure it is running. Encountered: {e}"
        except json.JSONDecodeError:
            return "Response is not valid JSON."
        except Exception as e:
            return f"An error occurred while loading the collection for {collection.replace('-', ' ')}. Encountered: {e}!"

        expected_keys = {'status', 'time', 'result'}
        if not expected_keys.issubset(data.keys()):
            return f"Response JSON does not contain the expected keys: {expected_keys}"
        if data.get('status') != 'ok':
            return f"Expected status 'ok', but got '{data.get('status')}'"

        result = data.get('result', {})
        config = result.get('config')
        if not isinstance(config, dict):
            return "'config' is not a dictionary in 'result'"
        params = config.get('params')
        if not isinstance(params, dict):
            return "'params' is missing or not a dictionary in 'config'"
        vectors = params.get('vectors')
        if not isinstance(vectors, dict):
            return "'vectors' is missing or not a dictionary in 'params'"

        if vectors.get('distance') != 'Cosine':
            return f"Expected distance to be 'Cosine', but got '{vectors.get('distance')}'"
        if vectors.get('size') not in [384, 1536]:
            return f"Expected size to be 384 or 1536, but got '{vectors.get('size')}'"
        if result.get('points_count', 0) == 0:
            return f"The collection '{collection}' does not contain anything"
        return None

    @dynamic_test(time_limit=0)
    def test1_loading_and_retrieval(self):

        for movie, scene_count, expected_info_regex, query, expected_scene_response_regex in self.test_data:
            program = TestedProgram()
            program.start()
            output = program.execute(movie)
            output2 = program.execute(query)

            # Check for the expected info line using the provided regex.
            if not re.search(expected_info_regex, output):
                return CheckResult.wrong(
                    f"For movie '{movie}', the expected title and script URL were not found."
                )

            # Check for scene count information.
            expected_scene_info = f"Found {scene_count} scenes in the script for {movie}."
            if expected_scene_info not in output:
                return CheckResult.wrong(
                    f"For movie '{movie}', expected scene count info '{expected_scene_info}' was not found. Expected {scene_count} scenes. Did you use the correct scene splitter settings?\n"
                )

            # Check that the embedded script info is present.
            embedded_info = f"Embedded script for {movie}."
            if embedded_info not in output:
                return CheckResult.wrong(
                    f"For movie '{movie}', expected embedded script info '{embedded_info}' was not found.\n"
                )

            # Verify that at least one scene marker "Scene 1:" is present.
            if "Scene 1:" not in output2:
                return CheckResult.wrong(
                    f"For movie '{movie}', the marker 'Scene 1:' was not found in the scene output."
                )

            # Check that at least one scene matches the expected scene response regex.
            if not re.search(expected_scene_response_regex, output2, re.IGNORECASE):
                return CheckResult.wrong(
                    f"For movie '{movie}', no scene matching the expected pattern was found.\nExpected pattern: {expected_scene_response_regex}\n"
                )
        return CheckResult.correct()

    @dynamic_test(time_limit=0)
    def test2_check_embeddings(self):
        """
        Test the embeddings by verifying that the expected Qdrant collection
        has valid configuration and content.
        """
        expected_collection_names = ["Mission-Impossible"]
        error = self.check_qdrant_connection()
        if error:
            return CheckResult.wrong(error)
        for collection in expected_collection_names:
            error = self.verify_qdrant_collection(collection)
            if error:
                return CheckResult.wrong(error)
        return CheckResult.correct()

if __name__ == '__main__':
    MovieQAToolTest().run_tests()
