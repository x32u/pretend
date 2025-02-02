--
-- PostgreSQL database dump
--

-- Dumped from database version 15.7 (Debian 15.7-0+deb12u1)
-- Dumped by pg_dump version 15.7 (Debian 15.7-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: access_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.access_tokens (
    user_id bigint,
    refresh_token text
);


ALTER TABLE public.access_tokens OWNER TO postgres;

--
-- Name: afk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.afk (
    guild_id bigint,
    user_id bigint,
    reason text,
    "time" timestamp with time zone
);


ALTER TABLE public.afk OWNER TO postgres;

--
-- Name: aliases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aliases (
    guild_id bigint NOT NULL,
    command text NOT NULL,
    alias text NOT NULL
);


ALTER TABLE public.aliases OWNER TO postgres;

--
-- Name: anti_join; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anti_join (
    guild_id bigint,
    rate integer
);


ALTER TABLE public.anti_join OWNER TO postgres;

--
-- Name: antinuke; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.antinuke (
    guild_id bigint,
    configured text,
    owner_id bigint,
    whitelisted jsonb,
    admins jsonb,
    logs bigint
);


ALTER TABLE public.antinuke OWNER TO postgres;

--
-- Name: antinuke_modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.antinuke_modules (
    guild_id bigint,
    module text,
    punishment text,
    threshold integer
);


ALTER TABLE public.antinuke_modules OWNER TO postgres;

--
-- Name: antispam; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.antispam (
    guild_id bigint,
    rate integer,
    timeout bigint,
    users text,
    channels text
);


ALTER TABLE public.antispam OWNER TO postgres;

--
-- Name: api_key; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_key (
    key text,
    user_id bigint,
    role text
);


ALTER TABLE public.api_key OWNER TO postgres;

--
-- Name: archive; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.archive (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.archive OWNER TO postgres;

--
-- Name: archive_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.archive_category (
    guild_id bigint NOT NULL,
    category_id bigint NOT NULL
);


ALTER TABLE public.archive_category OWNER TO postgres;

--
-- Name: authorize; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorize (
    guild_id bigint,
    user_id bigint,
    till timestamp with time zone,
    transfers integer
);


ALTER TABLE public.authorize OWNER TO postgres;

--
-- Name: autopfp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autopfp (
    guild_id bigint NOT NULL,
    type text NOT NULL,
    category text NOT NULL,
    channel_id bigint
);


ALTER TABLE public.autopfp OWNER TO postgres;

--
-- Name: autoping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoping (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.autoping OWNER TO postgres;

--
-- Name: autoreact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoreact (
    guild_id bigint NOT NULL,
    trigger text NOT NULL,
    reactions text NOT NULL
);


ALTER TABLE public.autoreact OWNER TO postgres;

--
-- Name: autoreacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoreacts (
    guild_id bigint NOT NULL,
    trigger text NOT NULL,
    reaction text NOT NULL
);


ALTER TABLE public.autoreacts OWNER TO postgres;

--
-- Name: autoresponder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoresponder (
    guild_id bigint,
    trigger text,
    response text,
    strict boolean DEFAULT true
);


ALTER TABLE public.autoresponder OWNER TO postgres;

--
-- Name: autorole; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autorole (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.autorole OWNER TO postgres;

--
-- Name: avatar_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.avatar_history (
    user_id text NOT NULL,
    name text,
    avatars text,
    background text
);


ALTER TABLE public.avatar_history OWNER TO postgres;

--
-- Name: avatar_urls; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.avatar_urls (
    user_id bigint,
    token text,
    data bytea
);


ALTER TABLE public.avatar_urls OWNER TO postgres;

--
-- Name: avatars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.avatars (
    user_id bigint NOT NULL,
    name text NOT NULL,
    avatar text NOT NULL,
    key text NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.avatars OWNER TO postgres;

--
-- Name: bday; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bday (
    user_id bigint,
    month integer,
    day integer
);


ALTER TABLE public.bday OWNER TO postgres;

--
-- Name: birthday; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.birthday (
    user_id bigint,
    bday timestamp with time zone,
    said text
);


ALTER TABLE public.birthday OWNER TO postgres;

--
-- Name: blacklist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blacklist (
    id bigint NOT NULL,
    type text NOT NULL
);


ALTER TABLE public.blacklist OWNER TO postgres;

--
-- Name: boost; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.boost (
    guild_id bigint,
    channel_id bigint,
    message text
);


ALTER TABLE public.boost OWNER TO postgres;

--
-- Name: booster_module; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booster_module (
    guild_id bigint,
    base bigint
);


ALTER TABLE public.booster_module OWNER TO postgres;

--
-- Name: booster_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booster_roles (
    guild_id bigint,
    user_id bigint,
    role_id bigint
);


ALTER TABLE public.booster_roles OWNER TO postgres;

--
-- Name: br_award; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.br_award (
    guild_id bigint,
    role_id bigint
);


ALTER TABLE public.br_award OWNER TO postgres;

--
-- Name: bumpreminder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bumpreminder (
    guild_id bigint,
    channel_id bigint,
    user_id bigint,
    thankyou text,
    reminder text,
    "time" timestamp with time zone
);


ALTER TABLE public.bumpreminder OWNER TO postgres;

--
-- Name: confess; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.confess (
    guild_id bigint,
    channel_id bigint,
    confession integer
);


ALTER TABLE public.confess OWNER TO postgres;

--
-- Name: confess_members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.confess_members (
    guild_id bigint,
    user_id bigint,
    confession integer
);


ALTER TABLE public.confess_members OWNER TO postgres;

--
-- Name: confess_mute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.confess_mute (
    guild_id bigint,
    user_id bigint
);


ALTER TABLE public.confess_mute OWNER TO postgres;

--
-- Name: counters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.counters (
    guild_id bigint,
    channel_type text,
    channel_id bigint,
    channel_name text,
    module text
);


ALTER TABLE public.counters OWNER TO postgres;

--
-- Name: disablecmd; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disablecmd (
    guild_id bigint,
    cmd text
);


ALTER TABLE public.disablecmd OWNER TO postgres;

--
-- Name: disablemodule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disablemodule (
    guild_id bigint NOT NULL,
    module text NOT NULL
);


ALTER TABLE public.disablemodule OWNER TO postgres;

--
-- Name: donor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.donor (
    user_id bigint,
    since bigint,
    status text
);


ALTER TABLE public.donor OWNER TO postgres;

--
-- Name: economy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.economy (
    user_id bigint,
    cash double precision,
    card double precision,
    daily bigint,
    dice bigint
);


ALTER TABLE public.economy OWNER TO postgres;

--
-- Name: error_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.error_codes (
    code character varying(30) NOT NULL,
    info json
);


ALTER TABLE public.error_codes OWNER TO postgres;

--
-- Name: fake_perms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fake_perms (
    guild_id bigint,
    role_id bigint,
    perms text
);


ALTER TABLE public.fake_perms OWNER TO postgres;

--
-- Name: filter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.filter (
    guild_id bigint,
    mode text,
    rule_id bigint
);


ALTER TABLE public.filter OWNER TO postgres;

--
-- Name: force_nick; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.force_nick (
    guild_id bigint,
    user_id bigint,
    nickname text
);


ALTER TABLE public.force_nick OWNER TO postgres;

--
-- Name: gamestats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gamestats (
    user_id bigint,
    game text,
    wins integer,
    loses integer,
    total integer
);


ALTER TABLE public.gamestats OWNER TO postgres;

--
-- Name: give_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.give_roles (
    guild_id bigint,
    role_id bigint
);


ALTER TABLE public.give_roles OWNER TO postgres;

--
-- Name: giveaway; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.giveaway (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    winners integer,
    members text,
    finish timestamp with time zone,
    host bigint,
    title text
);


ALTER TABLE public.giveaway OWNER TO postgres;

--
-- Name: global_disabled_cmds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.global_disabled_cmds (
    cmd character varying(30) NOT NULL,
    disabled boolean,
    disabled_by text
);


ALTER TABLE public.global_disabled_cmds OWNER TO postgres;

--
-- Name: globalban; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.globalban (
    user_id bigint,
    reason text
);


ALTER TABLE public.globalban OWNER TO postgres;

--
-- Name: gw_ended; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gw_ended (
    channel_id bigint,
    message_id bigint,
    members text
);


ALTER TABLE public.gw_ended OWNER TO postgres;

--
-- Name: hardban; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hardban (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    reason text,
    moderator_id bigint NOT NULL
);


ALTER TABLE public.hardban OWNER TO postgres;

--
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id text,
    url text
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: imgonly; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.imgonly (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.imgonly OWNER TO postgres;

--
-- Name: invoke; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoke (
    guild_id bigint,
    command text,
    embed text
);


ALTER TABLE public.invoke OWNER TO postgres;

--
-- Name: jail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jail (
    guild_id bigint,
    channel_id bigint,
    role_id bigint
);


ALTER TABLE public.jail OWNER TO postgres;

--
-- Name: jail_members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jail_members (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    roles text,
    jailed_at timestamp with time zone
);


ALTER TABLE public.jail_members OWNER TO postgres;

--
-- Name: lastfm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lastfm (
    user_id bigint,
    username text
);


ALTER TABLE public.lastfm OWNER TO postgres;

--
-- Name: lastfm_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lastfm_users (
    id integer,
    discord_user_id bigint,
    username character varying(255),
    session_key character varying(255)
);


ALTER TABLE public.lastfm_users OWNER TO postgres;

--
-- Name: lastfmcc; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lastfmcc (
    user_id bigint,
    command text
);


ALTER TABLE public.lastfmcc OWNER TO postgres;

--
-- Name: leave; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leave (
    guild_id bigint,
    channel_id bigint,
    message text
);


ALTER TABLE public.leave OWNER TO postgres;

--
-- Name: level_rewards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.level_rewards (
    guild_id bigint,
    level integer,
    role_id bigint
);


ALTER TABLE public.level_rewards OWNER TO postgres;

--
-- Name: level_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.level_user (
    guild_id bigint,
    user_id bigint,
    xp integer,
    level integer,
    target_xp bigint
);


ALTER TABLE public.level_user OWNER TO postgres;

--
-- Name: leveling; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leveling (
    guild_id bigint,
    channel_id bigint,
    message text,
    booster_boost text
);


ALTER TABLE public.leveling OWNER TO postgres;

--
-- Name: lfmode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lfmode (
    user_id bigint,
    mode text
);


ALTER TABLE public.lfmode OWNER TO postgres;

--
-- Name: lfreactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lfreactions (
    user_id bigint,
    reactions text
);


ALTER TABLE public.lfreactions OWNER TO postgres;

--
-- Name: lock_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lock_role (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.lock_role OWNER TO postgres;

--
-- Name: lockdown_ignore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lockdown_ignore (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.lockdown_ignore OWNER TO postgres;

--
-- Name: logging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logging (
    guild_id bigint NOT NULL,
    messages bigint,
    guild bigint,
    roles bigint,
    channels bigint,
    members bigint
);


ALTER TABLE public.logging OWNER TO postgres;

--
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    key text NOT NULL,
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    author jsonb DEFAULT '{}'::jsonb NOT NULL,
    logs jsonb DEFAULT '{}'::jsonb NOT NULL
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- Name: marry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marry (
    author bigint,
    soulmate bigint,
    "time" bigint
);


ALTER TABLE public.marry OWNER TO postgres;

--
-- Name: number_counter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.number_counter (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    last_counted bigint,
    current_number integer
);


ALTER TABLE public.number_counter OWNER TO postgres;

--
-- Name: opened_tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opened_tickets (
    guild_id bigint,
    channel_id bigint,
    user_id bigint
);


ALTER TABLE public.opened_tickets OWNER TO postgres;

--
-- Name: prefixes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prefixes (
    guild_id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.prefixes OWNER TO postgres;

--
-- Name: reactionrole; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reactionrole (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    emoji text,
    role_id bigint
);


ALTER TABLE public.reactionrole OWNER TO postgres;

--
-- Name: reminder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reminder (
    user_id bigint,
    channel_id bigint,
    guild_id bigint,
    date timestamp with time zone,
    task text
);


ALTER TABLE public.reminder OWNER TO postgres;

--
-- Name: reskin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reskin (
    user_id bigint,
    toggled boolean,
    name text,
    avatar text
);


ALTER TABLE public.reskin OWNER TO postgres;

--
-- Name: reskin_enabled; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reskin_enabled (
    guild_id bigint
);


ALTER TABLE public.reskin_enabled OWNER TO postgres;

--
-- Name: restore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restore (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    roles text
);


ALTER TABLE public.restore OWNER TO postgres;

--
-- Name: restrictcommand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restrictcommand (
    guild_id bigint NOT NULL,
    command text NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.restrictcommand OWNER TO postgres;

--
-- Name: seen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seen (
    user_id bigint,
    guild_id bigint,
    "time" timestamp with time zone
);


ALTER TABLE public.seen OWNER TO postgres;

--
-- Name: selfprefix; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.selfprefix (
    user_id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.selfprefix OWNER TO postgres;

--
-- Name: spotify; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spotify (
    user_id bigint,
    access_token text
);


ALTER TABLE public.spotify OWNER TO postgres;

--
-- Name: starboard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.starboard (
    guild_id bigint,
    channel_id bigint,
    emoji text,
    count integer,
    role_id bigint
);


ALTER TABLE public.starboard OWNER TO postgres;

--
-- Name: starboard_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.starboard_messages (
    guild_id bigint,
    channel_id bigint,
    message_id bigint,
    starboard_message_id bigint
);


ALTER TABLE public.starboard_messages OWNER TO postgres;

--
-- Name: stickymessage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stickymessage (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.stickymessage OWNER TO postgres;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    guild_id bigint NOT NULL,
    author_id bigint NOT NULL,
    name text NOT NULL,
    response text NOT NULL
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- Name: ticket_topics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticket_topics (
    guild_id bigint,
    name text,
    description text
);


ALTER TABLE public.ticket_topics OWNER TO postgres;

--
-- Name: tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tickets (
    guild_id bigint,
    open_embed text,
    category_id bigint,
    logs bigint,
    support_id bigint
);


ALTER TABLE public.tickets OWNER TO postgres;

--
-- Name: timezone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.timezone (
    user_id bigint,
    zone text
);


ALTER TABLE public.timezone OWNER TO postgres;

--
-- Name: trial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trial (
    guild_id bigint NOT NULL,
    end_date integer
);


ALTER TABLE public.trial OWNER TO postgres;

--
-- Name: trials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trials (
    guild_id bigint NOT NULL,
    expires bigint NOT NULL
);


ALTER TABLE public.trials OWNER TO postgres;

--
-- Name: username_track; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.username_track (
    guild_id bigint,
    webhook_url text
);


ALTER TABLE public.username_track OWNER TO postgres;

--
-- Name: usernames; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usernames (
    user_id bigint,
    user_name text,
    "time" bigint
);


ALTER TABLE public.usernames OWNER TO postgres;

--
-- Name: vcs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vcs (
    user_id bigint,
    voice bigint
);


ALTER TABLE public.vcs OWNER TO postgres;

--
-- Name: vm_buttons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vm_buttons (
    guild_id bigint,
    action text,
    label text,
    emoji text,
    style text
);


ALTER TABLE public.vm_buttons OWNER TO postgres;

--
-- Name: voicemaster; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.voicemaster (
    guild_id bigint,
    channel_id bigint,
    interface_id bigint
);


ALTER TABLE public.voicemaster OWNER TO postgres;

--
-- Name: warns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.warns (
    guild_id bigint,
    user_id bigint,
    author_id bigint,
    "time" text,
    reason text
);


ALTER TABLE public.warns OWNER TO postgres;

--
-- Name: webhook; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.webhook (
    guild_id bigint,
    code text,
    url text,
    channel text,
    name text,
    avatar text
);


ALTER TABLE public.webhook OWNER TO postgres;

--
-- Name: welcome; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welcome (
    guild_id bigint,
    channel_id bigint,
    message text
);


ALTER TABLE public.welcome OWNER TO postgres;

--
-- Name: whitelist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whitelist (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.whitelist OWNER TO postgres;

--
-- Name: whitelist_state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.whitelist_state (
    guild_id bigint NOT NULL,
    embed text
);


ALTER TABLE public.whitelist_state OWNER TO postgres;

--
-- Name: xray; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xray (
    guild_id bigint,
    target_id bigint,
    webhook_url text
);


ALTER TABLE public.xray OWNER TO postgres;

--
-- Data for Name: access_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.access_tokens (user_id, refresh_token) FROM stdin;
\.


--
-- Data for Name: afk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.afk (guild_id, user_id, reason, "time") FROM stdin;
\.


--
-- Data for Name: aliases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aliases (guild_id, command, alias) FROM stdin;
1254536563186991184	antinuke giverole	gr
1254536563186991184	an	
1254536563186991184	antinuke massmention	mm
1254536563186991184	antinuke giverole	gr
1254536563186991184	an kick	k
1254536563186991184	antinuke ban	b
1254536563186991184	antinuke botadd	ba
1254536563186991184	antinuke channeldelete	cd
1254536563186991184	an channelcreate	cc
1254536563186991184	copyembed	ec
1202055026797707316	mute	m
1202055026797707316	mute	to
1202055026797707316	mute	tout
1202055026797707316	kick	k
1202055026797707316	warn	wa
1202055026797707316	ban	b
1202055026797707316	av	pfp
1202055026797707316	banner	bnr
1202055026797707316	sbanner	sbnr
\.


--
-- Data for Name: anti_join; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anti_join (guild_id, rate) FROM stdin;
\.


--
-- Data for Name: antinuke; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.antinuke (guild_id, configured, owner_id, whitelisted, admins, logs) FROM stdin;
1254536563186991184	true	1169601140804042842	[1047630662133350470]	[1047630662133350470]	1269685507198287893
1202055026797707316	true	1208370307551989761	[1157111422598250577]	\N	\N
\.


--
-- Data for Name: antinuke_modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.antinuke_modules (guild_id, module, punishment, threshold) FROM stdin;
1254536563186991184	role giving	strip	0
1254536563186991184	mass mention	strip	\N
1254536563186991184	kick	kick	20
1254536563186991184	ban	kick	20
1254536563186991184	bot add	strip	\N
1254536563186991184	channel delete	strip	15
1254536563186991184	role delete	strip	15
1254536563186991184	spammer	kick	\N
1254536563186991184	channel create	ban	15
1254536563186991184	new accounts	kick	604800
1202055026797707316	role delete	strip	1
1202055026797707316	ban	strip	10
1202055026797707316	channel create	strip	1
1202055026797707316	role create	strip	1
\.


--
-- Data for Name: antispam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.antispam (guild_id, rate, timeout, users, channels) FROM stdin;
\.


--
-- Data for Name: api_key; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.api_key (key, user_id, role) FROM stdin;
gFAM9t!&zKlt49V6duic6@1s0ZkyH3	598125772754124823	master
\.


--
-- Data for Name: archive; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.archive (guild_id, channel_id) FROM stdin;
\.


--
-- Data for Name: archive_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.archive_category (guild_id, category_id) FROM stdin;
\.


--
-- Data for Name: authorize; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authorize (guild_id, user_id, till, transfers) FROM stdin;
\.


--
-- Data for Name: autopfp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autopfp (guild_id, type, category, channel_id) FROM stdin;
1254536563186991184	pfps	random	1269682188270571634
1254536563186991184	pfps	roadmen	1269682188270571634
1254536563186991184	pfps	girl	1269682188270571634
1254536563186991184	pfps	egirl	1269682188270571634
1254536563186991184	pfps	anime	1269682188270571634
1254536563186991184	pfps	ceinory	1269682188270571634
1202055026797707316	pfps	random	1269988512153731195
1202055026797707316	banners	random	1269988513596833943
\.


--
-- Data for Name: autoping; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoping (guild_id, channel_id, message) FROM stdin;
\.


--
-- Data for Name: autoreact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoreact (guild_id, trigger, reactions) FROM stdin;
1202055026797707316	skull	["\\ud83d\\udc80"]
1202055026797707316	sob	["\\ud83d\\ude2d"]
1202055026797707316	faggot	["\\ud83c\\udf08"]
1202055026797707316	fagot	["\\ud83c\\udf08"]
1202055026797707316	nigga	["\\ud83d\\udc80"]
1202055026797707316	fag	["\\ud83c\\udf08"]
1202055026797707316	fagg	["\\ud83c\\udf08"]
1202055026797707316	fags	["\\ud83c\\udf08"]
1202055026797707316	faggs	["\\ud83c\\udf08"]
1202055026797707316	cum	["<a:shot:1270007392037240996>"]
\.


--
-- Data for Name: autoreacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoreacts (guild_id, trigger, reaction) FROM stdin;
\.


--
-- Data for Name: autoresponder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoresponder (guild_id, trigger, response, strict) FROM stdin;
1254536563186991184	pic perms	to get pic perms boost /higher	t
1202055026797707316	nigger	kill all niggers	t
1202055026797707316	kys	keep yourself safe	t
1202055026797707316	engrave	<@1157111422598250577>	t
1202055026797707316	war.dev	<@1157111422598250577>	t
\.


--
-- Data for Name: autorole; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autorole (guild_id, role_id) FROM stdin;
1202055026797707316	1269988406604206120
1202055026797707316	1269988404825821245
\.


--
-- Data for Name: avatar_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.avatar_history (user_id, name, avatars, background) FROM stdin;
\.


--
-- Data for Name: avatar_urls; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.avatar_urls (user_id, token, data) FROM stdin;
\.


--
-- Data for Name: avatars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.avatars (user_id, name, avatar, key, "timestamp") FROM stdin;
\.


--
-- Data for Name: bday; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bday (user_id, month, day) FROM stdin;
\.


--
-- Data for Name: birthday; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.birthday (user_id, bday, said) FROM stdin;
\.


--
-- Data for Name: blacklist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blacklist (id, type) FROM stdin;
\.


--
-- Data for Name: boost; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.boost (guild_id, channel_id, message) FROM stdin;
1202055026797707316	1269988490737745993	ty 4 boostin {user.mention}
\.


--
-- Data for Name: booster_module; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booster_module (guild_id, base) FROM stdin;
1202055026797707316	1202057666919419995
\.


--
-- Data for Name: booster_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booster_roles (guild_id, user_id, role_id) FROM stdin;
\.


--
-- Data for Name: br_award; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.br_award (guild_id, role_id) FROM stdin;
\.


--
-- Data for Name: bumpreminder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bumpreminder (guild_id, channel_id, user_id, thankyou, reminder, "time") FROM stdin;
\.


--
-- Data for Name: confess; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.confess (guild_id, channel_id, confession) FROM stdin;
\.


--
-- Data for Name: confess_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.confess_members (guild_id, user_id, confession) FROM stdin;
\.


--
-- Data for Name: confess_mute; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.confess_mute (guild_id, user_id) FROM stdin;
\.


--
-- Data for Name: counters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.counters (guild_id, channel_type, channel_id, channel_name, module) FROM stdin;
1202055026797707316	voice	1270046118801182823	{target}	humans
\.


--
-- Data for Name: disablecmd; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.disablecmd (guild_id, cmd) FROM stdin;
\.


--
-- Data for Name: disablemodule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.disablemodule (guild_id, module) FROM stdin;
\.


--
-- Data for Name: donor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.donor (user_id, since, status) FROM stdin;
214753146512080907	1722717439	purchased
1169601140804042842	1722717493	purchased
598125772754124823	1722798442	purchased
\.


--
-- Data for Name: economy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.economy (user_id, cash, card, daily, dice) FROM stdin;
840439255708991508	1576.91	0	1722847700	\N
1169601140804042842	0	1766.81	1722965587	1722879216
\.


--
-- Data for Name: error_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.error_codes (code, info) FROM stdin;
CZCbKh	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722636183:R>", "error": "Command raised an exception: Error: BrowserType.launch: Executable doesn't exist at /home/evict/.cache/ms-playwright/chromium-1124/chrome-linux/chrome\\n\\u2554\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2557\\n\\u2551 Looks like Playwright was just installed or updated.       \\u2551\\n\\u2551 Please run the following command to download new browsers: \\u2551\\n\\u2551                                                            \\u2551\\n\\u2551     playwright install                                     \\u2551\\n\\u2551                                                            \\u2551\\n\\u2551 <3 Playwright Team                                         \\u2551\\n\\u255a\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u255d", "code": "CZCbKh", "command": "screenshot"}
y9fs0D	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722646407:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "y9fs0D", "command": "jishaku shell"}
AIo5nh	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722649194:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "AIo5nh", "command": "help"}
t3KZdO	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722649831:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "t3KZdO", "command": "help"}
sCjDdD	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650120:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "sCjDdD", "command": "help"}
OhGcQQ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650378:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: Must be between 1 and 25 in length.", "code": "OhGcQQ", "command": "help"}
JaKvgv	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650547:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "JaKvgv", "command": "help"}
omcevA	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722650571:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "omcevA", "command": "help"}
TXY7cj	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650576:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "TXY7cj", "command": "help"}
TDflsP	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650641:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: This field is required", "code": "TDflsP", "command": "help"}
yHpThO	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650767:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: Must be between 1 and 25 in length.", "code": "yHpThO", "command": "help"}
9TV0GV	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650803:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: Must be between 1 and 25 in length.", "code": "9TV0GV", "command": "help"}
TiIB8f	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722650857:R>", "error": "Command raised an exception: NameError: name 'Button' is not defined", "code": "TiIB8f", "command": "help"}
htWUqV	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722651009:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: Must be between 1 and 25 in length.", "code": "htWUqV", "command": "help"}
dsSVEs	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722651300:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn components.0.components.0.options: Must be between 1 and 25 in length.", "code": "dsSVEs", "command": "help"}
oKMAAv	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722651578:R>", "error": "Command raised an exception: RecursionError: maximum recursion depth exceeded in comparison", "code": "oKMAAv", "command": "help"}
gbCO3d	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722651670:R>", "error": "Command raised an exception: RecursionError: maximum recursion depth exceeded in comparison", "code": "gbCO3d", "command": "help"}
ONwlBb	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652002:R>", "error": "Command raised an exception: TypeError: 'PretendContext' object is not callable", "code": "ONwlBb", "command": "help"}
J50G6Q	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652161:R>", "error": "Command raised an exception: NoNodesAvailable: There are no nodes available.", "code": "J50G6Q", "command": "play"}
WfDJ2t	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652261:R>", "error": "Command raised an exception: KeyError: 'hits'", "code": "WfDJ2t", "command": "song"}
0tsQ7c	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652281:R>", "error": "Command raised an exception: KeyError: 'hits'", "code": "0tsQ7c", "command": "song"}
dbec8t	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652464:R>", "error": "Command raised an exception: KeyError: 'hits'", "code": "dbec8t", "command": "song"}
NvywFr	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652490:R>", "error": "Command raised an exception: KeyError: 'hits'", "code": "NvywFr", "command": "song"}
5B1OdB	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722652524:R>", "error": "Command raised an exception: KeyError: 'hits'", "code": "5B1OdB", "command": "song"}
jv9MSD	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722653674:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "jv9MSD", "command": "bans"}
lRek10	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722654030:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "lRek10", "command": "help"}
9wCedB	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722654590:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "9wCedB", "command": "help"}
D2D13Z	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722654663:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "D2D13Z", "command": "help"}
dTfVib	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722654875:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "dTfVib", "command": "help"}
1fhUjX	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722655089:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "1fhUjX", "command": "help"}
GwtwCO	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722655480:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "GwtwCO", "command": "help"}
eMNo6A	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722655610:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "eMNo6A", "command": "help"}
fGsgtV	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722655696:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "fGsgtV", "command": "help"}
Xinz3H	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722656042:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "Xinz3H", "command": "help"}
FsmOTT	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722656079:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "FsmOTT", "command": "help"}
Pbu6cc	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659362:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "Pbu6cc", "command": "help"}
iJNJQs	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659489:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "iJNJQs", "command": "help"}
F06Mdc	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659537:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "F06Mdc", "command": "help"}
ZR4HY0	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659685:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "ZR4HY0", "command": "help"}
McZArt	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659767:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "McZArt", "command": "help"}
YCsk4D	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659873:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "YCsk4D", "command": "help"}
x7fSA0	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722659877:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "x7fSA0", "command": "help"}
z5qTmr	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722659904:R>", "error": "Command raised an exception: TypeError: Paginator.__init__() missing 1 required positional argument: 'embeds'", "code": "z5qTmr", "command": "help"}
rueZQN	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722659984:R>", "error": "Command raised an exception: AttributeError: 'PretendHelp' object has no attribute 'paginator'", "code": "rueZQN", "command": "help"}
CATCvf	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722663034:R>", "error": "Command raised an exception: NoNodesAvailable: There are no nodes available.", "code": "CATCvf", "command": "play"}
NOMZbI	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722665980:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "NOMZbI", "command": "bans"}
pzu5WJ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722701197:R>", "error": "Command raised an exception: NoNodesAvailable: There are no nodes available.", "code": "pzu5WJ", "command": "play"}
WVwtgA	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722701210:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "WVwtgA", "command": "jishaku shell"}
fMkfbl	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 1169601140804042842, "timestamp": "<t:1722702266:R>", "error": "Command raised an exception: PermissionError: [Errno 13] Permission denied: '/root/PretendImages/Banners/'", "code": "fMkfbl", "command": "report"}
OA9QWT	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722702666:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "OA9QWT", "command": "timezone list"}
7ED2yO	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722703318:R>", "error": "Command raised an exception: TypeError: Webhook.send() got an unexpected keyword argument 'reference'", "code": "7ED2yO", "command": "reskin name"}
Rtwikh	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722703557:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"name\\" of relation \\"reskin\\" does not exist", "code": "Rtwikh", "command": "reskin name"}
TNOFc6	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 987183275560820806, "timestamp": "<t:1722703683:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin\\" does not exist", "code": "TNOFc6", "command": "reskin name"}
wZobnM	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 987183275560820806, "timestamp": "<t:1722703696:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin\\" does not exist", "code": "wZobnM", "command": "help"}
xeROCU	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722703712:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin\\" does not exist", "code": "xeROCU", "command": "help"}
owGGZ6	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722703757:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin\\" does not exist", "code": "owGGZ6", "command": "help"}
6X93GX	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 987183275560820806, "timestamp": "<t:1722703823:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin\\" does not exist", "code": "6X93GX", "command": "help"}
1zCrnu	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722703985:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "1zCrnu", "command": "jishaku shell"}
Cb561m	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722704005:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'success'", "code": "Cb561m", "command": "reskin name"}
CfYky5	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722704013:R>", "error": "Command raised an exception: KeyError: 'avatar_url'", "code": "CfYky5", "command": "help"}
40vmJN	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722704121:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'webhook'", "code": "40vmJN", "command": "help"}
rYW62K	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722704125:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'webhook'", "code": "rYW62K", "command": "jishaku"}
WTGXz7	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722704411:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "WTGXz7", "command": "jishaku shell"}
8f4Ax1	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 987183275560820806, "timestamp": "<t:1722704472:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'success'", "code": "8f4Ax1", "command": "reskin disable"}
few66z	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722705527:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "few66z", "command": "jishaku shell"}
xookJk	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722705536:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"reskin_enabled\\" does not exist", "code": "xookJk", "command": "help"}
NE66Lx	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722705571:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "NE66Lx", "command": "jishaku shell"}
lt3rLg	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722708299:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "lt3rLg", "command": "jishaku shell"}
z6Kcil	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722708834:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "z6Kcil", "command": "jishaku shell"}
BshOZ3	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722708880:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "BshOZ3", "command": "jishaku shell"}
b4LbXt	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709019:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "b4LbXt", "command": "jishaku shell"}
g19b4p	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709074:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "g19b4p", "command": "bans"}
5R3aaN	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709258:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'success'", "code": "5R3aaN", "command": "reskin name"}
v1H6Yp	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709384:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "v1H6Yp", "command": "bans"}
UsPYO5	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709433:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "UsPYO5", "command": "bans"}
h5c1wp	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709448:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "h5c1wp", "command": "bans"}
cYTlCQ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709494:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "cYTlCQ", "command": "bans"}
os6FG8	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709572:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "os6FG8", "command": "timezone list"}
KTrlej	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709599:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "KTrlej", "command": "timezone list"}
cq65DZ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722709965:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "cq65DZ", "command": "fyp"}
ZVWJco	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722710053:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "ZVWJco", "command": "donators"}
L0eQ3h	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722710107:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "L0eQ3h", "command": "donators"}
3kakm5	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722710788:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "3kakm5", "command": "muted"}
rRvv6e	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722710887:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'edit'", "code": "rRvv6e", "command": "shazam"}
R8zPNJ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722712393:R>", "error": "Command raised an exception: AttributeError: 'Fun' object has no attribute 'session'", "code": "R8zPNJ", "command": "fyp"}
pcuPfX	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722712429:R>", "error": "Command raised an exception: AttributeError: 'Fun' object has no attribute 'session'", "code": "pcuPfX", "command": "fyp"}
qGm2AE	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722712576:R>", "error": "Command raised an exception: AttributeError: 'Fun' object has no attribute 'session'", "code": "qGm2AE", "command": "fyp"}
8dgdo1	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722712949:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "8dgdo1", "command": "jishaku shell"}
1leAmw	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722713020:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "1leAmw", "command": "jishaku shell"}
52umbU	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722713054:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "52umbU", "command": "jishaku shell"}
k6YzAk	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722713250:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "k6YzAk", "command": "jishaku shell"}
IqX11u	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 1169601140804042842, "timestamp": "<t:1722716073:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "IqX11u", "command": "nowplaying"}
jVgKik	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716112:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "jVgKik", "command": "donor add"}
v7512E	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716199:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "v7512E", "command": "donor add"}
61HHmP	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716270:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "61HHmP", "command": "donor add"}
L5FUyt	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716486:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "L5FUyt", "command": "donor add"}
9gR8xg	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716598:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "9gR8xg", "command": "donor add"}
jTzZNq	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 1169601140804042842, "timestamp": "<t:1722718499:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "jTzZNq", "command": "nowplaying"}
9rqJGH	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716635:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_member'", "code": "9rqJGH", "command": "donor add"}
3Tp2Qp	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722716748:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_role'", "code": "3Tp2Qp", "command": "donor add"}
akohyQ	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722717046:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_role'", "code": "akohyQ", "command": "donor add"}
h6IE3d	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722717112:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'get_role'", "code": "h6IE3d", "command": "donor add"}
GEKKeW	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722717131:R>", "error": "Command raised an exception: AttributeError: 'int' object has no attribute 'id'", "code": "GEKKeW", "command": "donor add"}
Boislv	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722718051:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "Boislv", "command": "nowplaying"}
1a78v9	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722718189:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "1a78v9", "command": "nowplaying"}
pboADt	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 971464344749629512, "timestamp": "<t:1722718262:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'title'", "code": "pboADt", "command": "queue"}
fMkpCm	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 1169601140804042842, "timestamp": "<t:1722718956:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "fMkpCm", "command": "nowplaying"}
TmVcKk	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722719890:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "TmVcKk", "command": "nowplaying"}
KFL0hO	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722719920:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "KFL0hO", "command": "nowplaying"}
w5SbtV	{"guild_id": 1266750786478805023, "channel_id": 1266751590660968499, "user_id": 1169601140804042842, "timestamp": "<t:1722720344:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "w5SbtV", "command": "nowplaying"}
5PyJsR	{"guild_id": 950153022405763124, "channel_id": 1269400788342669336, "user_id": 1169601140804042842, "timestamp": "<t:1722720465:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "5PyJsR", "command": "nowplaying"}
2zoY0J	{"guild_id": 950153022405763124, "channel_id": 1269400788342669336, "user_id": 598125772754124823, "timestamp": "<t:1722720473:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "2zoY0J", "command": "jishaku shell"}
v5gWcV	{"guild_id": 950153022405763124, "channel_id": 1269400788342669336, "user_id": 598125772754124823, "timestamp": "<t:1722720544:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "v5gWcV", "command": "jishaku shell"}
1wh67w	{"guild_id": 950153022405763124, "channel_id": 1269400788342669336, "user_id": 1169601140804042842, "timestamp": "<t:1722720553:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "1wh67w", "command": "nowplaying"}
4jxtfo	{"guild_id": 950153022405763124, "channel_id": 1269400788342669336, "user_id": 1169601140804042842, "timestamp": "<t:1722720796:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "4jxtfo", "command": "nowplaying"}
neIeUx	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722725448:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "neIeUx", "command": "nowplaying"}
htwViq	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722725473:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "htwViq", "command": "nowplaying"}
sgYBsE	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722725742:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "sgYBsE", "command": "jishaku shell"}
5Bp1YT	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722725807:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "5Bp1YT", "command": "jishaku shell"}
kJfH1Z	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722725893:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "kJfH1Z", "command": "jishaku shell"}
cG7prA	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722741640:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "cG7prA", "command": "jishaku shell"}
bZplCy	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722743216:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "bZplCy", "command": "stickers"}
gyTpvG	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722745261:R>", "error": "Command raised an exception: Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user", "code": "gyTpvG", "command": "apikey add"}
MMGQSH	{"guild_id": 1268777695244980389, "channel_id": 1268777695244980392, "user_id": 598125772754124823, "timestamp": "<t:1722750339:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "MMGQSH", "command": "jishaku shell"}
Q80Jrp	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722762779:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "Q80Jrp", "command": "nowplaying"}
ObcC14	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763274:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "ObcC14", "command": "nowplaying"}
nKPa4b	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763323:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "nKPa4b", "command": "nowplaying"}
o7Par8	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763357:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "o7Par8", "command": "nowplaying"}
BIvwmo	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763384:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "BIvwmo", "command": "nowplaying"}
yUuPt1	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722763595:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "yUuPt1", "command": "nowplaying"}
85j7nQ	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763669:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "85j7nQ", "command": "nowplaying"}
TvQpEC	{"guild_id": 1268137490011656213, "channel_id": 1269394377122512916, "user_id": 1169601140804042842, "timestamp": "<t:1722763930:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "TvQpEC", "command": "nowplaying"}
Ngo3cx	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722764452:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "Ngo3cx", "command": "nowplaying"}
43DX94	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722765073:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "43DX94", "command": "nowplaying"}
X5kiAh	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722764839:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "X5kiAh", "command": "nowplaying"}
xCvYSC	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722766553:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "xCvYSC", "command": "nowplaying"}
XsU8fc	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722784783:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "XsU8fc", "command": "nowplaying"}
EKvj2O	{"guild_id": 1254536563186991184, "channel_id": 1269682186039201837, "user_id": 1169601140804042842, "timestamp": "<t:1722786818:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'edit'", "code": "EKvj2O", "command": "role humans"}
mwGYsc	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722788907:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.name: This field is required\\nIn embeds.0.fields.0.value: This field is required", "code": "mwGYsc", "command": "createembed"}
4rietS	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789054:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.name: This field is required\\nIn embeds.0.fields.0.value: This field is required", "code": "4rietS", "command": "createembed"}
966HsS	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789064:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.value: This field is required", "code": "966HsS", "command": "createembed"}
NCgEe9	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789178:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.value: This field is required", "code": "NCgEe9", "command": "createembed"}
eCaJVa	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789207:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.value: This field is required", "code": "eCaJVa", "command": "createembed"}
6FucB0	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789287:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.value: This field is required", "code": "6FucB0", "command": "createembed"}
QoU1Vq	{"guild_id": 1254536563186991184, "channel_id": 1269682203827109999, "user_id": 1169601140804042842, "timestamp": "<t:1722789293:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn embeds.0.fields.0.value: This field is required", "code": "QoU1Vq", "command": "createembed"}
8U5J74	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722792482:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "8U5J74", "command": "nowplaying"}
af18ps	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722792674:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "af18ps", "command": "nowplaying"}
fzoNJP	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722792938:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'edit'", "code": "fzoNJP", "command": "lastfm set"}
aQ3QMp	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722792943:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'edit'", "code": "aQ3QMp", "command": "lastfm set"}
aMB8wX	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722792950:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "aMB8wX", "command": "nowplaying"}
4NQiyz	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793020:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'add_reaction'", "code": "4NQiyz", "command": "nowplaying"}
x3ZMGr	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793146:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "x3ZMGr", "command": "reskin avatar"}
4MsMMD	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793151:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "4MsMMD", "command": "reskin avatar"}
WqPkGW	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793161:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "WqPkGW", "command": "help"}
0hWXxw	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793219:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "0hWXxw", "command": "help"}
TvZEex	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797421:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" does not exist", "code": "TvZEex", "command": "nowplaying"}
JiNKOk	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793238:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "JiNKOk", "command": "help"}
3GxzJT	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793276:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "3GxzJT", "command": "nowplaying"}
oecQ6b	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793296:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "oecQ6b", "command": "nowplaying"}
xfq45L	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793278:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "xfq45L", "command": "nowplaying"}
XfXAZd	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722794194:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "XfXAZd", "command": "jishaku shell"}
mpmlNn	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793294:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "mpmlNn", "command": "nowplaying"}
vXwAzH	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722793752:R>", "error": "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\\nIn avatar_url: Scheme \\"none\\" is not supported. Scheme must be one of ('http', 'https'). Not a well formed URL.", "code": "vXwAzH", "command": "play"}
bt28Fd	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722794389:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "bt28Fd", "command": "jishaku shell"}
KEpGC2	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795000:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" does not exist", "code": "KEpGC2", "command": "nowplaying"}
uwo3zB	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795054:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"lastfm_users\\" does not exist", "code": "uwo3zB", "command": "nowplaying"}
35yhSx	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795107:R>", "error": "Command raised an exception: UndefinedTableError: missing FROM-clause entry for table \\"public\\"", "code": "35yhSx", "command": "nowplaying"}
SWRrXH	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795142:R>", "error": "Command raised an exception: UndefinedTableError: missing FROM-clause entry for table \\"public\\"", "code": "SWRrXH", "command": "nowplaying"}
cbrKIo	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722795206:R>", "error": "Command raised an exception: UndefinedTableError: missing FROM-clause entry for table \\"public\\"", "code": "cbrKIo", "command": "nowplaying"}
nX4ODA	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795263:R>", "error": "Command raised an exception: UndefinedTableError: missing FROM-clause entry for table \\"public\\"", "code": "nX4ODA", "command": "nowplaying"}
OuAS5D	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722795279:R>", "error": "Command raised an exception: UndefinedTableError: missing FROM-clause entry for table \\"public\\"", "code": "OuAS5D", "command": "nowplaying"}
h8AWYx	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795306:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"lastfm_users\\" does not exist", "code": "h8AWYx", "command": "nowplaying"}
YKibXB	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795761:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "YKibXB", "command": "jishaku shell"}
lCg2t9	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722795942:R>", "error": "Command raised an exception: IndexError: record index out of range", "code": "lCg2t9", "command": "nowplaying"}
1ILVYf	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796129:R>", "error": "Command raised an exception: InterfaceError: the server expects 2 arguments for this query, 1 was passed\\nHINT:  Check the query against the passed list of arguments.", "code": "1ILVYf", "command": "nowplaying"}
Umz7Ye	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796190:R>", "error": "Command raised an exception: UnboundLocalError: cannot access local variable 'user' where it is not associated with a value", "code": "Umz7Ye", "command": "nowplaying"}
vg3qjP	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796287:R>", "error": "Command raised an exception: UnboundLocalError: cannot access local variable 'user' where it is not associated with a value", "code": "vg3qjP", "command": "nowplaying"}
YW0cn0	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796360:R>", "error": "Command raised an exception: UnboundLocalError: cannot access local variable 'user' where it is not associated with a value", "code": "YW0cn0", "command": "nowplaying"}
JF1E2g	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796516:R>", "error": "Command raised an exception: UnboundLocalError: cannot access local variable 'user' where it is not associated with a value", "code": "JF1E2g", "command": "nowplaying"}
SrS9Ez	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796585:R>", "error": "Command raised an exception: TypeError: Invalid variable type: value should be str, int or float, got <Record username='resentdev'> of type <class 'tools.bot.Record'>", "code": "SrS9Ez", "command": "nowplaying"}
pPLz0K	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796933:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "pPLz0K", "command": "nowplaying"}
86SauF	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722796973:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "86SauF", "command": "nowplaying"}
Wfy9y4	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722796974:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "Wfy9y4", "command": "nowplaying"}
llEoYH	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797357:R>", "error": "Command raised an exception: UndefinedTableError: relation \\"lfmode\\" does not exist", "code": "llEoYH", "command": "nowplaying"}
tZzVOz	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797387:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" does not exist", "code": "tZzVOz", "command": "nowplaying"}
0364Ti	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797473:R>", "error": "Command raised an exception: DatatypeMismatchError: argument of WHERE must be type boolean, not type bigint", "code": "0364Ti", "command": "nowplaying"}
dnaFYl	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797507:R>", "error": "Command raised an exception: DatatypeMismatchError: argument of WHERE must be type boolean, not type bigint", "code": "dnaFYl", "command": "nowplaying"}
4HrztV	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722799457:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"discord_user_id\\" does not exist", "code": "4HrztV", "command": "lastfm mode view"}
w8iNjZ	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722797823:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"user_id\\" does not exist", "code": "w8iNjZ", "command": "lastfm user"}
UoQOZr	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722798207:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "UoQOZr", "command": "lastfm spotify"}
yieWtJ	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798221:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "yieWtJ", "command": "lastfm spotify"}
xgrsAd	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798306:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"user_id\\" does not exist", "code": "xgrsAd", "command": "lastfm cover"}
DLPZ9W	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798492:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"embed\\" of relation \\"lfmode\\" does not exist", "code": "DLPZ9W", "command": "lastfm mode set"}
8SI3iw	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798550:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"embed\\" of relation \\"lfmode\\" does not exist", "code": "8SI3iw", "command": "lastfm mode remove"}
H3tVO9	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798878:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "H3tVO9", "command": "nowplaying"}
IS6tgy	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722798840:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "IS6tgy", "command": "nowplaying"}
fD6Ljh	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800004:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "fD6Ljh", "command": "jishaku shell"}
vSTNkx	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800139:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "vSTNkx", "command": "jishaku shell"}
AyhxxO	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800214:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"discord_user_id\\" does not exist", "code": "AyhxxO", "command": "lastfm mode view"}
GmqUg6	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800389:R>", "error": "Command raised an exception: AttributeError: 'Lastfm' object has no attribute 'db'", "code": "GmqUg6", "command": "lastfm mode view"}
vhKkEg	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800425:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "vhKkEg", "command": "lastfm mode view"}
heiRDF	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800734:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "heiRDF", "command": "lastfm mode view"}
0uv5ve	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800759:R>", "error": "Command raised an exception: IndexError: list index out of range", "code": "0uv5ve", "command": "jishaku override"}
lognQY	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800879:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "lognQY", "command": "lastfm mode view"}
oit5h4	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800901:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "oit5h4", "command": "jishaku override"}
paAeAn	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800941:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "paAeAn", "command": "lastfm mode view"}
Ecpl2Z	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722800953:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "Ecpl2Z", "command": "jishaku override"}
KrHFXQ	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722801025:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'lastfm_message'", "code": "KrHFXQ", "command": "lastfm mode view"}
fdC3oG	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722801111:R>", "error": "Command raised an exception: NameError: name 'embed' is not defined", "code": "fdC3oG", "command": "lastfm mode set"}
4SICBK	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722801225:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "4SICBK", "command": "nowplaying"}
WxdyJr	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722802839:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "WxdyJr", "command": "nowplaying"}
nFKmrk	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722803119:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "nFKmrk", "command": "nowplaying"}
wG6b1a	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722803214:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "wG6b1a", "command": "nowplaying"}
Fy27cD	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722803352:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "Fy27cD", "command": "nowplaying"}
257Jik	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722803420:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "257Jik", "command": "nowplaying"}
hNUvFu	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722803500:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "hNUvFu", "command": "nowplaying"}
im5uxk	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722803704:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "im5uxk", "command": "jishaku shell"}
Spo27c	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722803733:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "Spo27c", "command": "nowplaying"}
4DwThh	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722825232:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "4DwThh", "command": "nowplaying"}
hzBeTZ	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722826437:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "hzBeTZ", "command": "nowplaying"}
wo1jrh	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722826465:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "wo1jrh", "command": "nowplaying"}
CuZLJ3	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722826802:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "CuZLJ3", "command": "nowplaying"}
a5yWBS	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722827289:R>", "error": "Command raised an exception: ValueError: params cannot be None", "code": "a5yWBS", "command": "nowplaying"}
8xigzo	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722827338:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'replace'", "code": "8xigzo", "command": "nowplaying"}
gLgCcK	{"guild_id": 950153022405763124, "channel_id": 1256138394069766184, "user_id": 598125772754124823, "timestamp": "<t:1722830276:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'lastfm_message'", "code": "gLgCcK", "command": "lastfm customcommand"}
zto6Rc	{"guild_id": 1254536563186991184, "channel_id": 1269691124218462301, "user_id": 1169601140804042842, "timestamp": "<t:1722858386:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" of relation \\"lastfm\\" does not exist", "code": "zto6Rc", "command": "lastfm reactions"}
AAiJBw	{"guild_id": 1254536563186991184, "channel_id": 1269691124218462301, "user_id": 1169601140804042842, "timestamp": "<t:1722858414:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" of relation \\"lastfm\\" does not exist", "code": "AAiJBw", "command": "lastfm reactions"}
oNeIpQ	{"guild_id": 1254536563186991184, "channel_id": 1269691124218462301, "user_id": 1169601140804042842, "timestamp": "<t:1722858435:R>", "error": "Command raised an exception: UndefinedColumnError: column \\"reactions\\" of relation \\"lastfm\\" does not exist", "code": "oNeIpQ", "command": "lastfm reactions"}
QJlbCP	{"guild_id": 1254536563186991184, "channel_id": 1269682193186160801, "user_id": 1169601140804042842, "timestamp": "<t:1722863130:R>", "error": "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'edit'", "code": "QJlbCP", "command": "voicemaster setup"}
FyzZBe	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 1169601140804042842, "timestamp": "<t:1722863302:R>", "error": "Command raised an exception: TypeError: 'NoneType' object is not subscriptable", "code": "FyzZBe", "command": "lastfm spotify"}
oGYTeo	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 987183275560820806, "timestamp": "<t:1722870432:R>", "error": "Command raised an exception: ValueError: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. Please check the `candidate.safety_ratings` to determine if the response was blocked.", "code": "oGYTeo", "command": "chatgpt"}
YXGiVs	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 987183275560820806, "timestamp": "<t:1722871009:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'lastfm_message'", "code": "YXGiVs", "command": "nowplaying"}
qz5yEo	{"guild_id": 1202055026797707316, "channel_id": 1269988483158507521, "user_id": 1208370307551989761, "timestamp": "<t:1722874974:R>", "error": "Command raised an exception: ValueError: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. Please check the `candidate.safety_ratings` to determine if the response was blocked.", "code": "qz5yEo", "command": "chatgpt"}
mx8hqA	{"guild_id": 1202055026797707316, "channel_id": 1269988483158507521, "user_id": 1208370307551989761, "timestamp": "<t:1722876969:R>", "error": "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions", "code": "mx8hqA", "command": "nickname"}
R7Leqi	{"guild_id": 1202055026797707316, "channel_id": 1269988483158507521, "user_id": 1208370307551989761, "timestamp": "<t:1722876979:R>", "error": "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions", "code": "R7Leqi", "command": "nickname"}
qmWoHH	{"guild_id": 1202055026797707316, "channel_id": 1269988494319681559, "user_id": 1169601140804042842, "timestamp": "<t:1722878963:R>", "error": "Command raised an exception: TypeError: PretendContext.reply() got an unexpected keyword argument 'allowed_mentions'", "code": "qmWoHH", "command": "8ball"}
RBKque	{"guild_id": 1202055026797707316, "channel_id": 1269988494319681559, "user_id": 1169601140804042842, "timestamp": "<t:1722879091:R>", "error": "Command raised an exception: ValueError: Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. Please check the `candidate.safety_ratings` to determine if the response was blocked.", "code": "RBKque", "command": "chatgpt"}
iFdxZo	{"guild_id": 892675627373699072, "channel_id": 1259232215070674945, "user_id": 598125772754124823, "timestamp": "<t:1722882029:R>", "error": "Command raised an exception: AttributeError: 'PretendContext' object has no attribute 'warning'", "code": "iFdxZo", "command": "getguild"}
hMCBUw	{"guild_id": 950153022405763124, "channel_id": 1269408686628012125, "user_id": 598125772754124823, "timestamp": "<t:1722882618:R>", "error": "Command raised an exception: RuntimeError: Session is closed", "code": "hMCBUw", "command": "jishaku shell"}
\.


