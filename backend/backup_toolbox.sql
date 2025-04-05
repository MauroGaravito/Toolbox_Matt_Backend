--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

-- Started on 2025-04-06 07:43:51

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 868 (class 1247 OID 17352)
-- Name: roleenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roleenum AS ENUM (
    'admin',
    'supervisor',
    'worker'
);


ALTER TYPE public.roleenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 17359)
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_logs (
    id integer NOT NULL,
    user_id integer,
    action character varying NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.activity_logs OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17364)
-- Name: activity_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activity_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_logs_id_seq OWNER TO postgres;

--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 221
-- Name: activity_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activity_logs_id_seq OWNED BY public.activity_logs.id;


--
-- TOC entry 222 (class 1259 OID 17365)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17368)
-- Name: digital_signatures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.digital_signatures (
    id integer NOT NULL,
    user_id integer NOT NULL,
    toolbox_talk_id integer NOT NULL,
    full_name character varying NOT NULL,
    email character varying NOT NULL,
    signed_at timestamp without time zone
);


ALTER TABLE public.digital_signatures OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17373)
-- Name: digital_signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.digital_signatures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.digital_signatures_id_seq OWNER TO postgres;

--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 224
-- Name: digital_signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.digital_signatures_id_seq OWNED BY public.digital_signatures.id;


--
-- TOC entry 217 (class 1259 OID 17064)
-- Name: generated_toolbox_talks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.generated_toolbox_talks (
    id integer NOT NULL,
    topic character varying NOT NULL,
    content text NOT NULL,
    created_by integer,
    created_at timestamp without time zone
);


ALTER TABLE public.generated_toolbox_talks OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17374)
-- Name: generated_toolbox_talks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.generated_toolbox_talks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.generated_toolbox_talks_id_seq OWNER TO postgres;

--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 225
-- Name: generated_toolbox_talks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.generated_toolbox_talks_id_seq OWNED BY public.generated_toolbox_talks.id;


--
-- TOC entry 226 (class 1259 OID 17375)
-- Name: reference_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reference_documents (
    id integer NOT NULL,
    uploaded_by integer,
    file_name character varying NOT NULL,
    file_path character varying NOT NULL,
    uploaded_at timestamp without time zone,
    toolbox_talk_id integer
);


ALTER TABLE public.reference_documents OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17380)
-- Name: reference_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reference_documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reference_documents_id_seq OWNER TO postgres;

--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 227
-- Name: reference_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reference_documents_id_seq OWNED BY public.reference_documents.id;


--
-- TOC entry 228 (class 1259 OID 17381)
-- Name: signatures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.signatures (
    id integer NOT NULL,
    toolbox_talk_id integer,
    signer_name character varying NOT NULL,
    signer_email character varying,
    signature_image text,
    signed_at timestamp without time zone
);


ALTER TABLE public.signatures OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17386)
-- Name: signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.signatures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.signatures_id_seq OWNER TO postgres;

--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 229
-- Name: signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.signatures_id_seq OWNED BY public.signatures.id;


--
-- TOC entry 230 (class 1259 OID 17387)
-- Name: toolbox_talk_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.toolbox_talk_participants (
    id integer NOT NULL,
    toolbox_talk_id integer,
    user_id integer,
    assigned_at timestamp without time zone
);


ALTER TABLE public.toolbox_talk_participants OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17390)
-- Name: toolbox_talk_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.toolbox_talk_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.toolbox_talk_participants_id_seq OWNER TO postgres;

--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 231
-- Name: toolbox_talk_participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.toolbox_talk_participants_id_seq OWNED BY public.toolbox_talk_participants.id;


--
-- TOC entry 232 (class 1259 OID 17391)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    email character varying,
    hashed_password character varying,
    role public.roleenum,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17396)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 219 (class 1259 OID 17337)
-- Name: vector_indexes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vector_indexes (
    id integer NOT NULL,
    toolbox_talk_id integer NOT NULL,
    file_path_index character varying NOT NULL,
    file_path_metadata character varying NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.vector_indexes OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17336)
