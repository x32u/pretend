CREATE TABLE IF NOT EXISTS autopfp (
    guild_id BIGINT NOT NULL,         -- ID of the guild
    channel_id BIGINT NOT NULL,       -- ID of the channel
    genre VARCHAR(50) NOT NULL,       -- Genre (e.g., male, female, anime, random, banner)
    type VARCHAR(50) NOT NULL,        -- Type (e.g., pfp, gif, or none)
    PRIMARY KEY (guild_id, genre, type) -- Ensures no duplicate configurations for the same guild and genre/type combination
);

CREATE TABLE if not exists afk (
    guild_id bigint,
    user_id bigint,
    reason text,
    "time" timestamp with time zone
);

CREATE TABLE if not exists aliases (
    guild_id bigint NOT NULL,
    command text NOT NULL,
    alias text NOT NULL
);

CREATE TABLE if not exists anti_join (
    guild_id bigint,
    rate integer
);

CREATE TABLE if not exists antinuke (
    guild_id bigint,
    configured text,
    owner_id bigint,
    whitelisted jsonb,
    admins jsonb,
    logs bigint
);

CREATE TABLE if not exists antinuke_modules (
    guild_id bigint,
    module text,
    punishment text,
    threshold integer
);

CREATE TABLE if not exists antispam (
    guild_id bigint,
    rate integer,
    timeout bigint,
    users text,
    channels text
);

CREATE TABLE if not exists api_key (
    user_id bigint NOT NULL,
    key text,
    role text
);

