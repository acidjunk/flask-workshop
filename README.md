## Install for development

    mkvirtualenv --python=/usr/local/bin/python3 improviser
    pip install -r requirements.txt
    createdb workskop
    createuser workshop -sP
    psql -d workshop < workshop_initial.psql
    FLASK_APP=main flask run

## With env

    cp env.example env
    ./start.sh

## Version handling

Bump version (first lookup up current version and commit)

    bumpversion --current-version 0.2.0 minor version.py

Will bump version to 0.3.0

    bumpversion --current-version 0.2.0 patch version.py

Will bump version to 0.2.1

## Update deployment
```
workon improviser_deploy
zappa update
```

## License
Copyright (C) 2019 René Dohmen <acidjunk@gmail.com>

Licensed under the GNU GENERAL PUBLIC LICENSE Version 3
A copy of the LICENSE is included in the project.