-- Name: vector_indexes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vector_indexes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vector_indexes_id_seq OWNER TO postgres;

--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 218
-- Name: vector_indexes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vector_indexes_id_seq OWNED BY public.vector_indexes.id;


--
-- TOC entry 4739 (class 2604 OID 17397)
-- Name: activity_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs ALTER COLUMN id SET DEFAULT nextval('public.activity_logs_id_seq'::regclass);


--
-- TOC entry 4740 (class 2604 OID 17398)
-- Name: digital_signatures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_signatures ALTER COLUMN id SET DEFAULT nextval('public.digital_signatures_id_seq'::regclass);


--
-- TOC entry 4737 (class 2604 OID 17399)
-- Name: generated_toolbox_talks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.generated_toolbox_talks ALTER COLUMN id SET DEFAULT nextval('public.generated_toolbox_talks_id_seq'::regclass);


--
-- TOC entry 4741 (class 2604 OID 17400)
-- Name: reference_documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reference_documents ALTER COLUMN id SET DEFAULT nextval('public.reference_documents_id_seq'::regclass);


--
-- TOC entry 4742 (class 2604 OID 17401)
-- Name: signatures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.signatures ALTER COLUMN id SET DEFAULT nextval('public.signatures_id_seq'::regclass);


--
-- TOC entry 4743 (class 2604 OID 17402)
-- Name: toolbox_talk_participants id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.toolbox_talk_participants ALTER COLUMN id SET DEFAULT nextval('public.toolbox_talk_participants_id_seq'::regclass);


--
-- TOC entry 4744 (class 2604 OID 17403)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4738 (class 2604 OID 17340)
-- Name: vector_indexes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vector_indexes ALTER COLUMN id SET DEFAULT nextval('public.vector_indexes_id_seq'::regclass);


--
-- TOC entry 4932 (class 0 OID 17359)
-- Dependencies: 220
-- Data for Name: activity_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_logs (id, user_id, action, "timestamp") FROM stdin;
\.


--
-- TOC entry 4934 (class 0 OID 17365)
-- Dependencies: 222
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
464abfb20e3b
\.


--
-- TOC entry 4935 (class 0 OID 17368)
-- Dependencies: 223
-- Data for Name: digital_signatures; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.digital_signatures (id, user_id, toolbox_talk_id, full_name, email, signed_at) FROM stdin;
19	1	13	Mauricio Garavito	contact@downundersolutions.com	2025-03-28 22:55:45.087901
20	1	13	Pepe	contact1@downundersolutions.com	2025-03-28 22:56:09.57267
26	1	13	daniel	daniel@test.com	2025-03-31 03:44:46.675247
\.


