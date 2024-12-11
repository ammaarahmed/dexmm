export $(grep -v '^#' .env | xargs)


# unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)
