{{ config(materialized='view') }}

SELECT
    sha,
    commit_message,
    COUNT(*) AS affected_files,
    stats_total,
    stats_additions,
    stats_deletions,
    commiter,
    commit_date,
    repository
FROM
    git_t.commits_t
GROUP BY sha, commit_message, commit_date, commiter, stats_total, stats_additions, stats_deletions, repository