--
-- TOC entry 4929 (class 0 OID 17064)
-- Dependencies: 217
-- Data for Name: generated_toolbox_talks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.generated_toolbox_talks (id, topic, content, created_by, created_at) FROM stdin;
13	Working at Heights replacing high tension cables	# Toolbox Talk: Working at Heights – Replacing High Tension Cables\n\n**Introduction**\n\nWorking at heights is a critical safety concern in the construction and electrical industries, particularly when replacing high tension cables. This Toolbox Talk aims to outline the hazards associated with this task, the necessary risk controls, and important discussion points to ensure the safety of all personnel involved. The guidelines and information presented in this document are based on the Safe Work Australia Model Code of Practice – Construction Work (November 2024) and the Managing the Risk of Falls at Workplaces Code of Practice (August 2019).\n\n**Hazards**\n\nThe hazards associated with working at heights when replacing high tension cables include, but are not limited to:\n\n1. **Falls from Height**: The primary risk involves falling from ladders, scaffolds, or other elevated structures. For example, an individual working on a ladder to reach electrical connections may lose balance and fall, resulting in serious injury.\n\n2. **Electrical Shock**: High tension cables carry significant electrical currents. Contact with these cables can lead to electric shocks, which can be fatal. For instance, if a worker inadvertently touches an exposed cable while attempting to replace it, they may suffer severe injuries.\n\n3. **Falling Objects**: Tools or materials can fall from heights, posing a risk to individuals below. An example includes a tool slipping from a scaffold and striking a worker on the ground.\n\n4. **Weather Conditions**: Wind, rain, or extreme temperatures can exacerbate the risks associated with working at heights. For example, wet surfaces can lead to slips and falls, while strong winds can destabilize ladders or scaffolding.\n\n5. **Inadequate Training**: Workers who are not adequately trained in working at heights or electrical safety may inadvertently increase their risk of injury.\n\n**Risk Controls**\n\nTo mitigate the identified hazards, the following risk control measures should be implemented:\n\n1. **Planning and Preparation**: Conduct a thorough risk assessment before beginning work. This includes identifying potential hazards, reviewing weather conditions, and ensuring all equipment is fit for purpose.\n\n2. **Use of Personal Protective Equipment (PPE)**: Ensure that all workers are equipped with appropriate PPE, such as hard hats, safety harnesses, and non-slip footwear. For example, a safety harness should be worn when working from heights to prevent falls.\n\n3. **Safe Work Method Statements (SWMS)**: Develop and adhere to a SWMS that outlines the specific procedures for replacing high tension cables at heights. This document should include emergency procedures and outline the use of fall protection systems.\n\n4. **Fall Protection Systems**: Implement fall protection measures, including guardrails, safety nets, and harness systems. For instance, installing guardrails around the work area can prevent falls from edges.\n\n5. **Training and Competency**: Ensure all personnel involved are adequately trained in working at heights and electrical safety. Regular training should be scheduled to keep skills current.\n\n6. **Supervision**: Designate a competent supervisor to oversee operations. This supervisor should be responsible for ensuring compliance with safety procedures and addressing any unsafe practices.\n\n**Discussion Points**\n\n1. **Personal Experiences**: Encourage workers to share any previous experiences related to working at heights or with high tension cables and discuss the lessons learned.\n\n2. **Emergency Procedures**: Review emergency procedures in case of a fall or electrical incident, including the location of first aid kits and emergency contact numbers.\n\n3. **Reporting Unsafe Conditions**: Discuss the importance of reporting unsafe conditions or practices to supervisors immediately.\n\n4. **Daily Safety Checks**: Highlight the necessity of conducting daily safety checks on equipment and work areas to identify potential hazards before commencing work.\n\n5. **Team Communication**: Emphasize the importance of clear communication among team members during operations, particularly when working at heights.\n\n**Conclusion**\n\nWorking at heights to replace high tension cables presents significant hazards that require diligent risk management and control measures. By adhering to the guidelines outlined in the Model Code of Practice – Construction Work and implementing the recommended risk controls, the safety of all personnel can be significantly enhanced. Ongoing training, effective communication, and a commitment to safety are essential to prevent accidents and ensure a safe working environment. It is imperative that all workers remain vigilant and proactive in identifying and mitigating risks associated with working at heights.	1	2025-03-28 22:52:20.299999
\.


--
-- TOC entry 4938 (class 0 OID 17375)
-- Dependencies: 226
-- Data for Name: reference_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reference_documents (id, uploaded_by, file_name, file_path, uploaded_at, toolbox_talk_id) FROM stdin;
33	1	20250329095300_Managing-electrical-risks-in-the-workplace-COP.pdf	backend/uploads\\20250329095300_Managing-electrical-risks-in-the-workplace-COP.pdf	2025-03-28 22:53:00.132889	13
34	1	20250329095346_Managing-the-risk-of-falls-at-workplaces-COP.pdf	backend/uploads\\20250329095346_Managing-the-risk-of-falls-at-workplaces-COP.pdf	2025-03-28 22:53:46.557098	13
\.


