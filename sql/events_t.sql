CREATE TABLE IF NOT EXISTS {EVENTS_T} (
    id  BIGINT,
    type    VARCHAR,
    actorId   BIGINT,
    actorLogin  VARCHAR,
    repoId  BIGINT,
    repoName    VARCHAR,
    payloadPushId   BIGINT,
    payloadSize     INTEGER,
    payloadDistinctSize INTEGER,
    payloadRef  VARCHAR,
    payloadHead VARCHAR,
    payloadBefore   VARCHAR,
    payloadCommit   JSON,
    public  VARCHAR,
    created_at  TIMESTAMP,
    organization JSON,
    PRIMARY KEY(id)
)