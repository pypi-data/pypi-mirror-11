Do What Thou Wilt Shall be the Whole of the Law.

======
gulag
=======

`gulag` is a higher level mongodb driver.

Dedicated to all political, corporate & religious dissidents. In every juristiction.
Vive toutes les differences!


Highlights:

- Declarative collections (model in MVC paradigmn)
- Auto-reconnect


::
# Your mongodb collection definition:

    import gulag

    class Task(gulag.nosql.MongoModel):
        """
       Don't be a pathetic task rabbit. Roll your own.

        == Schema (polite documentation only) =====

        key : Cache key
        expires_utc : Expiry time
        b64: Encoded pickle
        """

        db_name = "my_database"
        col_name = "my_col"            # omit to use class name
        capped_size = 1024 * 1024      # 1 GB (omit for non-capped)

        index = [
            ("key", "is_active", "expires_utc", )
        ]

    # Instantiate package global:
    TASK = Task()


Python package installation
----------------------------
>pip install gulag


setting.py
----------
MONGO_URL      = "mongodb://127.0.0.1:27017"


# Example in-application use:
-----------------------------

```

from gulag import nosql
import setting

nosql.conf.from_object(setting)
from myapp.mymodel import TASK

doc = TASK.find_one({"key": "unique"})


```

Author: @meduccio
Love is the Law. Love under will.

# Change log --------------------------------------------------------------------------------------------------------------
- Add analytics support e.g.
    MONGO_METRICS = {
        "DB_NAME": "analytics",
        "LIMIT_MS" : 500.0,  # Record nothing quicker than 500ms
    }
- Dedication & motivation
- Increase default connection pool from 20 to 200