--
-- TOC entry 4940 (class 0 OID 17381)
-- Dependencies: 228
-- Data for Name: signatures; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.signatures (id, toolbox_talk_id, signer_name, signer_email, signature_image, signed_at) FROM stdin;
8	13	Mauricio Garavito	contact@downundersolutions.com	data:image/png;base64,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	2025-03-28 22:55:45.104783
9	13	Pepe	contact1@downundersolutions.com	data:image/png;base64,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	2025-03-28 22:56:09.583726
15	13	daniel	daniel@test.com	data:image/png;base64,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	2025-03-31 03:44:46.683358
\.


--
-- TOC entry 4942 (class 0 OID 17387)
-- Dependencies: 230
-- Data for Name: toolbox_talk_participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.toolbox_talk_participants (id, toolbox_talk_id, user_id, assigned_at) FROM stdin;
\.


--
-- TOC entry 4944 (class 0 OID 17391)
-- Dependencies: 232
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, hashed_password, role, created_at) FROM stdin;
1	mauro	contact@downundersolutions.com	$2b$12$KUyGjcakru04zPaqa6vkDeejE.Usuhm1at3gfKRRY9XkMSOicp6je	admin	2025-03-22 13:47:56.646563
7	worker	test@test.com	$2b$12$gm1vqvtBOWHsn71qbhHKvemE57KBigYQ41y3K/2JD9oZmeyGfMP5y	worker	2025-03-24 02:49:31.234875
10	daniel	daniel@test.com	$2b$12$luJBHah/SrzY0i5IgpD.rOATh54tL32a/MxS9997XxjQCCr2Kgnqq	worker	2025-03-30 23:39:16.380573
\.


--
-- TOC entry 4931 (class 0 OID 17337)
-- Dependencies: 219
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vector_indexes (id, toolbox_talk_id, file_path_index, file_path_metadata, created_at) FROM stdin;
\.


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 221
-- Name: activity_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.activity_logs_id_seq', 1, false);


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 224
-- Name: digital_signatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.digital_signatures_id_seq', 26, true);


--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 225
-- Name: generated_toolbox_talks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.generated_toolbox_talks_id_seq', 13, true);


--
-- TOC entry 4962 (class 0 OID 0)
-- Dependencies: 227
-- Name: reference_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reference_documents_id_seq', 34, true);


--
-- TOC entry 4963 (class 0 OID 0)
-- Dependencies: 229
-- Name: signatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.signatures_id_seq', 15, true);


--
-- TOC entry 4964 (class 0 OID 0)
-- Dependencies: 231
-- Name: toolbox_talk_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.toolbox_talk_participants_id_seq', 10, true);


--
-- TOC entry 4965 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 4966 (class 0 OID 0)
-- Dependencies: 218
-- Name: vector_indexes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vector_indexes_id_seq', 1, false);


--
-- TOC entry 4752 (class 2606 OID 17409)
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4755 (class 2606 OID 17411)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4757 (class 2606 OID 17413)
-- Name: digital_signatures digital_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_signatures
    ADD CONSTRAINT digital_signatures_pkey PRIMARY KEY (id);


--
-- TOC entry 4746 (class 2606 OID 17071)
-- Name: generated_toolbox_talks generated_toolbox_talks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.generated_toolbox_talks
    ADD CONSTRAINT generated_toolbox_talks_pkey PRIMARY KEY (id);


--
-- TOC entry 4761 (class 2606 OID 17415)
-- Name: reference_documents reference_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reference_documents
    ADD CONSTRAINT reference_documents_pkey PRIMARY KEY (id);


--
-- TOC entry 4764 (class 2606 OID 17417)
-- Name: signatures signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.signatures
    ADD CONSTRAINT signatures_pkey PRIMARY KEY (id);


--
-- TOC entry 4767 (class 2606 OID 17419)
-- Name: toolbox_talk_participants toolbox_talk_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.toolbox_talk_participants
    ADD CONSTRAINT toolbox_talk_participants_pkey PRIMARY KEY (id);


