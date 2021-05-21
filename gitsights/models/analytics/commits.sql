{{ config(materialized='view') }}

SELECT
    sha,
    commiter,
    commit_date,
    commit_message,
    comment_count,
    stats_total,
    stats_additions,
    stats_deletions,
    file ->> 'sha' AS file_sha,
    file ->> 'filename' AS filename,
    file ->> 'status' AS status,
    (file ->> 'additions')::INT AS additions,
    (file ->> 'deletions')::INT AS deletions,
    (file ->> 'changes')::INT AS changes,
    repository
FROM
    git_t.commits_t,
    json_array_elements(files) as file