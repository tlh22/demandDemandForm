/***
Setup details for demand
***/

DROP TABLE IF EXISTS demand."RestrictionsInSurveys" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys"
(
    "SurveyID" integer,
    "GeometryID" character varying(12) COLLATE pg_catalog."default",
    "DemandSurveyDateTime" timestamp without time zone,
    "Enumerator" character varying (100) COLLATE pg_catalog."default",
    "Done" boolean,
    "SuspensionReference" character varying (100) COLLATE pg_catalog."default",
    "SuspensionReason" character varying (255) COLLATE pg_catalog."default",
    "SuspensionLength" double precision,
    "NrBaysSuspended" integer,
    "SuspensionNotes" character varying (255) COLLATE pg_catalog."default",
    "Photos_01" character varying (255) COLLATE pg_catalog."default",
    "Photos_02" character varying (255) COLLATE pg_catalog."default",
    "Photos_03" character varying (255) COLLATE pg_catalog."default",
    geom geometry(LineString,27700) NOT NULL,
	CONSTRAINT "RestrictionsInSurveys_pkey" PRIMARY KEY ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys"
    OWNER to postgres;

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", gid::text AS "GeometryID", r.geom As geom
FROM mhtc_operations."RC_Sections_merged" r, demand."Surveys";


---
DROP TABLE IF EXISTS demand."RestrictionsInSurveys_TN" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys_TN"
(
    "SurveyID" integer,
    "GeometryID" character varying(12) COLLATE pg_catalog."default",
    "DemandSurveyDateTime" timestamp without time zone,
    "Enumerator" character varying (100) COLLATE pg_catalog."default",
    "Done" boolean,
    "SuspensionReference" character varying (100) COLLATE pg_catalog."default",
    "SuspensionReason" character varying (255) COLLATE pg_catalog."default",
    "SuspensionLength" double precision,
    "NrBaysSuspended" integer,
    "SuspensionNotes" character varying (255) COLLATE pg_catalog."default",
    "Photos_01" character varying (255) COLLATE pg_catalog."default",
    "Photos_02" character varying (255) COLLATE pg_catalog."default",
    "Photos_03" character varying (255) COLLATE pg_catalog."default",
    geom geometry(LineString,27700) NOT NULL,
	CONSTRAINT "RestrictionsInSurveys_TN_pkey" PRIMARY KEY ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys_TN"
    OWNER to postgres;

INSERT INTO demand."RestrictionsInSurveys_TN" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", s."GeometryID", s.geom As geom
FROM mhtc_operations."Supply" s, demand."Surveys" su
WHERE s."CPZ" = 'TN'
AND substring(su."SurveyDay" from '\((.+)\)') = 'TN';


