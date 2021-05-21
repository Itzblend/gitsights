INSERT INTO {COMMITS_T} (
    sha,
    commiter,
    commit_date,
    commit_message,
    comment_count,
    stats_total,
    stats_additions,
    stats_deletions,
    files,
    repository
)
SELECT
    data ->> 'sha' AS sha,
    data #>> '{{commit, committer, name}}' AS commiter,
    (data #>> '{{commit, committer, date}}')::TIMESTAMP AS commit_date,
    data #>> '{{commit, message}}' AS commit_message,
    (data #>> '{{commit, comment_count}}')::INT AS comment_count,
    (data #>> '{{stats, total}}')::INT AS stats_total,
    (data #>> '{{stats, additions}}')::INT AS stats_additions,
    (data #>> '{{stats, deletions}}')::INT AS stats_deletions,
    (data -> 'files')::JSON AS files,
    data ->> 'repository' AS repository
FROM
    staging
ON CONFLICT DO NOTHING