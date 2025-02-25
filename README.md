# Bookstore API

## Testing Strategy

**Unit Tests**: Tests related to individual components or functions in isolation. I have tried to cover most of the functions from main.py and bookmgmt.py

**Integration Tests**: Focuses on testing how different parts of the system work together, such as the interaction between the APIs, database, and other components. These tests ensure that the system works as expected in a real-world scenario.

## Test Frameworks:
 I've used pytest for writing and running tests. Also used pytest-xdist for parallel test execution to speed up the testing process.

## Running Tests

To run locally install the requirements from requirements.txt and run the following command

python -m pytest -s .\TestCases\path_to_testcase

(e.g python -m pytest -s .\TestCases\UnitTests\test_main\test_login.py)


## Challenges faced while writing Tests

Database Isolation: Integration tests often interact with a shared database. We had to ensure proper database isolation and cleanup between tests to avoid conflicts.

Test Dependencies: Some tests depend on the success of others (e.g., retrieving a book by ID after adding it). We had to ensure that tests were executed in a controlled order and handled edge cases like missing data.

Handling Redirects: Some API endpoints triggered redirects (e.g., HTTP 307), which caused issues in test execution. We had to use follow_redirects=True to handle these scenarios.

Authentication: We encountered challenges in managing authentication tokens across multiple tests. To solve this, we created a fixture to handle token retrieval and reuse



