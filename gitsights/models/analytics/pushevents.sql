{{ config(materialized='view') }}

-- pushevents view
 SELECT id,
        type,
        actorid,
        actorlogin,
        repoid,
        reponame,
        payloadpushid,
        payloadsize,
        payloadhead,
        payloadbefore,
        public,
        created_at,
        (organization ->> 'id')::INT             AS organization_id,
        organization ->> 'login'                 AS organization_name,
        -- payloadcommit
        (payloadcommit ->> 'push_id')::BIGINT    AS push_id,
        (payloadcommit ->> 'size')::INT          AS size,
        (payloadcommit ->> 'distinct_size')::INT AS distinct_size,
        commit ->> 'sha'                         AS sha,
        json_extract_path_text(commit, 'author', 'email') AS author_email,
        json_extract_path_text(commit, 'author', 'name')  AS author_name,
        commit ->> 'message'                     AS message,
        commit ->> 'distinct'                    AS distinct,
        commit ->> 'url'                         AS commit_url
 FROM git_t.events_t,
      json_array_elements(payloadcommit -> 'commits') AS commit
WHERE type = 'PushEvent'