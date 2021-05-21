INSERT INTO {ISSUES_T} (
    id,
    node_id,
    number,
    title,
    user_name,
    user_id,
    user_type,
    state,
    locked,
    assignees,
    milestone,
    comments,
    created_at,
    updated_at,
    closed_at,
    repository_name,
    repository_id,
    body
)
SELECT
    (data ->> 'id')::INT AS id,
    data ->> 'node_id' AS node_id,
    (data ->> 'number')::INT AS number,
    data ->> 'title' AS title,
    data #>> '{{user, login}}' AS user_name,
    (data #>> '{{user, id}}')::INT AS user_id,
    data #>> '{{user, type}}' AS user_type,
    data ->> 'state' AS state,
    data ->> 'locked' AS locked,
    (data -> 'assignees')::JSON AS assignees,
    data ->> 'milestone' AS milestone,
    (data ->> 'comments')::INT AS comments,
    (data ->> 'created_at')::TIMESTAMP AS created_at,
    (data ->> 'updated_at')::TIMESTAMP AS updated_at,
    (data ->> 'closed_at')::TIMESTAMP AS closed_at,
    data #>> '{{repository, name}}' AS repository_name,
    (data #>> '{{repository, id}}')::INT AS repository_id,
    data ->> 'body' AS body
FROM
    staging
ON CONFLICT DO NOTHING