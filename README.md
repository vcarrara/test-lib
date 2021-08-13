# olympuslib

**olympuslib** is a Python library containing reusable logics for **Olympe's** data pipeline.

## How to install

### Development

Run the following commands:

```bash
pip install git+https://github.com/namkinmkg/olympuslib.git@RELEASE_VERSION
```

### Testing

The repository contains tests that are not packaged to the final library. To execute these tests, run:

```bash
pip install pytest
pytest
```

## Usage

Import the library as a standard Python lib:

```python
import olympuslib
```

Use the custom logger for monitoring:

```python
from olympuslib.logging.logger import OlympusLogger

logger = OlympusLogger(log_to_file=True, file_path="./logs")
logger.critical('Something went wrong')
```