--
-- Data for Name: fake_perms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fake_perms (guild_id, role_id, perms) FROM stdin;
1202055026797707316	1269988403571589131	["change_nickname"]
1202055026797707316	1269988363327246407	["manage_channels"]
1202055026797707316	1269988364623282290	["manage_roles"]
1202055026797707316	1269988373603553341	["moderate_members", "manage_messages", "manage_nicknames", "manage_threads"]
\.


--
-- Data for Name: filter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.filter (guild_id, mode, rule_id) FROM stdin;
1202055026797707316	invites	1270035597968543754
1202055026797707316	words	1270035842282557550
\.


--
-- Data for Name: force_nick; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.force_nick (guild_id, user_id, nickname) FROM stdin;
950153022405763124	461294830287585291	pls fuck me daddy
\.


--
-- Data for Name: gamestats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gamestats (user_id, game, wins, loses, total) FROM stdin;
\.


--
-- Data for Name: give_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.give_roles (guild_id, role_id) FROM stdin;
\.


--
-- Data for Name: giveaway; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.giveaway (guild_id, channel_id, message_id, winners, members, finish, host, title) FROM stdin;
\.


--
-- Data for Name: global_disabled_cmds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.global_disabled_cmds (cmd, disabled, disabled_by) FROM stdin;
\.


