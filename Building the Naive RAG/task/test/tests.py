import qdrant_client.http.exceptions
from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import requests
import json

class RAGTest(StageTest):
    test_data = [
        (
            "BlacKkKlansman",
            113,
            "https://imsdb.com/scripts/BlacKkKlansman.html",
        ),
        (
            "Mission Impossible",
            129,
            "https://imsdb.com/scripts/Mission-Impossible.html",
        ),
        (
            "Wonder Woman",
            55,
            "https://imsdb.com/scripts/Wonder-Woman.html",
        )
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
    def test1_loading_docs(self):
        """
        Test the loading of movie scripts by simulating user input (the movie title),
        verifying the loaded script info, and checking for expected scene count info.
        """
        error = self.check_qdrant_connection()
        if error:
            return CheckResult.wrong(error)

        for movie, scene_count, expected_url in self.test_data:
            program = TestedProgram()
            program.start()  # Start the program; initial output is not checked here.
            output = program.execute(movie)

            expected_info_lines = [
                f"Loaded script for {movie} from {expected_url}.",
                f"Found {scene_count} scenes in the script for {movie}.",
                f"Embedded script for {movie}."
            ]
            for line in expected_info_lines:
                if line not in output:
                    return CheckResult.wrong(
                        f"Expected info '{line}' not found in the output for movie {movie}.\n\n"
                    )
        return CheckResult.correct()

    @dynamic_test(time_limit=0)
    def test2_check_embeddings(self):
        """
        Test the embeddings by verifying that each expected Qdrant collection
        has valid configuration and content.
        """
        error = self.check_qdrant_connection()
        if error:
            return CheckResult.wrong(error)

        # For each movie in test_data, derive the expected collection name.
        for movie, _, _ in self.test_data:
            collection_name = movie if " " not in movie else movie.replace(" ", "-")
            error = self.verify_qdrant_collection(collection_name)
            if error:
                return CheckResult.wrong(error)
        return CheckResult.correct()

if __name__ == '__main__':
    RAGTest().run_tests()
