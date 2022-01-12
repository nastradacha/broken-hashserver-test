# Broken-Hashserver Automation Exercise

The current project is developed using Python and Pytest framework

## Python pip modules


    pip install requests
    pip install pytest
## Environment Variables

This Project has been executed on Windows


Windows example:
1. C:/> SET PORT=8088
2. Use the Control Panel to set a System or User variable for
PORT. Remember to reopen your cmd window after doing this.


## Running Tests

To run tests, run the following command from root folder

```bash
  pytest -v  --html=test_results\broken_hashserver.html

```


## Documentation

[Documentation](https://linktodocumentation)

1. Sets the environment variable Port
2. Starts the Server
3. A POST to /hash  tthat accepts a string and returns job_id
4. A GET to /hash should accept a job identifier. It should return the base64 encoded password hash for the corresponding POST request.
5. A GET to /stats should accept no data. It should return a JSON data structure
  for the total hash requests since the server started and the average time of a hash request in milliseconds       