--
-- Data for Name: globalban; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.globalban (user_id, reason) FROM stdin;
\.


--
-- Data for Name: gw_ended; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gw_ended (channel_id, message_id, members) FROM stdin;
\.


--
-- Data for Name: hardban; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hardban (guild_id, user_id, reason, moderator_id) FROM stdin;
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, url) FROM stdin;
\.


--
-- Data for Name: imgonly; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.imgonly (guild_id, channel_id) FROM stdin;
1202055026797707316	1269988506156007507
1202055026797707316	1269988502511030284
\.


--
-- Data for Name: invoke; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoke (guild_id, command, embed) FROM stdin;
\.


--
-- Data for Name: jail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jail (guild_id, channel_id, role_id) FROM stdin;
950153022405763124	1269414814246240267	1269414811691651123
1202055026797707316	1270042379247681640	1270042374810239115
\.


--
-- Data for Name: jail_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jail_members (guild_id, user_id, roles, jailed_at) FROM stdin;
\.


--
-- Data for Name: lastfm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lastfm (user_id, username) FROM stdin;
\.


--
-- Data for Name: lastfm_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lastfm_users (id, discord_user_id, username, session_key) FROM stdin;
\N	598125772754124823	resentdev	dT_OdlLnK4MT5aMuLsym9zHAPsVokUSp
\N	1169601140804042842	precinations	juBlstfYSw9ZxFiOG4Gr91Cj2ufpq9Dd
\N	971464344749629512	FiJiCoLD	mcVJTGkf3nD0qjE5AikIQPv6hgoXQyba
\.


