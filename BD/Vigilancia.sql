--
-- PostgreSQL database dump
--

-- Dumped from database version 17.1 (Debian 17.1-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

-- Started on 2025-04-06 00:54:57

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 16489)
-- Name: ACCIONES; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ACCIONES" (
    escenario integer NOT NULL,
    id_dispositivo text NOT NULL,
    comando text NOT NULL,
    orden integer NOT NULL
);


ALTER TABLE public."ACCIONES" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16409)
-- Name: CONDICIONES_MANUALES; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CONDICIONES_MANUALES" (
    nombre text NOT NULL,
    descripcion text NOT NULL,
    seleccionado boolean DEFAULT false NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public."CONDICIONES_MANUALES" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16438)
-- Name: DATOS_SENSIBLES; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DATOS_SENSIBLES" (
    id integer NOT NULL,
    key_name text NOT NULL,
    value bytea NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public."DATOS_SENSIBLES" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16402)
-- Name: ESCENARIOS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ESCENARIOS" (
    id integer NOT NULL,
    nombre text NOT NULL,
    descripcion text NOT NULL
);


ALTER TABLE public."ESCENARIOS" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16395)
-- Name: EVENTOS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EVENTOS" (
    nombre text NOT NULL,
    descripcion text NOT NULL,
    dispositivo_origen text NOT NULL,
    tipo text NOT NULL,
    id integer NOT NULL,
    url text NOT NULL,
    titulo text NOT NULL,
    canal_notificacion text DEFAULT 'CanalVigilancia'::text,
    destinatarios text[]
);


ALTER TABLE public."EVENTOS" OWNER TO postgres;

--
-- TOC entry 3425 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE "EVENTOS"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."EVENTOS" IS 'Tabla de definición de eventos.';


--
-- TOC entry 224 (class 1259 OID 16463)
-- Name: EVENTO_CONDICION_ESCENARIO; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EVENTO_CONDICION_ESCENARIO" (
    evento integer NOT NULL,
    condicion integer NOT NULL,
    escenario integer NOT NULL
);


ALTER TABLE public."EVENTO_CONDICION_ESCENARIO" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16388)
-- Name: USUARIOS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."USUARIOS" (
    usuario text NOT NULL,
    clave bytea NOT NULL
);


ALTER TABLE public."USUARIOS" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16473)
-- Name: condiciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.condiciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.condiciones_id_seq OWNER TO postgres;

--
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 225
-- Name: condiciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.condiciones_id_seq OWNED BY public."CONDICIONES_MANUALES".id;


--
-- TOC entry 221 (class 1259 OID 16437)
-- Name: datos_sensibles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datos_sensibles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datos_sensibles_id_seq OWNER TO postgres;

--
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 221
-- Name: datos_sensibles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datos_sensibles_id_seq OWNED BY public."DATOS_SENSIBLES".id;


--
-- TOC entry 226 (class 1259 OID 16487)
-- Name: escenario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.escenario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.escenario_id_seq OWNER TO postgres;

--
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 226
-- Name: escenario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.escenario_id_seq OWNED BY public."ESCENARIOS".id;


--
-- TOC entry 223 (class 1259 OID 16452)
-- Name: eventos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eventos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.eventos_id_seq OWNER TO postgres;

--
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 223
-- Name: eventos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eventos_id_seq OWNED BY public."EVENTOS".id;


--
-- TOC entry 3241 (class 2604 OID 16474)
-- Name: CONDICIONES_MANUALES id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CONDICIONES_MANUALES" ALTER COLUMN id SET DEFAULT nextval('public.condiciones_id_seq'::regclass);

--
-- TOC entry 3242 (class 2604 OID 16441)
-- Name: DATOS_SENSIBLES id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DATOS_SENSIBLES" ALTER COLUMN id SET DEFAULT nextval('public.datos_sensibles_id_seq'::regclass);