CREATE TABLE if not exists archive (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE if not exists archive_category (
    guild_id bigint NOT NULL,
    category_id bigint NOT NULL
);

CREATE TABLE if not exists uthorize (
    guild_id bigint,
    user_id bigint,
    till timestamp with time zone,
    transfers integer
);

CREATE TABLE if not exists autopfp (
    guild_id bigint NOT NULL,
    type text NOT NULL,
    category text NOT NULL,
    channel_id bigint,
    PRIMARY KEY (guild_id, type, category)
);

CREATE TABLE if not exists autoping (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    message text NOT NULL,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE if not exists autoreact (
    guild_id bigint NOT NULL,
    trigger text NOT NULL,
    reactions text NOT NULL,
    PRIMARY KEY (guild_id, trigger)
);

CREATE TABLE if not exists utoreacts (
    guild_id bigint NOT NULL,
    trigger text NOT NULL,
    reaction text NOT NULL,
    PRIMARY KEY (guild_id, trigger, reaction)
);

CREATE TABLE if not exists autoresponder (
    guild_id bigint,
    trigger text,
    response text,
    strict boolean DEFAULT true
);

CREATE TABLE if not exists autorole (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL,
    PRIMARY KEY (guild_id, role_id)
);

CREATE TABLE if not exists avatar_history (
    user_id text NOT NULL,
    name text,
    avatars text,
    background text,
    PRIMARY KEY (user_id)
);

CREATE TABLE if not exists avatar_urls (
    user_id bigint,
    token text,
    data bytea
);

CREATE TABLE if not exists avatars (
    user_id bigint NOT NULL,
    name text NOT NULL,
    avatar text NOT NULL,
    key text NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    PRIMARY KEY (user_id, key)
);

CREATE TABLE if not exists bday (
    user_id bigint,
    month integer,
    day integer
);

CREATE TABLE if not exists birthday (
    user_id bigint,
    bday timestamp with time zone,
    said text
);

CREATE TABLE if not exists blacklist (
    id bigint NOT NULL,
    type text NOT NULL,
    PRIMARY KEY (id, type)
);

CREATE TABLE if not exists boost (
    guild_id bigint,
    channel_id bigint,
    message text
);

CREATE TABLE if not exists booster_module (
    guild_id bigint,
    base bigint
);

CREATE TABLE if not exists booster_roles (
    guild_id bigint,
    user_id bigint,
    role_id bigint
);

CREATE TABLE if not exists br_award (
    guild_id bigint,
    role_id bigint
);

CREATE TABLE if not exists bumpreminder (
    guild_id bigint,
    channel_id bigint,
    user_id bigint,
    thankyou text,
    reminder text,
    "time" timestamp with time zone
);

CREATE TABLE if not exists confess (
    guild_id bigint,
    channel_id bigint,
    confession integer
);

CREATE TABLE if not exists confess_members (
    guild_id bigint,
    user_id bigint,
    confession integer
);

CREATE TABLE if not exists confess_mute (
    guild_id bigint,
    user_id bigint
);

CREATE TABLE if not exists counters (
    guild_id bigint,
    channel_type text,
    channel_id bigint,
    channel_name text,
    module text
);

CREATE TABLE if not exists disablecmd (
    guild_id bigint,
    cmd text
);

CREATE TABLE if not exists disablemodule (
    guild_id bigint NOT NULL,
    module text NOT NULL
);

CREATE TABLE if not exists donor (
    user_id bigint,
    since bigint,
    status text
);

CREATE TABLE if not exists economy (
    user_id bigint,
    cash double precision,
    card double precision,
    daily bigint,
    dice bigint
);

CREATE TABLE if not exists error_codes (
    code character varying(30) NOT NULL,
    info json,
    PRIMARY KEY (code)
);

CREATE TABLE if not exists fake_perms (
    guild_id bigint,
    role_id bigint,
    perms text
);

CREATE TABLE if not exists filter (
    guild_id bigint,
    mode text,
    rule_id bigint
);

CREATE TABLE if not exists force_nick (
    guild_id bigint,
    user_id bigint,
    nickname text
);

CREATE TABLE if not exists gamestats (
    user_id bigint,
    game text,
    wins integer,
    loses integer,
    total integer
);

CREATE TABLE if not exists give_roles (
    guild_id bigint,
    role_id bigint
);

CREATE TABLE if not exists giveaway (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    winners integer,
    members text,
    finish timestamp with time zone,
    host bigint,
    title text
);

CREATE TABLE if not exists global_disabled_cmds (
    cmd character varying(30) NOT NULL,
    disabled boolean,
    disabled_by text,
    PRIMARY KEY (cmd)
);

CREATE TABLE if not exists globalban (
    user_id bigint,
    reason text
);

CREATE TABLE if not exists gw_ended (
    channel_id bigint,
    message_id bigint,
    members text
);

CREATE TABLE if not exists hardban (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    reason text,
    moderator_id bigint NOT NULL
);

CREATE TABLE if not exists images (
    id text,
    url text
);

CREATE TABLE if not exists imgonly (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);

CREATE TABLE if not exists invoke (
    guild_id bigint,
    command text,
    embed text
);

CREATE TABLE if not exists jail (
    guild_id bigint,
    channel_id bigint,
    role_id bigint
);

CREATE TABLE if not exists jail_members (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    roles text,
    jailed_at timestamp with time zone,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE if not exists lastfm (
    user_id bigint,
    username text,
    reactions text,
    customcmd text,
    embed text
);

CREATE TABLE if not exists leave (
    guild_id bigint,
    channel_id bigint,
    message text
);

CREATE TABLE if not exists level_rewards (
    guild_id bigint,
    level integer,
    role_id bigint
);

CREATE TABLE if not exists level_user (
    guild_id bigint,
    user_id bigint,
    xp integer,
    level integer,
    target_xp bigint
);

CREATE TABLE if not exists leveling (
    guild_id bigint,
    channel_id bigint,
    message text,
    booster_boost text
);

CREATE TABLE if not exists lock_role (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL,
    PRIMARY KEY (role_id)
);

CREATE TABLE if not exists lockdown_ignore (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    PRIMARY KEY (channel_id)
);

CREATE TABLE if not exists logging (
    guild_id bigint NOT NULL,
    messages bigint,
    guild bigint,
    roles bigint,
    channels bigint,
    members bigint,
    PRIMARY KEY (guild_id)
);

CREATE TABLE if not exists logs (
    key text NOT NULL,
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    author jsonb DEFAULT '{}'::jsonb NOT NULL,
    logs jsonb DEFAULT '{}'::jsonb NOT NULL,
    PRIMARY KEY (key)
);

CREATE TABLE if not exists marry (
    author bigint,
    soulmate bigint,
    "time" bigint
);

CREATE TABLE if not exists number_counter (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    last_counted bigint,
    current_number integer,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE if not exists opened_tickets (
    guild_id bigint,
    channel_id bigint,
    user_id bigint
);

CREATE TABLE if not exists prefixes (
    guild_id bigint NOT NULL,
    prefix text
);

CREATE TABLE if not exists reactionrole (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    emoji text,
    role_id bigint
);

CREATE TABLE if not exists reminder (
    user_id bigint,
    channel_id bigint,
    guild_id bigint,
    date timestamp with time zone,
    task text
);

CREATE TABLE if not exists reskin (
    user_id bigint,
    username text,
    avatar_url text,
    toggled boolean
);

CREATE TABLE if not exists reskin_enabled (
    guild_id bigint
);

CREATE TABLE if not exists restore (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    roles text,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE if not exists restrictcommand (
    guild_id bigint NOT NULL,
    command text NOT NULL,
    role_id bigint NOT NULL
);

CREATE TABLE if not exists seen (
    user_id bigint,
    guild_id bigint,
    "time" timestamp with time zone
);

CREATE TABLE if not exists selfprefix (
    user_id bigint NOT NULL,
    prefix text,
    PRIMARY KEY (user_id)
);

CREATE TABLE if not exists spotify (
    user_id bigint,
    access_token text
);

CREATE TABLE if not exists starboard (
    guild_id bigint,
    channel_id bigint,
    emoji text,
    count integer,
    role_id bigint
);

CREATE TABLE if not exists starboard_messages (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    starboard_message_id bigint
);

CREATE TABLE if not exists stickymessage (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    message text NOT NULL,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE if not exists tags (
    guild_id bigint NOT NULL,
    author_id bigint NOT NULL,
    name text NOT NULL,
    response text NOT NULL
);

CREATE TABLE if not exists ticket_topics (
    guild_id bigint,
    name text,
    description text
);

CREATE TABLE if not exists tickets (
    guild_id bigint,
    open_embed text,
    category_id bigint,
    logs bigint,
    support_id bigint
);

CREATE TABLE if not exists timezone (
    user_id bigint,
    zone text
);

CREATE TABLE if not exists trial (
    guild_id bigint NOT NULL,
    end_date integer,
    PRIMARY KEY (guild_id)
);

CREATE TABLE if not exists trials (
    guild_id bigint NOT NULL,
    expires bigint NOT NULL,
    PRIMARY KEY (guild_id)
);

CREATE TABLE if not exists username_track (
    guild_id bigint,
    webhook_url text
);

CREATE TABLE if not exists usernames (
    user_id bigint,
    user_name text,
    "time" bigint
);

CREATE TABLE if not exists vcs (
    user_id bigint,
    voice bigint
);

CREATE TABLE if not exists vm_buttons (
    guild_id bigint,
    action text,
    label text,
    emoji text,
    style text
);

CREATE TABLE if not exists voicemaster (
    guild_id bigint,
    channel_id bigint,
    interface_id bigint
);

CREATE TABLE if not exists warns (
    guild_id bigint,
    user_id bigint,
    author_id bigint,
    "time" text,
    reason text
);

CREATE TABLE if not exists webhook (
    guild_id bigint,
    code text,
    url text,
    channel text,
    name text,
    avatar text
);

CREATE TABLE if not exists welcome (
    guild_id bigint,
    channel_id bigint,
    message text
);

CREATE TABLE if not exists whitelist (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL
);

CREATE TABLE if not exists whitelist_state (
    guild_id bigint NOT NULL,
    embed text,
    PRIMARY KEY (guild_id)
);

CREATE TABLE if not exists xray (
    guild_id bigint,
    target_id bigint,
    webhook_url text
);