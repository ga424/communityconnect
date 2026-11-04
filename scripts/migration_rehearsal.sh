#!/usr/bin/env bash
set -euo pipefail
# Dedicated disposable cc_test database only. No production URL accepted.
liquibase_run() {
  docker compose run --rm migrate \
    --url=jdbc:postgresql://db:5432/cc_test \
    --username=cc_test --password=cc_test \
    --changelog-file=changelog/db.changelog.xml "$@"
}
liquibase_run update
liquibase_run update
liquibase_run rollback-count --count=1
liquibase_run update
