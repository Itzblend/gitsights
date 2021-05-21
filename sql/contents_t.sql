CREATE TABLE IF NOT EXISTS {CONTENTS_T} (
    name    VARCHAR,
    path    VARCHAR,
    sha     VARCHAR,
    size    INTEGER,
    url     VARCHAR,
    content TEXT,
    encoding    VARCHAR,
    PRIMARY KEY(sha, path)
)