--
-- Data for Name: lastfmcc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lastfmcc (user_id, command) FROM stdin;
598125772754124823	hi
\.


--
-- Data for Name: leave; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leave (guild_id, channel_id, message) FROM stdin;
1202055026797707316	1269988494319681559	fys {user.mention}
\.


--
-- Data for Name: level_rewards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.level_rewards (guild_id, level, role_id) FROM stdin;
1202055026797707316	1	1269988416527929386
1202055026797707316	3	1269988415646990417
1202055026797707316	5	1269988414397087930
1202055026797707316	7	1269988412983607377
1202055026797707316	7	1269988403571589131
1202055026797707316	10	1269988411679445044
1202055026797707316	15	1269988410462965824
1202055026797707316	20	1269988409154211860
1202055026797707316	25	1269988407682273342
1202055026797707316	50	1269988384995016715
1202055026797707316	75	1269988380855242806
1202055026797707316	100	1269988380142342256
1202055026797707316	125	1269988378510884965
\.


--
-- Data for Name: level_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.level_user (guild_id, user_id, xp, level, target_xp) FROM stdin;
1202055026797707316	1208370307551989761	296	6	316
1202055026797707316	732530644412006460	44	2	118
1202055026797707316	1169601140804042842	64	3	170
\.


--
-- Data for Name: leveling; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leveling (guild_id, channel_id, message, booster_boost) FROM stdin;
1202055026797707316	1269988498576904235	congrats {user.mention}, your dick's **{level}cm** long now	\N
\.


--
-- Data for Name: lfmode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lfmode (user_id, mode) FROM stdin;
\.


--
-- Data for Name: lfreactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lfreactions (user_id, reactions) FROM stdin;
\.


--
-- Data for Name: lock_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lock_role (guild_id, role_id) FROM stdin;
\.


--
-- Data for Name: lockdown_ignore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lockdown_ignore (guild_id, channel_id) FROM stdin;
\.


--
-- Data for Name: logging; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logging (guild_id, messages, guild, roles, channels, members) FROM stdin;
950153022405763124	1269411799875457171	1269411799875457171	1269411799875457171	1269411799875457171	1269411799875457171
1254536563186991184	1269682209514717327	1269682209514717327	1269682209514717327	1269682209514717327	1269682209514717327
1202055026797707316	1269988481157828612	1269988481157828612	1269988481157828612	1269988481157828612	1269988481157828612
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (key, guild_id, channel_id, author, logs) FROM stdin;
\.


--
-- Data for Name: marry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marry (author, soulmate, "time") FROM stdin;
\.


--
-- Data for Name: number_counter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.number_counter (guild_id, channel_id, last_counted, current_number) FROM stdin;
\.


--
-- Data for Name: opened_tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opened_tickets (guild_id, channel_id, user_id) FROM stdin;
\.


