INSERT INTO {EVENTS_T} (
    id,
    type,
    actorId,
    actorLogin,
    repoId,
    repoName,
    payloadPushId,
    payloadSize,
    payloadDistinctSize,
    payloadRef,
    payloadHead,
    payloadBefore,
    payloadCommit,
    public,
    created_at,
    organization
)
SELECT
    (data ->> 'id')::BIGINT AS id,
    data ->> 'type' AS type,
    (data #>> '{{actor, id}}')::BIGINT AS actorid,
    data #>> '{{actor, login}}' AS actorlogin,
    (data #>> '{{repo, id}}')::BIGINT AS repoid,
    data #>> '{{repo, name}}' AS reponame,
    (data #>> '{{payload, push_id}}')::BIGINT AS payloadpushid,
    (data #>> '{{payload, size}}')::INT AS payloadsize,
    (data #>> '{{payload, distinct_size}}')::INT AS payloaddistinctsize,
    data #>> '{{payload, ref}}' AS payloadref,
    data #>> '{{payload, head}}' AS payloadhead,
    data #>> '{{payload, before}}' AS payloadbefore,
    data -> 'payload' AS payloadcommit,
    data ->> 'public' AS public,
    (data ->> 'created_at')::TIMESTAMP AS created_at,
    data -> 'org' AS organization
FROM staging
ON CONFLICT DO NOTHING
