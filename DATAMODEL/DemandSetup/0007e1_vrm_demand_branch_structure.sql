
-- Demand

CREATE SEQUENCE "demand"."Demand_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE "demand"."Demand_id_seq" OWNER TO "postgres";

DROP TABLE IF EXISTS "demand"."VRM_DemandStem";
CREATE TABLE "demand"."VRM_DemandStem" (
    "id" integer DEFAULT "nextval"('"demand"."Demand_id_seq"'::"regclass") NOT NULL,
    "GeometryID" character varying(12) NOT NULL,
    "SectionID" integer,
    "SurveyID" integer,
    "DemandSurveyDateTime" timestamp without time zone,
    "Done" boolean,
    "SuspensionReference" character varying (100) COLLATE pg_catalog."default",
    "SuspensionReason" character varying (255) COLLATE pg_catalog."default",
    "SuspensionLength" double precision,
    "NrBaysSuspended" integer,
    "SuspensionNotes" character varying (255) COLLATE pg_catalog."default"
    "Photos_01" character varying (255) COLLATE pg_catalog."default",
    "Photos_02" character varying (255) COLLATE pg_catalog."default",
    "Photos_03" character varying (255) COLLATE pg_catalog."default",
    "VRM_01" character varying (12) COLLATE pg_catalog."default",
    "VRM_02" character varying (12) COLLATE pg_catalog."default",
    "VRM_03" character varying (12) COLLATE pg_catalog."default",
    "VRM_04" character varying (12) COLLATE pg_catalog."default",
    "VRM_05" character varying (12) COLLATE pg_catalog."default",
    "VRM_06" character varying (12) COLLATE pg_catalog."default",
    "VRM_07" character varying (12) COLLATE pg_catalog."default",
    "VRM_08" character varying (12) COLLATE pg_catalog."default",
    "VRM_09" character varying (12) COLLATE pg_catalog."default",
    "VRM_10" character varying (12) COLLATE pg_catalog."default",
    "VRM_11" character varying (12) COLLATE pg_catalog."default",
    "VRM_12" character varying (12) COLLATE pg_catalog."default",
    "VRM_13" character varying (12) COLLATE pg_catalog."default",
    "VRM_14" character varying (12) COLLATE pg_catalog."default",
    "VRM_15" character varying (12) COLLATE pg_catalog."default",
    "VRM_16" character varying (12) COLLATE pg_catalog."default",
    "VRM_17" character varying (12) COLLATE pg_catalog."default",
    "VRM_18" character varying (12) COLLATE pg_catalog."default",
    "VRM_19" character varying (12) COLLATE pg_catalog."default",
    "VRM_20" character varying (12) COLLATE pg_catalog."default",
    "VRM_21" character varying (12) COLLATE pg_catalog."default",
    "VRM_22" character varying (12) COLLATE pg_catalog."default",
    "VRM_23" character varying (12) COLLATE pg_catalog."default",
    "VRM_24" character varying (12) COLLATE pg_catalog."default",
    "VRM_25" character varying (12) COLLATE pg_catalog."default",
    "VRM_26" character varying (12) COLLATE pg_catalog."default",
    "VRM_27" character varying (12) COLLATE pg_catalog."default",
    "VRM_28" character varying (12) COLLATE pg_catalog."default",
    "VRM_29" character varying (12) COLLATE pg_catalog."default",
    "VRM_30" character varying (12) COLLATE pg_catalog."default",
    "VRM_31" character varying (12) COLLATE pg_catalog."default",
    "VRM_32" character varying (12) COLLATE pg_catalog."default",
    "VRM_33" character varying (12) COLLATE pg_catalog."default",
    "VRM_34" character varying (12) COLLATE pg_catalog."default",
    "VRM_35" character varying (12) COLLATE pg_catalog."default",
    "VRM_36" character varying (12) COLLATE pg_catalog."default",
    "VRM_37" character varying (12) COLLATE pg_catalog."default",
    "VRM_38" character varying (12) COLLATE pg_catalog."default",
    "VRM_39" character varying (12) COLLATE pg_catalog."default",
    "VRM_40" character varying (12) COLLATE pg_catalog."default",
    "VRM_41" character varying (12) COLLATE pg_catalog."default",
    "VRM_42" character varying (12) COLLATE pg_catalog."default",
    "VRM_43" character varying (12) COLLATE pg_catalog."default",
    "VRM_44" character varying (12) COLLATE pg_catalog."default",
    "VRM_45" character varying (12) COLLATE pg_catalog."default",
    "VRM_46" character varying (12) COLLATE pg_catalog."default",
    "VRM_47" character varying (12) COLLATE pg_catalog."default",
    "VRM_48" character varying (12) COLLATE pg_catalog."default",
    "VRM_49" character varying (12) COLLATE pg_catalog."default",
    "VRM_50" character varying (12) COLLATE pg_catalog."default",
    "VehicleTypeID_01" integer,
    "VehicleTypeID_02" integer,
    "VehicleTypeID_03" integer,
    "VehicleTypeID_04" integer,
    "VehicleTypeID_05" integer,
    "VehicleTypeID_06" integer,
    "VehicleTypeID_07" integer,
    "VehicleTypeID_08" integer,
    "VehicleTypeID_09" integer,
    "VehicleTypeID_10" integer,
    "VehicleTypeID_11" integer,
    "VehicleTypeID_12" integer,
    "VehicleTypeID_13" integer,
    "VehicleTypeID_14" integer,
    "VehicleTypeID_15" integer,
    "VehicleTypeID_16" integer,
    "VehicleTypeID_17" integer,
    "VehicleTypeID_18" integer,
    "VehicleTypeID_19" integer,
    "VehicleTypeID_20" integer,
    "VehicleTypeID_21" integer,
    "VehicleTypeID_22" integer,
    "VehicleTypeID_23" integer,
    "VehicleTypeID_24" integer,
    "VehicleTypeID_25" integer,
    "VehicleTypeID_26" integer,
    "VehicleTypeID_27" integer,
    "VehicleTypeID_28" integer,
    "VehicleTypeID_29" integer,
    "VehicleTypeID_30" integer,
    "VehicleTypeID_31" integer,
    "VehicleTypeID_32" integer,
    "VehicleTypeID_33" integer,
    "VehicleTypeID_34" integer,
    "VehicleTypeID_35" integer,
    "VehicleTypeID_36" integer,
    "VehicleTypeID_37" integer,
    "VehicleTypeID_38" integer,
    "VehicleTypeID_39" integer,
    "VehicleTypeID_40" integer,
    "VehicleTypeID_41" integer,
    "VehicleTypeID_42" integer,
    "VehicleTypeID_43" integer,
    "VehicleTypeID_44" integer,
    "VehicleTypeID_45" integer,
    "VehicleTypeID_46" integer,
    "VehicleTypeID_47" integer,
    "VehicleTypeID_48" integer,
    "VehicleTypeID_49" integer,
    "VehicleTypeID_50" integer,
    "Notes_01" character varying (255) COLLATE pg_catalog."default",
    "Notes_02" character varying (255) COLLATE pg_catalog."default",
    "Notes_03" character varying (255) COLLATE pg_catalog."default",
    "Notes_04" character varying (255) COLLATE pg_catalog."default",
    "Notes_05" character varying (255) COLLATE pg_catalog."default",
    "Notes_06" character varying (255) COLLATE pg_catalog."default",
    "Notes_07" character varying (255) COLLATE pg_catalog."default",
    "Notes_08" character varying (255) COLLATE pg_catalog."default",
    "Notes_09" character varying (255) COLLATE pg_catalog."default",
    "Notes_10" character varying (255) COLLATE pg_catalog."default",
    "Notes_11" character varying (255) COLLATE pg_catalog."default",
    "Notes_12" character varying (255) COLLATE pg_catalog."default",
    "Notes_13" character varying (255) COLLATE pg_catalog."default",
    "Notes_14" character varying (255) COLLATE pg_catalog."default",
    "Notes_15" character varying (255) COLLATE pg_catalog."default",
    "Notes_16" character varying (255) COLLATE pg_catalog."default",
    "Notes_17" character varying (255) COLLATE pg_catalog."default",
    "Notes_18" character varying (255) COLLATE pg_catalog."default",
    "Notes_19" character varying (255) COLLATE pg_catalog."default",
    "Notes_20" character varying (255) COLLATE pg_catalog."default",
    "Notes_21" character varying (255) COLLATE pg_catalog."default",
    "Notes_22" character varying (255) COLLATE pg_catalog."default",
    "Notes_23" character varying (255) COLLATE pg_catalog."default",
    "Notes_24" character varying (255) COLLATE pg_catalog."default",
    "Notes_25" character varying (255) COLLATE pg_catalog."default",
    "Notes_26" character varying (255) COLLATE pg_catalog."default",
    "Notes_27" character varying (255) COLLATE pg_catalog."default",
    "Notes_28" character varying (255) COLLATE pg_catalog."default",
    "Notes_29" character varying (255) COLLATE pg_catalog."default",
    "Notes_30" character varying (255) COLLATE pg_catalog."default",
    "Notes_31" character varying (255) COLLATE pg_catalog."default",
    "Notes_32" character varying (255) COLLATE pg_catalog."default",
    "Notes_33" character varying (255) COLLATE pg_catalog."default",
    "Notes_34" character varying (255) COLLATE pg_catalog."default",
    "Notes_35" character varying (255) COLLATE pg_catalog."default",
    "Notes_36" character varying (255) COLLATE pg_catalog."default",
    "Notes_37" character varying (255) COLLATE pg_catalog."default",
    "Notes_38" character varying (255) COLLATE pg_catalog."default",
    "Notes_39" character varying (255) COLLATE pg_catalog."default",
    "Notes_40" character varying (255) COLLATE pg_catalog."default",
    "Notes_41" character varying (255) COLLATE pg_catalog."default",
    "Notes_42" character varying (255) COLLATE pg_catalog."default",
    "Notes_43" character varying (255) COLLATE pg_catalog."default",
    "Notes_44" character varying (255) COLLATE pg_catalog."default",
    "Notes_45" character varying (255) COLLATE pg_catalog."default",
    "Notes_46" character varying (255) COLLATE pg_catalog."default",
    "Notes_47" character varying (255) COLLATE pg_catalog."default",
    "Notes_48" character varying (255) COLLATE pg_catalog."default",
    "Notes_49" character varying (255) COLLATE pg_catalog."default",
    "Notes_50" character varying (255) COLLATE pg_catalog."default",
    "PermitType_01" integer,
    "PermitType_02" integer,
    "PermitType_03" integer,
    "PermitType_04" integer,
    "PermitType_05" integer,
    "PermitType_06" integer,
    "PermitType_07" integer,
    "PermitType_08" integer,
    "PermitType_09" integer,
    "PermitType_10" integer,
    "PermitType_11" integer,
    "PermitType_12" integer,
    "PermitType_13" integer,
    "PermitType_14" integer,
    "PermitType_15" integer,
    "PermitType_16" integer,
    "PermitType_17" integer,
    "PermitType_18" integer,
    "PermitType_19" integer,
    "PermitType_20" integer,
    "PermitType_21" integer,
    "PermitType_22" integer,
    "PermitType_23" integer,
    "PermitType_24" integer,
    "PermitType_25" integer,
    "PermitType_26" integer,
    "PermitType_27" integer,
    "PermitType_28" integer,
    "PermitType_29" integer,
    "PermitType_30" integer,
    "PermitType_31" integer,
    "PermitType_32" integer,
    "PermitType_33" integer,
    "PermitType_34" integer,
    "PermitType_35" integer,
    "PermitType_36" integer,
    "PermitType_37" integer,
    "PermitType_38" integer,
    "PermitType_39" integer,
    "PermitType_40" integer,
    "PermitType_41" integer,
    "PermitType_42" integer,
    "PermitType_43" integer,
    "PermitType_44" integer,
    "PermitType_45" integer,
    "PermitType_46" integer,
    "PermitType_47" integer,
    "PermitType_48" integer,
    "PermitType_49" integer,
    "PermitType_50" integer,
    "RestrictionTypeID_01" integer,
    "RestrictionTypeID_02" integer,
    "RestrictionTypeID_03" integer,
    "RestrictionTypeID_04" integer,
    "RestrictionTypeID_05" integer,
    "RestrictionTypeID_06" integer,
    "RestrictionTypeID_07" integer,
    "RestrictionTypeID_08" integer,
    "RestrictionTypeID_09" integer,
    "RestrictionTypeID_10" integer,
    "RestrictionTypeID_11" integer,
    "RestrictionTypeID_12" integer,
    "RestrictionTypeID_13" integer,
    "RestrictionTypeID_14" integer,
    "RestrictionTypeID_15" integer,
    "RestrictionTypeID_16" integer,
    "RestrictionTypeID_17" integer,
    "RestrictionTypeID_18" integer,
    "RestrictionTypeID_19" integer,
    "RestrictionTypeID_20" integer,
    "RestrictionTypeID_21" integer,
    "RestrictionTypeID_22" integer,
    "RestrictionTypeID_23" integer,
    "RestrictionTypeID_24" integer,
    "RestrictionTypeID_25" integer,
    "RestrictionTypeID_26" integer,
    "RestrictionTypeID_27" integer,
    "RestrictionTypeID_28" integer,
    "RestrictionTypeID_29" integer,
    "RestrictionTypeID_30" integer,
    "RestrictionTypeID_31" integer,
    "RestrictionTypeID_32" integer,
    "RestrictionTypeID_33" integer,
    "RestrictionTypeID_34" integer,
    "RestrictionTypeID_35" integer,
    "RestrictionTypeID_36" integer,
    "RestrictionTypeID_37" integer,
    "RestrictionTypeID_38" integer,
    "RestrictionTypeID_39" integer,
    "RestrictionTypeID_40" integer,
    "RestrictionTypeID_41" integer,
    "RestrictionTypeID_42" integer,
    "RestrictionTypeID_43" integer,
    "RestrictionTypeID_44" integer,
    "RestrictionTypeID_45" integer,
    "RestrictionTypeID_46" integer,
    "RestrictionTypeID_47" integer,
    "RestrictionTypeID_48" integer,
    "RestrictionTypeID_49" integer,
    "RestrictionTypeID_50" integer

    );