--
-- TOC entry 4772 (class 2606 OID 17421)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4750 (class 2606 OID 17344)
-- Name: vector_indexes vector_indexes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vector_indexes
    ADD CONSTRAINT vector_indexes_pkey PRIMARY KEY (id);


--
-- TOC entry 4753 (class 1259 OID 17422)
-- Name: ix_activity_logs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_logs_id ON public.activity_logs USING btree (id);


--
-- TOC entry 4758 (class 1259 OID 17423)
-- Name: ix_digital_signatures_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_signatures_id ON public.digital_signatures USING btree (id);


--
-- TOC entry 4747 (class 1259 OID 17424)
-- Name: ix_generated_toolbox_talks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_generated_toolbox_talks_id ON public.generated_toolbox_talks USING btree (id);


--
-- TOC entry 4759 (class 1259 OID 17425)
-- Name: ix_reference_documents_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reference_documents_id ON public.reference_documents USING btree (id);


--
-- TOC entry 4762 (class 1259 OID 17426)
-- Name: ix_signatures_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_signatures_id ON public.signatures USING btree (id);


--
-- TOC entry 4765 (class 1259 OID 17427)
-- Name: ix_toolbox_talk_participants_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_toolbox_talk_participants_id ON public.toolbox_talk_participants USING btree (id);


--
-- TOC entry 4768 (class 1259 OID 17428)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4769 (class 1259 OID 17429)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 4770 (class 1259 OID 17430)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 4748 (class 1259 OID 17350)
-- Name: ix_vector_indexes_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_vector_indexes_id ON public.vector_indexes USING btree (id);


--
-- TOC entry 4775 (class 2606 OID 17431)
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4776 (class 2606 OID 17436)
-- Name: digital_signatures digital_signatures_toolbox_talk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_signatures
    ADD CONSTRAINT digital_signatures_toolbox_talk_id_fkey FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


--
-- TOC entry 4777 (class 2606 OID 17441)
-- Name: digital_signatures digital_signatures_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_signatures
    ADD CONSTRAINT digital_signatures_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4778 (class 2606 OID 17446)
-- Name: reference_documents fk_reference_documents_toolbox_talk_id_generated_toolbox_talks; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reference_documents
    ADD CONSTRAINT fk_reference_documents_toolbox_talk_id_generated_toolbox_talks FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


--
-- TOC entry 4773 (class 2606 OID 17451)
-- Name: generated_toolbox_talks generated_toolbox_talks_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.generated_toolbox_talks
    ADD CONSTRAINT generated_toolbox_talks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 4779 (class 2606 OID 17456)
-- Name: reference_documents reference_documents_toolbox_talk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reference_documents
    ADD CONSTRAINT reference_documents_toolbox_talk_id_fkey FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


--
-- TOC entry 4780 (class 2606 OID 17461)
-- Name: reference_documents reference_documents_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reference_documents
    ADD CONSTRAINT reference_documents_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id);


--
-- TOC entry 4781 (class 2606 OID 17466)
-- Name: signatures signatures_toolbox_talk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.signatures
    ADD CONSTRAINT signatures_toolbox_talk_id_fkey FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


--
-- TOC entry 4782 (class 2606 OID 17471)
-- Name: toolbox_talk_participants toolbox_talk_participants_toolbox_talk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.toolbox_talk_participants
    ADD CONSTRAINT toolbox_talk_participants_toolbox_talk_id_fkey FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


--
-- TOC entry 4783 (class 2606 OID 17476)
-- Name: toolbox_talk_participants toolbox_talk_participants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.toolbox_talk_participants
    ADD CONSTRAINT toolbox_talk_participants_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4774 (class 2606 OID 17345)
-- Name: vector_indexes vector_indexes_toolbox_talk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vector_indexes
    ADD CONSTRAINT vector_indexes_toolbox_talk_id_fkey FOREIGN KEY (toolbox_talk_id) REFERENCES public.generated_toolbox_talks(id);


-- Completed on 2025-04-06 07:43:58

--
-- PostgreSQL database dump complete
--

