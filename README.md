# PyLog
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog?ref=badge_shield)

Just another one Python logging package

## Description
PyLog supports sending logs to different way like a Graylog, rsyslog, file or HTTP.

## Usage

- Add JSON configuration file `logging.cfg` to project root directory.
- Fill it by following format:
    ```json
    {
        "targets": [
            {
                "name": "fl",
                "type": "file",
                "filename": "test.log"
            },
            {
                "name": "wf1",
                "type": "watch-file",
                "filename": "test.log"
            },
            {
                "name": "wf",
                "type": "watch-file",
                "filename": "test1.log"
            },
            {
                "name": "ht",
                "type": "http",
                "host": "localhost",
                "url": "example.com"
            },
            {
                "name": "gl",
                "type": "graylog",
                "host": "localhost",
                "port": 12202,
                "facility": "tst"
            }
        ],
        "rules": [
            {
                "name": "test*",
                "min-level": "info",
                "write-to": "fl,gl,ht,wf,wf1"
            }
        ]
    }
    ```
- Finally call `getLogger` function to initialize your logger:
    ```python
    from PyLog inport Logger
    
    # put some code here
    
    logger = Logger.getLogger('logger-name')
    ```
- Enjoy sending your logs everywhere

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FiPhosgen%2Fepylog?ref=badge_large)