--
-- Data for Name: prefixes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prefixes (guild_id, prefix) FROM stdin;
1268777695244980389	-
950153022405763124	-
1202055026797707316	,
\.


--
-- Data for Name: reactionrole; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reactionrole (guild_id, channel_id, message_id, emoji, role_id) FROM stdin;
1254536563186991184	1269695139844980902	1269695227346813009	<:sword:1255220317782020178>	1269682043189596325
1254536563186991184	1269695139844980902	1269697719606448219	<:sword:1255220317782020178>	1269682043189596325
1254536563186991184	1269697501980524585	1269697659724238919	<:sword:1255220317782020178>	1269682041340035163
1254536563186991184	1269682195404951567	1269699535245017108	<:sword:1255220317782020178>	1269682041340035163
\.


--
-- Data for Name: reminder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reminder (user_id, channel_id, guild_id, date, task) FROM stdin;
\.


--
-- Data for Name: reskin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reskin (user_id, toggled, name, avatar) FROM stdin;
598125772754124823	f	hi	https://cdn.discordapp.com/avatars/598125772754124823/ca5db36c447e2f2c302754e054525286.png?size=1024
732530644412006460	t	i ❤️ jesus	https://cdn.discordapp.com/avatars/732530644412006460/9c3d03cab48e8184c4ec2800f2220c4c.png?size=1024
1169601140804042842	t	bleed	https://cdn.discordapp.com/avatars/593921296224747521/4021abad5c35389022a1004a095f544e.png?size=1024
\.


--
-- Data for Name: reskin_enabled; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reskin_enabled (guild_id) FROM stdin;
\.


--
-- Data for Name: restore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.restore (guild_id, user_id, roles) FROM stdin;
1127267129121587370	1223498284996235337	[1127267129121587370, 1208816648782356570, 1208816660425867326, 1127267129176117269, 1208819086608441445, 1208819889360339014]
1226492622617444423	746608806867501099	[1226492622617444423, 1227139363360477204, 1226770585724518432, 1226492622617444425, 1250041214372155433]
1268137490011656213	1250829526964109387	[1268137490011656213, 1268592294546899046]
1268137490011656213	1149535834756874250	[1268137490011656213, 1268592294546899046]
950153022405763124	1207108276517605411	[950153022405763124]
950153022405763124	1185934752478396528	[950153022405763124]
950153022405763124	716390085896962058	[950153022405763124]
950153022405763124	235148962103951360	[950153022405763124]
950153022405763124	432610292342587392	[950153022405763124]
950153022405763124	155149108183695360	[950153022405763124]
950153022405763124	491769129318088714	[950153022405763124]
950153022405763124	720351927581278219	[950153022405763124]
950153022405763124	270904126974590976	[950153022405763124]
950153022405763124	578258045889544192	[950153022405763124]
950153022405763124	1256752431040036915	[950153022405763124]
950153022405763124	356268235697553409	[950153022405763124]
950153022405763124	557628352828014614	[950153022405763124]
950153022405763124	711428816127393844	[950153022405763124]
950153022405763124	949479338275913799	[950153022405763124]
950153022405763124	646937666251915264	[950153022405763124]
950153022405763124	1269050664416448513	[950153022405763124]
950153022405763124	1207108193147297837	[950153022405763124]
950153022405763124	1207108145235624020	[950153022405763124]
950153022405763124	1207108189884252173	[950153022405763124]
950153022405763124	1207108186365239296	[950153022405763124]
950153022405763124	1207108186260119552	[950153022405763124]
950153022405763124	1207108189913358342	[950153022405763124]
950153022405763124	1207108183584280608	[950153022405763124]
950153022405763124	1208472692337020999	[950153022405763124]
950153022405763124	987183275560820806	[950153022405763124]
950153022405763124	1169601140804042842	[950153022405763124]
950153022405763124	866197648493903914	[950153022405763124]
950153022405763124	1059833824541941873	[950153022405763124]
950153022405763124	1107099551816499200	[950153022405763124]
950153022405763124	1190186115307671573	[950153022405763124]
950153022405763124	996099484515827784	[950153022405763124]
950153022405763124	1133453569312440340	[950153022405763124]
950153022405763124	813062593316388864	[950153022405763124]
950153022405763124	518871170569863180	[950153022405763124]
950153022405763124	1043332857667538954	[950153022405763124]
950153022405763124	677611959558078477	[950153022405763124]
950153022405763124	896738730784747590	[950153022405763124]
950153022405763124	1179328426801381426	[950153022405763124]
950153022405763124	1241859669341896805	[950153022405763124]
950153022405763124	995167001779638293	[950153022405763124]
950153022405763124	1142660932900757626	[950153022405763124]
950153022405763124	1152008892918796428	[950153022405763124]
950153022405763124	798046382808104990	[950153022405763124]
950153022405763124	1076771218805489774	[950153022405763124]
950153022405763124	852894685729914910	[950153022405763124]
950153022405763124	1128790306750464050	[950153022405763124]
950153022405763124	1193509716123467878	[950153022405763124]
950153022405763124	684431774620712993	[950153022405763124]
950153022405763124	849339857993990144	[950153022405763124]
950153022405763124	1259709597694824469	[950153022405763124]
950153022405763124	1269433308945711135	[950153022405763124]
950153022405763124	995580403198988328	[950153022405763124]
950153022405763124	840439255708991508	[950153022405763124]
950153022405763124	447533024867778572	[950153022405763124]
950153022405763124	661306842273677341	[950153022405763124]
950153022405763124	1262943338340945920	[950153022405763124]
972867465635848253	598125772754124823	[972867465635848253, 972899470872285244, 1170198000014995556]
972867465635848253	1268777073078571121	[972867465635848253, 972899470872285244]
946800234804166697	1268777073078571121	[946800234804166697, 1036384181690847394]
946800234804166697	1146616084183650355	[946800234804166697, 1036384181690847394]
950153022405763124	1139318380676009995	[950153022405763124]
946800234804166697	845724632086347787	[946800234804166697, 1036384181690847394, 948343502507491339, 1171527920716619806]
946800234804166697	452763253861253120	[946800234804166697, 1036384181690847394]
950153022405763124	187747524646404105	[950153022405763124]
946800234804166697	1175049107891568782	[946800234804166697, 1036384181690847394, 1171527920716619806]
1208651928507129887	948573943650992169	[1208651928507129887]
950153022405763124	1044196479046254652	[950153022405763124]
946800234804166697	915101417595891742	[946800234804166697, 1036384181690847394, 1171527920716619806]
892675627373699072	697224554728390667	[892675627373699072, 1249814208334528533]
950153022405763124	969026219276394556	[950153022405763124]
672178593371127808	810066670055718914	[672178593371127808, 698323076202496121]
946800234804166697	938033489478025217	[946800234804166697, 1036384181690847394, 981564541982875688]
950153022405763124	908075736131338260	[950153022405763124]
946800234804166697	819386457030131732	[946800234804166697, 1036384181690847394]
950153022405763124	1118915899311784009	[950153022405763124]
1208651928507129887	969263509802201098	[1208651928507129887]
946800234804166697	1142143127235334315	[946800234804166697, 1036384181690847394]
892675627373699072	994566460108181524	[892675627373699072, 1249814208334528533]
946800234804166697	874023343165165588	[946800234804166697, 1036384181690847394]
950153022405763124	852784127447269396	[950153022405763124]
946800234804166697	1123586224851009656	[946800234804166697, 1036384181690847394, 948345555090833418]
892675627373699072	357585970100699146	[892675627373699072, 1249814208334528533]
1208651928507129887	900446386833727489	[1208651928507129887]
892675627373699072	1071934226011803688	[892675627373699072, 1249814208334528533]
946800234804166697	1212116225635651607	[946800234804166697, 1036384181690847394]
950153022405763124	882483895839358986	[950153022405763124]
946800234804166697	950536718275182592	[946800234804166697, 1036384181690847394]
946800234804166697	1250220782886584400	[946800234804166697, 1036384181690847394]
950153022405763124	954923887848722462	[950153022405763124]
946800234804166697	789866732465815623	[946800234804166697, 1036384181690847394]
950153022405763124	1221145814626205781	[950153022405763124]
946800234804166697	791942815193628702	[946800234804166697, 1036384181690847394, 948343375462019112]
950153022405763124	906756775158611989	[950153022405763124]
672178593371127808	647485123977150475	[672178593371127808, 698323076202496121]
950153022405763124	1057310810440994967	[950153022405763124]
946800234804166697	1192911412410986634	[946800234804166697, 1036384181690847394, 948343502507491339, 948343488594972724, 948343375462019112, 948343346257076224, 948345555090833418, 1171527920716619806]
946800234804166697	1149170812331503688	[946800234804166697, 1036384181690847394, 948343502507491339]
950153022405763124	585435009113128960	[950153022405763124]
946800234804166697	662770920821096452	[946800234804166697, 1036384181690847394, 948343346257076224]
946800234804166697	1115162865918283787	[946800234804166697, 1036384181690847394]
946800234804166697	1150040762973687848	[946800234804166697, 1036384181690847394, 948343346257076224]
950153022405763124	1015714172195049502	[950153022405763124]
946800234804166697	667126864724230204	[946800234804166697, 1036384181690847394, 948343488594972724]
946800234804166697	1129544554262040709	[946800234804166697, 1036384181690847394, 948343375462019112]
892675627373699072	1252001166703853588	[892675627373699072, 1249814208334528533]
946800234804166697	921520450138427392	[946800234804166697, 1036384181690847394]
946800234804166697	795634211083255848	[946800234804166697, 1036384181690847394]
892675627373699072	820661475013820496	[892675627373699072, 1249814208334528533]
946800234804166697	926931780236349530	[946800234804166697, 1036384181690847394]
892675627373699072	1031682374678880286	[892675627373699072, 1249814208334528533]
892675627373699072	902397632104759327	[892675627373699072, 1249814208334528533]
946800234804166697	951330074102214696	[946800234804166697, 1036384181690847394, 948343502507491339]
946800234804166697	857734631247708181	[946800234804166697, 1036384181690847394, 948343375462019112]
672178593371127808	789283935070322699	[672178593371127808, 934134615201947708, 772910083197370409, 772910080974651453, 772910065530699786, 680924892601778184, 698323076202496121, 767613428525170689]
946800234804166697	1136121807913623663	[946800234804166697, 1036384181690847394]
946800234804166697	1166963963817377883	[946800234804166697, 1036384181690847394, 1171527920716619806]
946800234804166697	1072986628022349906	[946800234804166697, 1036384181690847394]
950153022405763124	720397027636412519	[950153022405763124]
950153022405763124	498250712908562435	[950153022405763124]
950153022405763124	461294830287585291	[950153022405763124]
950153022405763124	713105351582548010	[950153022405763124]
892675627373699072	1069258018258178059	[892675627373699072, 1249814208334528533]
1208651928507129887	1069258018258178059	[1208651928507129887]
950153022405763124	1147292410116837416	[950153022405763124]
946800234804166697	1073240117394800774	[946800234804166697, 1036384181690847394, 948343488594972724]
946800234804166697	1054029157031497839	[946800234804166697, 1036384181690847394]
946800234804166697	502979907568271371	[946800234804166697, 1036384181690847394]
946800234804166697	678807889678172205	[946800234804166697, 1036384181690847394]
892675627373699072	1170953822634520628	[892675627373699072, 1249814208334528533]
892675627373699072	1235271206287048769	[892675627373699072, 1249814208334528533]
950153022405763124	858699890636619817	[950153022405763124]
946800234804166697	944050743483203584	[946800234804166697, 1036384181690847394, 948343488594972724]
946800234804166697	899153071538585600	[946800234804166697, 1036384181690847394, 948345555090833418]
946800234804166697	755544681776939008	[946800234804166697, 1036384181690847394]
672178593371127808	1129482004673605703	[672178593371127808, 698323076202496121]
950153022405763124	1234993627407716413	[950153022405763124]
950153022405763124	814125636825513995	[950153022405763124]
892675627373699072	754646394018725890	[892675627373699072, 1249814208334528533]
950153022405763124	710028376286429254	[950153022405763124]
1254536563186991184	1094942437820076083	[1254536563186991184, 1255628812012490784, 1255961078551019630]
1254536563186991184	356268235697553409	[1254536563186991184, 1255628812012490784, 1255961078551019630]
1254536563186991184	292953664492929025	[1254536563186991184, 1255628812012490784]
892675627373699072	840439255708991508	[892675627373699072, 1249814208334528533]
946800234804166697	1189384877418745947	[946800234804166697, 1036384181690847394]
1254536563186991184	416358583220043796	[1254536563186991184]
950153022405763124	682227930977402920	[950153022405763124]
946800234804166697	495958791666270209	[946800234804166697, 1036384181690847394]
950153022405763124	987091223837835294	[950153022405763124]
950153022405763124	742402634559914125	[950153022405763124]
892675627373699072	1234993627407716413	[892675627373699072, 1249814208334528533]
892675627373699072	974580866615496714	[892675627373699072, 1249814208334528533]
892675627373699072	968753252873146439	[892675627373699072, 1249814208334528533]
946800234804166697	1222558126981648570	[946800234804166697, 1036384181690847394, 948345555090833418]
946800234804166697	837317859277013022	[946800234804166697, 1036384181690847394]
1202055026797707316	1268777073078571121	[1202055026797707316, 1269988435125338184, 1269988359330201710, 1269988357732040725]
1202055026797707316	912268358416756816	[1202055026797707316, 1269988435125338184, 1269988359330201710, 1269988357732040725]
1202055026797707316	1034747093887234068	[1202055026797707316, 1269988357732040725]
946800234804166697	933154896058925076	[946800234804166697, 1036384181690847394]
950153022405763124	1259940333597360158	[950153022405763124]
946800234804166697	779716535802658836	[946800234804166697, 1036384181690847394]
950153022405763124	1188955485462872226	[950153022405763124]
946800234804166697	744734403468591185	[946800234804166697, 1036384181690847394, 1171527920716619806]
1257723151580659852	994051042939523174	[1257723151580659852, 1260628272790634589, 1260160410913345556, 1258283118272712814]
1257723151580659852	1145151922282692738	[1257723151580659852, 1258283118272712814]
946800234804166697	927168603449614376	[946800234804166697, 1036384181690847394, 948343375462019112]
946800234804166697	742117131952586782	[946800234804166697, 1036384181690847394, 948345555090833418, 1171527920716619806]
\.


--
-- Data for Name: restrictcommand; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.restrictcommand (guild_id, command, role_id) FROM stdin;
\.


