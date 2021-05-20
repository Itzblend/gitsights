CREATE TABLE IF NOT EXISTS {COMMITS_T} (
    sha     VARCHAR,
    commiter    VARCHAR,
    commit_date TIMESTAMP,
    commit_message  VARCHAR,
    comment_count   VARCHAR,
    filename    VARCHAR,
    status      VARCHAR,
    stats_total INTEGER,
    stats_additions   INTEGER,
    stats_deletions   INTEGER,
    files   JSON,
    PRIMARY KEY(sha)
)