ALTER TABLE "demand"."VRM_DemandStem"
    ADD PRIMARY KEY ("id");

ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_GeometryID_fkey" FOREIGN KEY ("GeometryID") REFERENCES "mhtc_operations"."Supply"("GeometryID");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_SectionID_fkey" FOREIGN KEY ("SectionID") REFERENCES "mhtc_operations"."RC_Sections_merged"("gid");

ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_01_fkey" FOREIGN KEY ("VehicleTypeID_01") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_02_fkey" FOREIGN KEY ("VehicleTypeID_02") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_03_fkey" FOREIGN KEY ("VehicleTypeID_03") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_04_fkey" FOREIGN KEY ("VehicleTypeID_04") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_05_fkey" FOREIGN KEY ("VehicleTypeID_05") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_06_fkey" FOREIGN KEY ("VehicleTypeID_06") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_07_fkey" FOREIGN KEY ("VehicleTypeID_07") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_08_fkey" FOREIGN KEY ("VehicleTypeID_08") REFERENCES "demand_lookups"."VehicleTypes"("Code");
ALTER TABLE ONLY "demand"."VRM_DemandStem"
    ADD CONSTRAINT "DemandStem_VehicleTypeID_09_fkey" FOREIGN KEY ("VehicleTypeID_09") REFERENCES "demand_lookups"."VehicleTypes"("Code");