--
-- Data for Name: seen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seen (user_id, guild_id, "time") FROM stdin;
1247076592556183598	1268777695244980389	2024-08-03 22:52:55.163961-07
1235271206287048769	1230468832829902848	2024-08-02 17:53:07.520068-07
214753146512080907	1268777695244980389	2024-08-03 13:21:55.280259-07
939274781977612378	1252343120545448039	2024-08-02 17:53:24.673885-07
948573943650992169	1208651928507129887	2024-08-04 02:14:54.984314-07
648683483723595776	1251675682648625264	2024-08-02 17:53:09.776227-07
763815690511450113	1127267129121587370	2024-08-02 17:52:30.113731-07
1250098229496905771	1133440161670234142	2024-08-02 17:53:05.531051-07
885681559552819202	721347673873186816	2024-08-02 17:52:30.485405-07
862945368407801888	1238542680095588523	2024-08-02 17:52:12.012552-07
1187419254220394597	1252343120545448039	2024-08-02 17:52:14.055826-07
1215582436587601920	1230468832829902848	2024-08-02 17:52:14.662432-07
746608806867501099	1226492622617444423	2024-08-02 17:52:41.769535-07
1238768616996995122	1234688687414050896	2024-08-02 17:52:15.106094-07
974456477458763826	721347673873186816	2024-08-02 17:53:15.516558-07
1140303046736355369	1247841972715126844	2024-08-02 17:53:08.259476-07
553732540570271765	1257541366867562496	2024-08-02 17:53:14.048236-07
1264329017696190587	1234874560890015785	2024-08-02 17:52:48.674584-07
1036056465498185748	1258919277449183402	2024-08-02 17:53:14.451614-07
554354904760582168	1240025784182374450	2024-08-02 17:52:48.846894-07
818894869292384347	1108225520962904075	2024-08-02 17:52:17.664809-07
741038814331666432	1226492622617444423	2024-08-02 17:52:42.370308-07
501583707157692416	1133440161670234142	2024-08-02 17:52:18.175743-07
1250429899307483196	1266108553563734147	2024-08-02 17:53:10.005523-07
1007027547705454693	1266143468359778316	2024-08-02 17:52:18.956188-07
1177394183519092796	1211365531073118329	2024-08-02 17:52:19.183936-07
1150462293063245924	721347673873186816	2024-08-02 17:52:19.626129-07
1214902532086833213	1258030644471140384	2024-08-02 17:52:43.105243-07
827098130956812349	1264378143741841511	2024-08-02 17:52:20.810514-07
1169444150605774926	1185200708866289725	2024-08-02 17:53:24.779172-07
959837826801893436	1201299986198036530	2024-08-02 17:53:26.954861-07
1171910131215237161	721347673873186816	2024-08-02 17:53:26.310539-07
769949474084093953	1209918006969503865	2024-08-02 17:53:19.966403-07
864273348497506304	1261865179776286761	2024-08-02 17:53:22.243191-07
1250142934938943578	1241366662142234686	2024-08-02 17:52:22.739394-07
1199508312341872704	1226828213129445468	2024-08-02 17:53:13.056822-07
816837524956643378	1209918006969503865	2024-08-02 17:52:23.300009-07
1250670386774016053	721347673873186816	2024-08-02 17:53:25.414263-07
823184075506188339	721347673873186816	2024-08-02 17:52:33.491905-07
1175880711652261900	1230468832829902848	2024-08-02 17:52:58.287887-07
795749886230265897	1127267129121587370	2024-08-02 17:53:05.716012-07
1092570781009064107	1209918006969503865	2024-08-02 17:52:24.048378-07
956334560386375722	1247844239430254594	2024-08-02 17:53:26.620325-07
1201238090304471162	1261865179776286761	2024-08-02 17:52:49.625707-07
1266898704561078414	1133822935610687488	2024-08-02 17:52:24.957868-07
365204669523558400	1240025784182374450	2024-08-02 17:52:33.924735-07
767152798474960896	1230468832829902848	2024-08-02 17:53:25.146938-07
1007004756880932864	1260607757577355285	2024-08-02 17:53:01.755946-07
1249035520076546115	1209918006969503865	2024-08-02 17:53:16.554945-07
1263613659339423765	721347673873186816	2024-08-02 17:53:26.981473-07
728386557584605225	1127267129121587370	2024-08-02 17:52:50.112792-07
792526365260906506	1133440161670234142	2024-08-02 17:52:26.864717-07
726087516918120482	1185200708866289725	2024-08-02 17:52:58.830598-07
1028065326547607622	950153022405763124	2024-08-05 00:07:15.497525-07
1111876644970446909	1230468832829902848	2024-08-02 17:52:50.526732-07
1084799758083833947	1252343120545448039	2024-08-02 17:52:43.96373-07
761995588606230528	1252343120545448039	2024-08-02 17:53:02.022852-07
1009949037740425216	1209918006969503865	2024-08-02 17:52:28.241971-07
1188011131172835350	1234688687414050896	2024-08-02 17:52:28.505763-07
1111876644970446909	1230468832829902848	2024-08-02 17:52:50.559793-07
1187992953638109286	1226828213129445468	2024-08-02 17:52:28.739654-07
1248216293660688486	1258919277449183402	2024-08-02 17:52:44.933632-07
389504068747395074	1201299986198036530	2024-08-02 17:52:28.999905-07
707958007828578437	1201174466886127756	2024-08-02 17:52:34.392655-07
1171676913803202711	1209918006969503865	2024-08-02 17:53:13.213214-07
710227118402961460	1258919277449183402	2024-08-02 17:53:05.832291-07
799162358647488532	1209918006969503865	2024-08-02 17:52:45.032249-07
886432449540808754	1260607757577355285	2024-08-02 17:52:35.670161-07
1096288292615491625	1096289760038883339	2024-08-02 17:53:05.923628-07
859898842120323143	1185200708866289725	2024-08-02 17:53:19.357469-07
869739018055721071	1251322041005506561	2024-08-02 17:53:16.712451-07
763450540276449290	1209918006969503865	2024-08-02 17:52:36.360467-07
1198734566328893534	1197794904043159673	2024-08-02 17:53:08.461081-07
966819050485350450	1240025784182374450	2024-08-02 17:53:10.309075-07
1062875781413486652	1257541366867562496	2024-08-02 17:52:37.429046-07
1249428492429557760	1251675682648625264	2024-08-02 17:53:24.540746-07
871565768603615242	1185200708866289725	2024-08-02 17:52:51.068942-07
1257188501045379072	1257541366867562496	2024-08-02 17:52:38.429515-07
1230788889011290183	1201299986198036530	2024-08-02 17:53:02.761097-07
1260955952442773595	1261865179776286761	2024-08-02 17:52:38.661238-07
818208121532317727	1201174466886127756	2024-08-02 17:53:25.477779-07
1133578686424162454	1133822935610687488	2024-08-02 17:52:51.256894-07
487099917089767425	1059213597307318393	2024-08-02 17:53:11.267977-07
1109148804810276906	1127267129121587370	2024-08-02 17:52:39.858017-07
1111898477258084472	1096289760038883339	2024-08-02 17:53:13.366695-07
750752584859385856	1230468832829902848	2024-08-02 17:52:51.291365-07
985199981721948210	1234198250995712073	2024-08-02 17:52:40.454746-07
508266003797508101	1230468832829902848	2024-08-02 17:52:59.59898-07
735889091564011704	1209918006969503865	2024-08-02 17:53:21.771646-07
1255289918263918593	1241477576757874778	2024-08-02 17:53:15.692405-07
1201265999727575092	1221001878960210031	2024-08-02 17:53:25.380359-07
1239747283382308904	721347673873186816	2024-08-02 17:53:08.996325-07
1258807399528267857	1230468832829902848	2024-08-02 17:53:13.687042-07
797498466494054430	1243192468472856576	2024-08-02 17:53:06.403784-07
1226094086440751175	1059213597307318393	2024-08-02 17:53:03.307046-07
1242821540777562134	1258919277449183402	2024-08-02 17:53:25.879495-07
431492247163371522	1257541366867562496	2024-08-02 17:53:03.441986-07
424780128568999968	721347673873186816	2024-08-02 17:53:06.99065-07
1023361449688584283	1247841972715126844	2024-08-02 17:52:47.54904-07
912803346321137685	1266747240953675889	2024-08-02 17:53:03.531131-07
784287311247835136	1096289760038883339	2024-08-02 17:53:09.051459-07
814133051378499635	721347673873186816	2024-08-02 17:53:09.137135-07
928111752158281749	1059213597307318393	2024-08-02 17:53:11.764355-07
1161481818122502174	1201019455040397392	2024-08-02 17:52:47.895767-07
799014895764504597	721347673873186816	2024-08-02 17:53:00.183934-07
601241875382534145	1096289760038883339	2024-08-02 17:53:00.307648-07
827906181384372225	1133440161670234142	2024-08-02 17:53:15.215717-07
995464018653364267	1252032046029602858	2024-08-02 17:53:13.77199-07
1255236652155015271	1133440161670234142	2024-08-02 17:52:56.792528-07
901315510296277022	1201019455040397392	2024-08-02 17:53:09.159146-07
766928365729873921	1209918006969503865	2024-08-02 17:53:04.175795-07
705266937881690132	1127267129121587370	2024-08-02 17:53:18.362063-07
903684585123119186	1133822935610687488	2024-08-02 17:53:00.616012-07
196102803935068162	1257541366867562496	2024-08-02 17:53:15.228947-07
872953349031481404	1226492622617444423	2024-08-02 17:53:09.450363-07
1234581611983536199	1241477576757874778	2024-08-02 17:53:09.475488-07
965662287799136256	1226492622617444423	2024-08-02 17:53:19.545348-07
549369855367970826	1133440161670234142	2024-08-02 17:53:06.995055-07
1039889083394183198	1260607757577355285	2024-08-02 17:53:19.227909-07
857153794084962344	1133440161670234142	2024-08-02 17:53:13.956697-07
1040411640522342523	721347673873186816	2024-08-02 17:53:22.923695-07
870508652363124746	1247841972715126844	2024-08-02 17:53:09.516882-07
1214792621923246114	1260607757577355285	2024-08-02 17:53:09.695471-07
1247868333731352718	721347673873186816	2024-08-02 17:53:21.261772-07
1236027126419816458	1226492622617444423	2024-08-02 17:53:16.568273-07
773609315314827284	1059213597307318393	2024-08-02 17:53:15.321017-07
828095530751229952	1209918006969503865	2024-08-02 17:53:17.417093-07
1219335527476629676	1209918006969503865	2024-08-02 17:53:22.085968-07
629805357732200449	1221001878960210031	2024-08-02 17:53:24.902266-07
1269050562809303150	721347673873186816	2024-08-02 17:53:23.820934-07
808132565206040607	1251675682648625264	2024-08-02 17:53:23.826871-07
1211447795907563602	1133440161670234142	2024-08-02 17:53:25.524418-07
1241859669341896805	1235302576459616367	2024-08-02 17:53:25.597695-07
1057641059238301848	1185200708866289725	2024-08-02 17:53:25.6912-07
1169601140804042842	1266750786478805023	2024-08-04 11:00:01.554149-07
761626793521971230	1256306941899309110	2024-08-02 17:53:26.485259-07
795160256329023509	1201019455040397392	2024-08-02 17:53:26.490707-07
1144020851486904443	1261865179776286761	2024-08-02 17:53:26.621606-07
400429809202888704	672178593371127808	2024-08-04 14:44:10.807746-07
987183275560820806	1268777695244980389	2024-08-04 18:09:07.891313-07
1208472692337020999	950153022405763124	2024-08-04 18:00:48.957797-07
1185934752478396528	950153022405763124	2024-08-03 14:36:33.846672-07
1067586499224293436	946800234804166697	2024-08-05 02:57:52.436781-07
1207108276517605411	950153022405763124	2024-08-03 14:32:10.645622-07
957388794208874607	950153022405763124	2024-08-03 15:07:01.045969-07
1125456119519793313	950153022405763124	2024-08-03 16:11:51.723681-07
1269050664416448513	950153022405763124	2024-08-03 14:42:06.837733-07
463367454312235010	950153022405763124	2024-08-03 16:49:25.947776-07
987183275560820806	950153022405763124	2024-08-05 08:35:30.224668-07
1169601140804042842	1268137490011656213	2024-08-04 02:50:15.931012-07
1256345985341325382	950153022405763124	2024-08-04 10:54:58.62876-07
1248366051956097115	892675627373699072	2024-08-04 12:57:31.771713-07
732530644412006460	1202055026797707316	2024-08-05 10:34:14.71187-07
1221770638390198273	946800234804166697	2024-08-05 00:12:35.365136-07
547882311983824907	950153022405763124	2024-08-04 16:25:07.77968-07
1251957547842146386	1257723151580659852	2024-08-05 08:26:27.902275-07
732530644412006460	950153022405763124	2024-08-05 09:15:28.436001-07
1262943338340945920	950153022405763124	2024-08-03 19:03:32.905388-07
1140860891089354762	950153022405763124	2024-08-05 00:08:27.033484-07
526341224609742859	892675627373699072	2024-08-04 20:28:49.845161-07
1259709597694824469	950153022405763124	2024-08-03 19:06:47.372858-07
187747524646404105	950153022405763124	2024-08-04 00:45:15.906648-07
1207108186260119552	950153022405763124	2024-08-03 15:06:28.119807-07
498250712908562435	950153022405763124	2024-08-05 00:08:35.298274-07
1169601140804042842	950153022405763124	2024-08-05 10:47:35.155099-07
1004023220871114884	950153022405763124	2024-08-05 00:08:54.938638-07
1007624133129023608	672178593371127808	2024-08-05 08:48:39.93205-07
1207108189884252173	950153022405763124	2024-08-03 15:06:34.15322-07
1150485725054242906	950153022405763124	2024-08-03 16:25:40.428034-07
876352806431387738	1257723151580659852	2024-08-04 06:46:51.935606-07
1207108183584280608	950153022405763124	2024-08-03 15:06:37.056571-07
969263509802201098	1208651928507129887	2024-08-04 07:29:51.967883-07
1207108145235624020	950153022405763124	2024-08-03 15:06:46.061447-07
1207108189913358342	950153022405763124	2024-08-03 15:06:47.968134-07
1204272063381245973	1257723151580659852	2024-08-04 03:09:12.813007-07
1207108186365239296	950153022405763124	2024-08-03 15:06:50.047956-07
772342846022877204	1257723151580659852	2024-08-04 04:58:36.674036-07
1207108193147297837	950153022405763124	2024-08-03 15:06:51.472502-07
948573943650992169	892675627373699072	2024-08-04 02:23:48.146861-07
715662341554831432	950153022405763124	2024-08-03 16:06:29.155869-07
864524371167019018	892675627373699072	2024-08-05 02:38:23.316252-07
980550223136972841	1257723151580659852	2024-08-04 13:11:55.657125-07
820661475013820496	892675627373699072	2024-08-04 18:03:48.374683-07
831953870133133332	892675627373699072	2024-08-04 18:04:44.990205-07
743306033144791110	1257723151580659852	2024-08-04 08:08:57.397943-07
852894685729914910	950153022405763124	2024-08-03 15:50:16.445591-07
971464344749629512	950153022405763124	2024-08-05 10:47:39.717933-07
1169601140804042842	1268777695244980389	2024-08-05 06:57:51.831232-07
1261488861599760440	950153022405763124	2024-08-04 18:32:58.928535-07
526341224609742859	950153022405763124	2024-08-04 21:47:32.437308-07
1252001166703853588	892675627373699072	2024-08-04 11:22:02.839071-07
110172019273785344	950153022405763124	2024-08-04 08:21:48.456875-07
894443904508780545	1257723151580659852	2024-08-05 08:09:26.664419-07
849602306835480586	946800234804166697	2024-08-04 19:53:43.772957-07
908075736131338260	950153022405763124	2024-08-03 16:50:47.489498-07
787556133611110422	950153022405763124	2024-08-05 00:16:37.457063-07
1220556320713998338	1257723151580659852	2024-08-04 16:12:20.012048-07
1116096066522185829	950153022405763124	2024-08-03 15:52:08.030072-07
948245588296740965	950153022405763124	2024-08-03 17:15:15.814966-07
959438821236301824	1257723151580659852	2024-08-04 08:26:00.451012-07
803074635796709416	1257723151580659852	2024-08-04 08:26:36.710755-07
623369905000939520	1257723151580659852	2024-08-04 08:27:52.17935-07
902397632104759327	892675627373699072	2024-08-04 20:22:25.286334-07
851437466871136256	892675627373699072	2024-08-05 03:13:22.13159-07
1208370307551989761	1202055026797707316	2024-08-05 10:24:38.365295-07
1074668481867419758	950153022405763124	2024-08-05 09:41:52.525818-07
1052833821449539655	892675627373699072	2024-08-05 06:10:22.92874-07
900446386833727489	892675627373699072	2024-08-04 18:46:21.890084-07
595239050273619969	892675627373699072	2024-08-05 11:21:26.657325-07
598125772754124823	1268777695244980389	2024-08-04 10:58:25.372531-07
838948300664340510	1257723151580659852	2024-08-05 07:48:43.722889-07
290338733423853578	1257723151580659852	2024-08-05 08:28:26.910394-07
971464344749629512	1268777695244980389	2024-08-04 17:53:22.765546-07
840439255708991508	950153022405763124	2024-08-04 01:49:19.034872-07
1184957039764582454	950153022405763124	2024-08-05 00:07:32.351055-07
1169601140804042842	1254536563186991184	2024-08-05 10:50:28.92524-07
1060756015093649508	1257723151580659852	2024-08-04 15:58:23.416764-07
987183275560820806	892675627373699072	2024-08-05 11:21:43.687219-07
732530644412006460	1254536563186991184	2024-08-05 10:37:19.748049-07
624274903281041428	1208651928507129887	2024-08-05 10:10:27.931358-07
461294830287585291	950153022405763124	2024-08-05 00:10:45.405056-07
704346007000973344	946800234804166697	2024-08-04 04:34:00.281937-07
595239050273619969	946800234804166697	2024-08-04 04:34:12.541119-07
1220724398164803705	892675627373699072	2024-08-04 07:42:17.743517-07
1169601140804042842	1202055026797707316	2024-08-05 10:55:44.650466-07
1164426037267009576	1257723151580659852	2024-08-04 22:05:15.540808-07
1247843122160074782	892675627373699072	2024-08-04 05:27:29.784203-07
153643814605553665	950153022405763124	2024-08-04 20:47:25.287811-07
1234993627407716413	892675627373699072	2024-08-04 13:14:57.917425-07
927168603449614376	946800234804166697	2024-08-05 10:59:09.457373-07
793973654886678555	1257723151580659852	2024-08-04 17:35:56.856816-07
485125994244472844	672178593371127808	2024-08-05 01:49:30.254143-07
742666571142660166	950153022405763124	2024-08-05 11:29:05.07838-07
756917367870717983	1257723151580659852	2024-08-05 08:19:22.332354-07
1194762394803642421	1257723151580659852	2024-08-04 17:36:30.493581-07
1210066990207868980	946800234804166697	2024-08-04 10:26:05.890641-07
341099790349631491	1257723151580659852	2024-08-05 05:07:14.621755-07
1061235304759054368	892675627373699072	2024-08-04 10:02:38.147457-07
840439255708991508	1257723151580659852	2024-08-05 08:21:05.496438-07
987183275560820806	946800234804166697	2024-08-04 17:04:57.714838-07
547882311983824907	946800234804166697	2024-08-04 17:05:48.746716-07
1137782359371030538	946800234804166697	2024-08-04 10:54:24.31452-07
1065688498516009060	1257723151580659852	2024-08-05 01:55:53.152405-07
853067018747510804	672178593371127808	2024-08-04 11:31:40.812189-07
852784127447269396	950153022405763124	2024-08-04 10:03:03.831795-07
428647094631268352	892675627373699072	2024-08-04 18:49:10.271934-07
1069258018258178059	1208651928507129887	2024-08-04 20:19:39.343957-07
971464344749629512	892675627373699072	2024-08-04 20:23:50.25593-07
1035927715548766208	1254536563186991184	2024-08-04 13:47:04.252648-07
1069258018258178059	892675627373699072	2024-08-04 20:25:20.066785-07
461914901624127489	950153022405763124	2024-08-05 11:00:00.784601-07
598125772754124823	950153022405763124	2024-08-05 11:30:04.898122-07
274323566021967877	1257723151580659852	2024-08-04 16:50:58.073824-07
1259709597694824469	892675627373699072	2024-08-04 21:32:47.369386-07
946885171049811969	950153022405763124	2024-08-05 00:08:05.313362-07
1196215053771358292	672178593371127808	2024-08-05 06:02:00.119481-07
793851837332979722	1257723151580659852	2024-08-05 08:19:40.257527-07
915350867438338058	950153022405763124	2024-08-05 04:47:55.200117-07
758918919628521474	1257723151580659852	2024-08-05 06:30:36.832236-07
1185934752478396528	1254536563186991184	2024-08-05 09:30:48.786635-07
214753146512080907	950153022405763124	2024-08-05 00:12:22.048396-07
1258677310731583529	1257723151580659852	2024-08-05 08:25:49.386357-07
598125772754124823	892675627373699072	2024-08-05 11:20:36.383343-07
1208370307551989761	950153022405763124	2024-08-05 10:22:27.321535-07
1259940333597360158	950153022405763124	2024-08-05 08:10:19.505613-07
716244627094765609	1257723151580659852	2024-08-05 09:33:21.342159-07
750379503179661444	950153022405763124	2024-08-05 09:21:33.151773-07
\.


