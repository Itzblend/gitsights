INSERT INTO {ORGANIZATION_T} (
    avatar_url,
    company,
    created_at,
    description,
    email,
    followers,
    following,
    has_organization_projects,
    has_repository_projects,
    id,
    is_verified,
    location,
    login,
    name,
    node_id,
    public_gists,
    public_members_url,
    public_repos,
    repos_url,
    twitter_username,
    type,
    updated_at
)
SELECT
    data ->> 'avatar_url' AS avatar_url,
    data ->> 'company' AS company,
    (data ->> 'created_at')::TIMESTAMP AS created_at,
    data ->> 'description' AS description,
    data ->> 'email' AS email,
    (data ->> 'followers')::INT AS followers,
    (data ->> 'following')::INT AS following,
    data ->> 'has_organization_projects' AS has_organization_projects,
    data ->> 'has_repository_projects' AS has_repository_projects,
    (data ->> 'id')::BIGINT AS id,
    data ->> 'is_verified' AS is_verified,
    data ->> 'location' AS location,
    data ->> 'login' AS login,
    data ->> 'name' AS name,
    data ->> 'node_id' AS node_id,
    (data ->> 'public_gists')::INT AS public_gists,
    data ->> 'public_members_url' AS public_members_url,
    (data ->> 'public_repos')::INT AS public_repos,
    data ->> 'repos_url' AS repos_url,
    data ->> 'twitter_username' AS twitter_username,
    data ->> 'type' AS type,
    (data ->> 'updated_at')::TIMESTAMP AS updated_at
FROM staging
ON CONFLICT (id, node_id) DO UPDATE
    SET
        avatar_url = excluded.avatar_url,
        company = excluded.company,
        description = excluded.description,
        email = excluded.email,
        followers = excluded.followers,
        following = excluded.following,
        has_organization_projects = excluded.has_organization_projects,
        has_repository_projects = excluded.has_repository_projects,
        is_verified = excluded.is_verified,
        location = excluded.location,
        login = excluded.login,
        name = excluded.name,
        public_gists = excluded.public_gists,
        public_members_url = excluded.public_members_url,
        public_repos = excluded.public_repos,
        repos_url = excluded.repos_url,
        twitter_username = excluded.twitter_username,
        type = excluded.type
