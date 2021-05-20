{{ config(materialized='view') }}

-- PRs view
SELECT id,
    type,
    actorid,
    actorlogin,
    repoid,
    reponame,
    public,
    (organization ->> 'id')::INT             AS organization_id,
    organization ->> 'login'                 AS organization_name,
    -- payloadcommit
    (payloadcommit ->> 'push_id')::BIGINT    AS push_id,
    (payloadcommit ->> 'size')::INT          AS size,
    (payloadcommit ->> 'distinct_size')::INT AS distinct_size,
    payloadcommit ->> 'action' AS action,
    (payloadcommit ->> 'number')::INT AS number,
    json_extract_path_text(payloadcommit, 'pull_request', 'url') AS pullrequest_url,
    (json_extract_path_text(payloadcommit, 'pull_request', 'id'))::INT AS pullrequest_id,
    json_extract_path_text(payloadcommit, 'pull_request', 'state') AS state,
    json_extract_path_text(payloadcommit, 'pull_request', 'locked') AS locked,
    json_extract_path_text(payloadcommit, 'pull_request', 'title') AS title,
    json_extract_path_text(payloadcommit, 'pull_request', 'user', 'login') AS author_name,
    (json_extract_path_text(payloadcommit, 'pull_request', 'user', 'id'))::INT AS author_id,
    (json_extract_path_text(payloadcommit, 'pull_request', 'created_at'))::TIMESTAMP AS created_at,
    (json_extract_path_text(payloadcommit, 'pull_request', 'updated_at'))::TIMESTAMP AS updated_at,
    (json_extract_path_text(payloadcommit, 'pull_request', 'closed_at'))::TIMESTAMP AS closed_at,
    (json_extract_path_text(payloadcommit, 'pull_request', 'merged_at'))::TIMESTAMP AS merged_at,
    (json_extract_path_text(payloadcommit, 'pull_request', 'comments'))::INT AS comments,
    (json_extract_path_text(payloadcommit, 'pull_request', 'commits'))::INT AS commits,
    (json_extract_path_text(payloadcommit, 'pull_request', 'additions'))::INT AS additions,
    (json_extract_path_text(payloadcommit, 'pull_request', 'deletions'))::INT AS deletions,
    (json_extract_path_text(payloadcommit, 'pull_request', 'changed_files'))::INT AS changed_files
FROM git_t.events_t
WHERE type = 'PullRequestEvent'