--
-- Data for Name: selfprefix; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.selfprefix (user_id, prefix) FROM stdin;
1169601140804042842	,
987183275560820806	
\.


--
-- Data for Name: spotify; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spotify (user_id, access_token) FROM stdin;
\.


--
-- Data for Name: starboard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.starboard (guild_id, channel_id, emoji, count, role_id) FROM stdin;
1202055026797707316	1269988492738428971	💀	3	\N
\.


--
-- Data for Name: starboard_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.starboard_messages (guild_id, channel_id, message_id, starboard_message_id) FROM stdin;
\.


--
-- Data for Name: stickymessage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stickymessage (guild_id, channel_id, message) FROM stdin;
1202055026797707316	1269988490737745993	use ,br create to create a custom role
1202055026797707316	1269988472291328072	you must be level <@&1269988416527929386>+ to claim this gw
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags (guild_id, author_id, name, response) FROM stdin;
1254536563186991184	1169601140804042842	pic	to get pic perms rep /higher
\.


--
-- Data for Name: ticket_topics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticket_topics (guild_id, name, description) FROM stdin;
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tickets (guild_id, open_embed, category_id, logs, support_id) FROM stdin;
\.


--
-- Data for Name: timezone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.timezone (user_id, zone) FROM stdin;
\.


--
-- Data for Name: trial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trial (guild_id, end_date) FROM stdin;
\.


--
-- Data for Name: trials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trials (guild_id, expires) FROM stdin;
\.


--
-- Data for Name: username_track; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.username_track (guild_id, webhook_url) FROM stdin;
\.


