INSERT INTO {CONTENTS_T} (
    name,
    path,
    sha,
    size,
    url,
    content,
    encoding,
    repository
)
SELECT
    data ->> 'name' AS name,
    data ->> 'path' AS path,
    data ->> 'sha' AS sha,
    (data ->> 'size')::INT AS size,
    data ->> 'url' AS url,
    (data ->> 'content')::TEXT AS content,
    data ->> 'encoding' AS encoding,
    data ->> 'repository'
FROM
    staging
ON CONFLICT DO NOTHING