--
-- TOC entry 3239 (class 2604 OID 16488)
-- Name: ESCENARIOS id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ESCENARIOS" ALTER COLUMN id SET DEFAULT nextval('public.escenario_id_seq'::regclass);


--
-- TOC entry 3237 (class 2604 OID 16453)
-- Name: EVENTOS id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTOS" ALTER COLUMN id SET DEFAULT nextval('public.eventos_id_seq'::regclass);

--
-- TOC entry 3258 (class 2606 OID 16505)
-- Name: ACCIONES ACCIONES_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ACCIONES"
    ADD CONSTRAINT "ACCIONES_pkey" PRIMARY KEY (escenario, orden);


--
-- TOC entry 3251 (class 2606 OID 16472)
-- Name: CONDICIONES_MANUALES CONDICIONES_MANUALES_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CONDICIONES_MANUALES"
    ADD CONSTRAINT "CONDICIONES_MANUALES_pkey" PRIMARY KEY (id);


--
-- TOC entry 3249 (class 2606 OID 16486)
-- Name: ESCENARIOS ESCENARIOS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ESCENARIOS"
    ADD CONSTRAINT "ESCENARIOS_pkey" PRIMARY KEY (id);


--
-- TOC entry 3247 (class 2606 OID 16451)
-- Name: EVENTOS EVENTOS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTOS"
    ADD CONSTRAINT "EVENTOS_pkey" PRIMARY KEY (id);


--
-- TOC entry 3256 (class 2606 OID 16507)
-- Name: EVENTO_CONDICION_ESCENARIO EVENTO_CONDICION_ESCENARIO_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTO_CONDICION_ESCENARIO"
    ADD CONSTRAINT "EVENTO_CONDICION_ESCENARIO_pkey" PRIMARY KEY (evento, condicion, escenario);


--
-- TOC entry 3245 (class 2606 OID 16394)
-- Name: USUARIOS USUARIOS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."USUARIOS"
    ADD CONSTRAINT "USUARIOS_pkey" PRIMARY KEY (usuario);


--
-- TOC entry 3254 (class 2606 OID 16446)
-- Name: DATOS_SENSIBLES datos_sensibles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DATOS_SENSIBLES"
    ADD CONSTRAINT datos_sensibles_pkey PRIMARY KEY (id);


--
-- TOC entry 3252 (class 1259 OID 16449)
-- Name: unico_seleccionado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unico_seleccionado ON public."CONDICIONES_MANUALES" USING btree (seleccionado) WHERE (seleccionado = true);


--
-- TOC entry 3259 (class 2606 OID 16480)
-- Name: EVENTO_CONDICION_ESCENARIO fk_condicion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTO_CONDICION_ESCENARIO"
    ADD CONSTRAINT fk_condicion FOREIGN KEY (condicion) REFERENCES public."CONDICIONES_MANUALES"(id) NOT VALID;


--
-- TOC entry 3262 (class 2606 OID 16492)
-- Name: ACCIONES fk_escenario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ACCIONES"
    ADD CONSTRAINT fk_escenario FOREIGN KEY (escenario) REFERENCES public."ESCENARIOS"(id) NOT VALID;


--
-- TOC entry 3260 (class 2606 OID 16497)
-- Name: EVENTO_CONDICION_ESCENARIO fk_escenario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTO_CONDICION_ESCENARIO"
    ADD CONSTRAINT fk_escenario FOREIGN KEY (escenario) REFERENCES public."ESCENARIOS"(id) NOT VALID;


--
-- TOC entry 3261 (class 2606 OID 16466)
-- Name: EVENTO_CONDICION_ESCENARIO fk_evento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EVENTO_CONDICION_ESCENARIO"
    ADD CONSTRAINT fk_evento FOREIGN KEY (evento) REFERENCES public."EVENTOS"(id) NOT VALID;


-- Completed on 2025-04-06 00:54:57

--
-- PostgreSQL database dump complete
--