--
-- Data for Name: usernames; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usernames (user_id, user_name, "time") FROM stdin;
1229545026699264090	doxingskids	1722646367
765826906234683424	emilysupport24	1722721159
838599966367940630	zoe.wentzelm	1722721165
926637236236201984	alantotamoks	1722721178
1045217579683299329	kaliuah	1722726462
1226733263612285049	blalaala	1722738268
821190815799967766	.sukugo	1722738274
1216618686593372181	is7gakb5jwb5rhwb6fv	1722739561
893316860135739393	ju1_.	1722741132
1012421109364305971	.purestcay.	1722746178
656627584574160896	gentlewhir	1722750303
866183443971702806	kwittyval	1722752160
810238078131896380	fuerza.360	1722752346
933410560924602378	ieatdogsforbreakfast.	1722752643
1116719260413210675	larpingcurrency	1722753070
1069089657977061426	unimaginablefantasy	1722753257
1134232881351376956	hyenasfavorite	1722753350
1028065326547607622	cwrspe	1722754103
1199248996095512608	songsforxain	1722754137
1216851335035486270	zayriak.	1722754269
1050212406179147886	purplenurpel	1722755351
1181785991518879766	s7ofia	1722755531
1199248996095512608	attentionseekingxain	1722756551
1176747438799847437	freemyswag5	1722757435
872398839905157130	pussypounder3000_.	1722757497
943193232358117388	yukisfave	1722758288
655965792940064778	gutrevival	1722758802
996277039566962688	zfancyz	1722759138
1088816615870709911	20193f1lymf03v0l	1722759738
827300877617594388	w0ckstxrrr_	1722760346
1148842194652893326	foodbuffet	1722760765
512802834257936411	claw.enforcement	1722761122
1138825656080289836	detachablenakiffy	1722762139
1138825656080289836	xsjhna12	1722762282
1013007050126676090	miyunaners	1722762668
1260243206671564922	gl9ssx	1722763039
1170637329170432054	madeheruseless	1722763141
1171473988564828284	hyyuko	1722763947
1127731451253756025	themelonmanfr	1722764223
1167271484817932319	hiswiickc	1722764925
1210391980501372991	pcxrter.	1722765145
1210391980501372991	sirevampsct	1722765189
1198394776047849545	kuiixla	1722765424
1062899243112738906	meowziesr	1722766555
949199451967356938	sueuxu	1722768271
1255775313523249194	0030824	1722768775
737715550217830511	miayyq8	1722769231
1192247663303852062	wwokee	1722769875
1107424511294451853	reiyeasigimy	1722770298
1223785034583117924	deleted020929	1722770410
1152005409662582977	pwcifysinsss.	1722770455
853789999421325343	fnqnn	1722773305
1150040762973687848	oioioibak7016	1722773803
914611168780369940	.si.ix.	1722773841
1236748320265732268	imlosingmymental	1722773949
242752798725242880	pierceeheart	1722775819
1177383294883602531	soulsevens	1722777105
863106265591709766	inneedoffent	1722777282
848074771849281577	.guiltyx	1722777477
1029369801128300596	hectorboys	1722777554
989265279584436345	cigarettetits	1722778184
1198039842261569678	cwutepandaellaaa	1722778428
845677779147685928	drlsummerroberts	1722778590
1107288169428307999	hitlungs	1722778988
965263078310703164	lembicz.	1722779733
1125516730068893807	14uq	1722780196
584706314635313153	raphaelebita	1722780352
1114938372557905920	skusak	1722780373
1114938372557905920	afternoonharpoon	1722780510
1173792560158875721	trey08_x	1722780646
916264940317339678	rialuvsani	1722782139
633106162916786177	irisflowerswhen	1722783097
916264940317339678	rialuvsherex	1722783184
808593296992763915	batch.update	1722783925
1047260742107275444	homiesexual.milk	1722783941
550803200723386391	morigotracks	1722784203
1119980041296687104	.michiehotgf	1722784383
1143467548650786998	stuckinherthoughts	1722784866
1201435035874627594	tylerr.0001	1722786838
1109580506833621202	pr3ttyprivilegee	1722786982
1090394066912555089	chlosqvn	1722787099
1009378201119756360	princessajuli	1722787202
1012421109364305971	.lostcay.	1722787640
734512545850982511	rottenkiss	1722787854
663108610280259605	hhhhh_444	1722788293
1083256134502207569	lushvst	1722788613
1040101292296646736	kazuucidio	1722789046
886329056042315848	kauyidin	1722789527
1178066454441099315	lovinqqval	1722789889
1205514811430150155	eafgirl.	1722790604
1131711944336879698	.hinaaz.	1722791091
1182832275453382657	.ilikejupiter	1722791387
937521472048615474	evkysvt	1722791488
1075893794312036502	joseff9007	1722792085
931102832508141571	widjdj.	1722792109
869765195122225233	catnisito	1722792836
869765195122225233	sodkasfajsahsjjaksjasd	1722792959
1220556320713998338	geto.vspp	1722793385
1092684803884720138	smokinhapack	1722793741
894933450765795351	rwibbun	1722793968
830061590921084960	undead.vampire	1722794048
1127731451253756025	gameslutt	1722794158
907436814925705297	kysathr	1722795542
1195711555447304232	xstarved	1722795878
1079202406006538341	jay.d9	1722796816
864048318556405760	yoveloo	1722797176
1112832044393824309	.harudoll	1722797179
1093621422674432142	rrcapone	1722797884
1172287521422589955	revengerevengerevenge	1722798834
783840111644508160	bunsizedboy	1722798867
720336192628981842	idgaflowla	1722799006
775130043235303455	arewethrough	1722799758
1057910436055490581	diie4your	1722801113
755544681776939008	tucewuce	1722801707
775130043235303455	iplantoleavetheinterent	1722802843
882341102722646077	whatsaheartt3	1722802969
979010120577065021	kimtaehyungcomepegme	1722803021
1025739540725514260	witchcraftlola	1722804394
835772840376008715	monkeybuttari	1722804543
951241304426299393	zx0h.l	1722805399
1021847755460710420	poeta.torturadaa	1722806696
1004273376430411877	adrislover2000	1722807056
806775164972171264	redstone.academics	1722807264
1162313350269636629	solsstices	1722807370
589214848353566739	luvpawzz	1722807557
799390166900801546	9k11_5874	1722807909
550492777490808854	slutchie	1722808303
1222181645738840067	_leesliee	1722808352
806775164972171264	mercenariezz	1722808489
1134175916680024107	zkaxiacensdqq.	1722808675
1134175916680024107	lusiaxdd	1722808897
1168302712681668632	ilovedext	1722809741
1095823651397455914	r6threat.	1722809922
1109855298409213993	chuusarahabaki	1722811079
1104543036056281099	v1rg1nn	1722811260
1135922824075300934	ittybitttymaee	1722811722
915857291843076157	dwllscig	1722811751
1084133590763327548	9.11.bomberme	1722812547
1181660656433369124	ppunkete	1722815487
1181660656433369124	dolljung	1722816099
1187854446470897756	mnnsp	1722813311
1007827457488994315	fwshua	1722817273
999092836836319295	kyianlovesrui	1722813621
1115745338125463663	.hquntedollq	1722815122
1036588330328014968	kid.rape	1722816582
732310214887342110	k.y.s.123	1722817219
512114978732507137	laceribbn	1722817290
578141849332613121	akillerimp	1722817557
1062487545545490442	zayforlife.	1722817826
732310214887342110	hate.niggersz	1722817953
989543768145420328	koalalana.	1722818093
999092836836319295	kyianlovesmylo	1722818376
999092836836319295	kyianlovesrui	1722818410
1163947465444171787	g6bu	1722819486
1184330992073318501	imtryingmyhardest.	1722819827
1203775794992914488	btw_akz	1722821102
1204184953764577328	genkakunahito	1722821645
809980849252466698	emoluv	1722821728
970112484973350932	1lovetyler	1722821874
1203775794992914488	btwikrm	1722821993
1204184953764577328	genkakunahito1	1722822039
1160249184839024662	syth3y	1722822554
1182097785223385222	mya20000000008	1722822557
920661944900395030	triodramas	1722822692
973788647197380638	dorkdorkdordorkdork	1722822775
932312553416171520	blbrady	1722823396
655965792940064778	despairess	1722823920
933154896058925076	soobinsoobing	1722824115
527622118461014027	pankocrmbs.	1722824136
431183027725664257	sp9des	1722824466
1053893435473543289	4xviinv	1722824859
925096747942936577	the_queerestenby	1722825098
792977432105451540	yrenenenenne	1722825224
1107732753014870066	just7myah	1722825310
925096747942936577	the_superstraight	1722825331
1122175095163592805	9vkn	1722826746
1156803057238151190	vampr0ject_w	1722827555
1092160743861919764	desiredtobehiseboy	1722827870
1220866504300560414	.whayyuikkj	1722828505
1097428353432178728	burntyourlovenotes	1722828896
792977432105451540	sswan_lake	1722829675
786199530337075222	funeralknife	1722829890
1117353327823429663	minhotel	1722830099
897222678065344532	rsy.n12	1722830667
1260955952442773595	ffleexy	1722830997
520999050565124125	dqeu	1722831881
1031295935755603980	only4_kb	1722832317
1259709597694824469	28530	1722832619
928117022804549723	x3jl	1722832809
947518417911578734	ilovemybfmeow534	1722833373
795178278600048650	yas5769	1722833930
520999050565124125	____________0003	1722834212
517558169879445534	fraudgeisha	1722835458
1100625878423195679	diacrse	1722835600
1052345826162245682	hauntingmorgue	1722836680
849367692083331074	moossball	1722836757
1103197519825088523	avewaevy	1722836877
1015976677521764432	.jaixz	1722837325
885047453970235402	teriyxaki	1722837619
1021279773923737611	passthablunttososa	1722837675
1109855298409213993	freakyosamu	1722837821
1138619745441165512	so.saaa	1722837855
816474786233450527	latinoluvrrrr	1722838244
813260675803643904	regret.gov	1722838458
942292714588897301	kiya7276	1722838812
1218309682234654802	yocsarah	1722839234
818851140749885480	strqwberriis	1722839269
1000586297330634793	carvvedb	1722839511
1000586297330634793	reynarenn	1722839554
1000586297330634793	carvvedb	1722839572
945508783805845554	seekforguidance	1722839824
945508783805845554	fworgetpaws	1722840047
945508783805845554	seekforguidance	1722840047
770878110522015774	taekeisan.	1722840294
1165109711713091654	ogforeverlastin	1722840445
867253464420450315	ilikemen2927383	1722840927
1247184438522286234	vamp._777	1722842892
856929930461446186	lxte_.	1722843150
1007155219576135770	soulstains	1722845521
1236402028612423750	mandyyyyyyyyyyyyyyyyyyy	1722846802
862446933510979604	tetsutime	1722846835
960476367462477856	strawberrigfie273	1722850186
792008802483961876	mozeqius	1722850848
1129761776012107867	snipedbyscarred	1722851352
792008802483961876	ajiaoqiu	1722851681
867680031382831174	jungwonsfatass	1722852142
1225908069645549672	leakedisla	1722852817
802161951295406121	fashionkillaaa.	1722853123
1198858307851534448	whokilled_jenn	1722853273
1148501433059127318	covetedgirl	1722853675
859299965804085278	love4milfs	1722854289
1148501433059127318	vyseuuu	1722854543
1016967016462159924	rocco.77	1722855456
874900426904989707	phsychadelic.symphony	1722855707
787696601538756648	.mikotokayano.	1722855707
1086865081859579995	angelichweart	1722857029
717463288144986142	poetiqees	1722857070
901482039881134154	chukiyo	1722857957
589214848353566739	wolverinearmpitlicker	1722858166
1144718437877301258	kggabrielz09	1722859704
1141818075793064038	gorification	1722859756
1012692394778570843	iza.wyd	1722860031
901482039881134154	mocamii	1722860151
964253190893764683	l6cl	1722862274
855804241212866560	1ml.syringe	1722862692
1025739540725514260	abby.pawss	1722862692
1180273187699839007	upth	1722863251
734512545850982511	sexbrat	1722864502
1134844244360695828	emawemaaa	1722866368
873301875712200764	rqqqfeen	1722866619
871371842164777011	.wishyoucalled	1722866922
891583409359568956	wave2neveah	1722867784
781865236499398726	alisparadis.com	1722867878
1111776406528081951	imamentalgirl	1722867915
874727933825155103	gollic_1	1722867939
979704330716327986	dedf1shh.	1722868027
1148017316622258276	ilymstupid	1722868515
1224792108691361840	derangedschiphrenicslut	1722868754
923732223943909406	galaxy_glayzz	1722869930
1169348482008617002	xhhhhhhhhhhhhhhhh	1722870026
1150899779975532635	pawpaya	1722871722
1007286475399897178	skibiditoiletfan19738	1722872593
878210674977820692	s7mmerr	1722872658
895400391771049994	eseo._.	1722874119
1058025676395003954	z0mbiegrll	1722874297
719275031863230534	http.inumaki	1722874453
1047630662133350470	deararya	1722876143
761670860175966239	kllstar	1722876191
761670860175966239	toujourscole	1722876294
977704055843463188	h136.	1722876704
1092931334172839978	awourra	1722877660
923411768888422470	pinksamura1	1722877916
1149083662449639586	blwoddycece	1722878903
1219672999557333112	c0rpsette	1722879033
1007534913442021416	444gore	1722879567
837466526524375050	passmeareefa	1722880771
937018261340569660	closetooyouuu	1722881816
1213924010551672903	zaraxsli	1722881962
959961935883931658	kxllswxtch2	1722882277
1148244484270858250	.restlesswithouthim	1722882278
\.


--
-- Data for Name: vcs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vcs (user_id, voice) FROM stdin;
\.


--
-- Data for Name: vm_buttons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vm_buttons (guild_id, action, label, emoji, style) FROM stdin;
950153022405763124	lock		<:lock:1234223571694518333>	gray
950153022405763124	unlock		<:unlock:1234223586412073011>	gray
950153022405763124	hide		<:ghost:1234223641869156362>	gray
950153022405763124	reveal		<:unghost:1234223631056244847>	gray
950153022405763124	rename		<:rename:1234223687679479879>	gray
950153022405763124	decrease		<:minus:1234223725004460053>	gray
950153022405763124	increase		<:plus:1234223750266880051>	gray
950153022405763124	info		<:info:1234223791949746287>	gray
950153022405763124	kick		<:kick:1234223809876463657>	gray
950153022405763124	claim		<:claim:1234223830667624528>	gray
1268777695244980389	lock		<:lock:1234223571694518333>	gray
1268777695244980389	unlock		<:unlock:1234223586412073011>	gray
1268777695244980389	hide		<:ghost:1234223641869156362>	gray
1268777695244980389	reveal		<:unghost:1234223631056244847>	gray
1268777695244980389	rename		<:rename:1234223687679479879>	gray
1268777695244980389	decrease		<:minus:1234223725004460053>	gray
1268777695244980389	increase		<:plus:1234223750266880051>	gray
1268777695244980389	info		<:info:1234223791949746287>	gray
1268777695244980389	kick		<:kick:1234223809876463657>	gray
1268777695244980389	claim		<:claim:1234223830667624528>	gray
1254536563186991184	lock		<:lock:1234223571694518333>	gray
1254536563186991184	unlock		<:unlock:1234223586412073011>	gray
1254536563186991184	hide		<:ghost:1234223641869156362>	gray
1254536563186991184	reveal		<:unghost:1234223631056244847>	gray
1254536563186991184	rename		<:rename:1234223687679479879>	gray
1254536563186991184	decrease		<:minus:1234223725004460053>	gray
1254536563186991184	increase		<:plus:1234223750266880051>	gray
1254536563186991184	info		<:info:1234223791949746287>	gray
1254536563186991184	kick		<:kick:1234223809876463657>	gray
1254536563186991184	claim		<:claim:1234223830667624528>	gray
1202055026797707316	lock		<:lock:1234223571694518333>	gray
1202055026797707316	unlock		<:unlock:1234223586412073011>	gray
1202055026797707316	hide		<:ghost:1234223641869156362>	gray
1202055026797707316	reveal		<:unghost:1234223631056244847>	gray
1202055026797707316	rename		<:rename:1234223687679479879>	gray
1202055026797707316	decrease		<:minus:1234223725004460053>	gray
1202055026797707316	increase		<:plus:1234223750266880051>	gray
1202055026797707316	info		<:info:1234223791949746287>	gray
1202055026797707316	kick		<:kick:1234223809876463657>	gray
1202055026797707316	claim		<:claim:1234223830667624528>	gray
\.


--
-- Data for Name: voicemaster; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.voicemaster (guild_id, channel_id, interface_id) FROM stdin;
1268777695244980389	1269125186490204191	1269125187547168850
950153022405763124	1269411600612331651	1269411601417502853
1254536563186991184	1270004756584202345	1270004758400340022
1202055026797707316	1270033918757699625	1270033920536088627
\.


--
-- Data for Name: warns; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.warns (guild_id, user_id, author_id, "time", reason) FROM stdin;
\.


--
-- Data for Name: webhook; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.webhook (guild_id, code, url, channel, name, avatar) FROM stdin;
\.


--
-- Data for Name: welcome; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.welcome (guild_id, channel_id, message) FROM stdin;
950153022405763124	1269408686628012125	{embed}{content: welcome {user.mention}}$v{description: open a <#1269410533707223208>  to get your server authorized}$v{color: CCCCFF}
1202055026797707316	1269988494319681559	hai {user.mention}
\.


--
-- Data for Name: whitelist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whitelist (guild_id, user_id) FROM stdin;
\.


--
-- Data for Name: whitelist_state; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.whitelist_state (guild_id, embed) FROM stdin;
\.


--
-- Data for Name: xray; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.xray (guild_id, target_id, webhook_url) FROM stdin;
\.


--
-- Name: archive archive_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.archive
    ADD CONSTRAINT archive_pkey PRIMARY KEY (guild_id, channel_id);


--
-- Name: autopfp autopfp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autopfp
    ADD CONSTRAINT autopfp_pkey PRIMARY KEY (guild_id, type, category);


--
-- Name: autoping autoping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoping
    ADD CONSTRAINT autoping_pkey PRIMARY KEY (guild_id, channel_id);


--
-- Name: autoreact autoreact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoreact
    ADD CONSTRAINT autoreact_pkey PRIMARY KEY (guild_id, trigger);


--
-- Name: autoreacts autoreacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoreacts
    ADD CONSTRAINT autoreacts_pkey PRIMARY KEY (guild_id, trigger, reaction);


--
-- Name: autorole autorole_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autorole
    ADD CONSTRAINT autorole_pkey PRIMARY KEY (guild_id, role_id);


--
-- Name: avatar_history avatar_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avatar_history
    ADD CONSTRAINT avatar_history_pkey PRIMARY KEY (user_id);


--
-- Name: avatars avatars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.avatars
    ADD CONSTRAINT avatars_pkey PRIMARY KEY (user_id, key);


--
-- Name: blacklist blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (id, type);


--
-- Name: error_codes error_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.error_codes
    ADD CONSTRAINT error_codes_pkey PRIMARY KEY (code);


--
-- Name: global_disabled_cmds global_disabled_cmds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.global_disabled_cmds
    ADD CONSTRAINT global_disabled_cmds_pkey PRIMARY KEY (cmd);


--
-- Name: jail_members jail_members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jail_members
    ADD CONSTRAINT jail_members_pkey PRIMARY KEY (guild_id, user_id);


--
-- Name: lock_role lock_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lock_role
    ADD CONSTRAINT lock_role_pkey PRIMARY KEY (role_id);


--
-- Name: lockdown_ignore lockdown_ignore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lockdown_ignore
    ADD CONSTRAINT lockdown_ignore_pkey PRIMARY KEY (channel_id);


--
-- Name: logging logging_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logging
    ADD CONSTRAINT logging_pkey PRIMARY KEY (guild_id);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (key);


--
-- Name: number_counter number_counter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.number_counter
    ADD CONSTRAINT number_counter_pkey PRIMARY KEY (guild_id, channel_id);


--
-- Name: restore restore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restore
    ADD CONSTRAINT restore_pkey PRIMARY KEY (guild_id, user_id);


--
-- Name: selfprefix selfprefix_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.selfprefix
    ADD CONSTRAINT selfprefix_pkey PRIMARY KEY (user_id);


--
-- Name: stickymessage stickymessage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stickymessage
    ADD CONSTRAINT stickymessage_pkey PRIMARY KEY (guild_id, channel_id);


--
-- Name: trial trial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trial
    ADD CONSTRAINT trial_pkey PRIMARY KEY (guild_id);


--
-- Name: trials trials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trials
    ADD CONSTRAINT trials_pkey PRIMARY KEY (guild_id);


--
-- Name: whitelist_state whitelist_state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.whitelist_state
    ADD CONSTRAINT whitelist_state_pkey PRIMARY KEY (guild_id);


--
-- PostgreSQL database dump complete
--

