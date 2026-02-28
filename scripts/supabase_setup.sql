-- Supabase / Postgres schema for technova community
-- Run in Supabase SQL editor or psql

create table if not exists discussions (
  id text primary key,
  title text not null,
  body text,
  author_type text default 'anonymous',
  author_value text,
  created_at bigint not null
);

create table if not exists comments (
  id text primary key,
  discussion_id text references discussions(id) on delete cascade,
  parent_id text,
  text text not null,
  author_type text default 'anonymous',
  author_value text,
  likes integer default 0,
  created_at bigint not null
);

create index if not exists idx_comments_discussion_id on comments(discussion_id);
create index if not exists idx_comments_parent_id on comments(parent_id);
