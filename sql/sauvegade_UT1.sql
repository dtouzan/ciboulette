--
-- Fichier généré par SQLiteStudio v3.4.4 sur mar. déc. 12 11:49:13 2023
--
-- Encodage texte utilisé : System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tableau : Camera
DROP TABLE IF EXISTS Camera;
CREATE TABLE IF NOT EXISTS Camera (ID INTEGER UNIQUE, NAME TEXT (1024), SIZE_X INTEGER DEFAULT (0), SIZE_Y INTEGER DEFAULT (0), SIZE_PIXEL REAL, COLD INTEGER DEFAULT (0));
INSERT INTO Camera (ID, NAME, SIZE_X, SIZE_Y, SIZE_PIXEL, COLD) VALUES (0, 'Atik 383L+', 3354, 2529, 5.4, 1);
INSERT INTO Camera (ID, NAME, SIZE_X, SIZE_Y, SIZE_PIXEL, COLD) VALUES (1, 'ZWO ASI 120Mini', 1280, 960, 3.75, 0);
INSERT INTO Camera (ID, NAME, SIZE_X, SIZE_Y, SIZE_PIXEL, COLD) VALUES (2, 'QHY5-M', 1280, 1024, 5.2, 0);

-- Tableau : Collection
DROP TABLE IF EXISTS Collection;
CREATE TABLE IF NOT EXISTS Collection (NAME TEXT (1024) DEFAULT OT_Library_UT1);
INSERT INTO Collection (NAME) VALUES ('OT_Library_UT1');
INSERT INTO Collection (NAME) VALUES ('OT_Library_HII');
INSERT INTO Collection (NAME) VALUES ('OT_Library_OIII');
INSERT INTO Collection (NAME) VALUES ('OT_Library_GALAXY');
INSERT INTO Collection (NAME) VALUES ('OT_Library_CLUSTER');
INSERT INTO Collection (NAME) VALUES ('OT_Library_VARIABLE');
INSERT INTO Collection (NAME) VALUES ('OT_Library_SUPERNOVA');
INSERT INTO Collection (NAME) VALUES ('OT_Library_ASTEROID');

-- Tableau : Database
DROP TABLE IF EXISTS Database;
CREATE TABLE IF NOT EXISTS Database (NAME TEXT (1024), RELEASE TEXT (1024));
INSERT INTO Database (NAME, RELEASE) VALUES ('UT1', '1.0.0');

-- Tableau : Disperser
DROP TABLE IF EXISTS Disperser;
CREATE TABLE IF NOT EXISTS Disperser (ID INTEGER UNIQUE, NAME TEXT (1024) DEFAULT SA200, LINES INTEGER DEFAULT (200), GRISM INTEGER DEFAULT (0), DIAMETER REAL DEFAULT (25));
INSERT INTO Disperser (ID, NAME, LINES, GRISM, DIAMETER) VALUES (1, 'Grism SA200', 200, 4, 25.0);
INSERT INTO Disperser (ID, NAME, LINES, GRISM, DIAMETER) VALUES (0, 'SA200', 200, 0, 25.0);

-- Tableau : Filter
DROP TABLE IF EXISTS Filter;
CREATE TABLE IF NOT EXISTS Filter (ID INTEGER UNIQUE, NAME TEXT (1024), DATA TEXT (1024), WAVELENGTH_MIN REAL, WAVELENGTH_MAX REAL);
INSERT INTO Filter (ID, NAME, DATA, WAVELENGTH_MIN, WAVELENGTH_MAX) VALUES (0, 'IR-CUT', 'UV/IR-Cut;L0;3800,4000,6850,7000;0,0.9,0.9,0', 380.0, 700.0);

-- Tableau : FilterWheel
DROP TABLE IF EXISTS FilterWheel;
CREATE TABLE IF NOT EXISTS FilterWheel (ID UNIQUE, NAME TEXT (1024), DATA TEXT (1024), SLOTS INTEGER DEFAULT (5), DIAMETER REAL, DATASET TEXT (1024) DEFAULT "L;CLS;Ha;OIII;V");
INSERT INTO FilterWheel (ID, NAME, DATA, SLOTS, DIAMETER, DATASET) VALUES (0, 'Atik EFW2', 'L;CLS;Ha35nm;OIII;V;g'';r'';SA200;Nome', 9, 31.75, 'L;CLS;Ha;OIII;V');
INSERT INTO FilterWheel (ID, NAME, DATA, SLOTS, DIAMETER, DATASET) VALUES (1, 'ZWO ASI EFWMini', 'None1;None2;None3;SA200;Grism SA200', 5, 31.75, 'L;CLS;Ha;OIII;V');

-- Tableau : Header
DROP TABLE IF EXISTS Header;
CREATE TABLE IF NOT EXISTS Header (NAME TEXT (1024), DATA TEXT (1024), RELEASE TEXT (1024) DEFAULT (1.0));
INSERT INTO Header (NAME, DATA, RELEASE) VALUES ('filter', 'name;label;spectral_axis;flux', '1.0.0');
INSERT INTO Header (NAME, DATA, RELEASE) VALUES ('mast', 'intentType;obs_collection;instrument_name;filters;disperser;target_name;target_classification;obs_id;s_ra;s_dec;proposal_pi;dataproduct_type;calib_level;scheduling;t_min;t_max;t_exptime;obs_title;focal;format;url', '1.0.0');

-- Tableau : Instrument
DROP TABLE IF EXISTS Instrument;
CREATE TABLE IF NOT EXISTS Instrument ( 
	OBSERVATION_ID       INTEGER     ,
	NAME                 TEXT(1024)     ,
	FILTER               TEXT(1024)     ,
	DISPERSER            TEXT(1024)     ,
	CAMERA               TEXT(1024)     ,
	EXPOSURE_TIME        REAL     ,
	POSITION_ANGLE       REAL     ,
	BINNING_X            INTEGER     ,
	BINNING_Y            INTEGER     ,
	GAIN                 INTEGER     ,
	FOREIGN KEY ( OBSERVATION_ID ) REFERENCES Observation( OBSERVATION_ID )  
 );
INSERT INTO Instrument (OBSERVATION_ID, NAME, FILTER, DISPERSER, CAMERA, EXPOSURE_TIME, POSITION_ANGLE, BINNING_X, BINNING_Y, GAIN) VALUES (1, 'UT1', 'IR-CUT', NULL, '0.75', 300.0, 0.0, 2, 2, 0);
INSERT INTO Instrument (OBSERVATION_ID, NAME, FILTER, DISPERSER, CAMERA, EXPOSURE_TIME, POSITION_ANGLE, BINNING_X, BINNING_Y, GAIN) VALUES (2, 'UT1', 'IR-CUT', '', '0.2', 900.0, NULL, NULL, NULL, NULL);

-- Tableau : Observation
DROP TABLE IF EXISTS Observation;
CREATE TABLE IF NOT EXISTS Observation (SCIENCE_PROGRAM_ID INTEGER NOT NULL, OBSERVATION_ID INTEGER NOT NULL, TITLE TEXT (1024), COLLECTION TEXT (1024) NOT NULL, PROPOSAL_PI TEXT (1024), PRIORITY INTEGER, SATUS INTEGER, SCHEDULING TEXT (1024) DEFAULT ('2023-01-01T00:00:00'), FITS_FILE TEXT (1024), NOTE_FILE TEXT (1024), CALIBRATION INTEGER, CONSTRAINT unq_Observation_OBSERVATION_ID UNIQUE (OBSERVATION_ID), FOREIGN KEY (SCIENCE_PROGRAM_ID) REFERENCES ScienceProgram (SCIENCE_PROGRAM_ID));
INSERT INTO Observation (SCIENCE_PROGRAM_ID, OBSERVATION_ID, TITLE, COLLECTION, PROPOSAL_PI, PRIORITY, SATUS, SCHEDULING, FITS_FILE, NOTE_FILE, CALIBRATION) VALUES (1000, 1, 'HII in galaxy', 'OT_Library_UT1', 'dtouzan@gmail.com', NULL, NULL, '2019-05-31T23:36:00', 'ngc5350-20190531-2336-1x300-f750.fits', 'fits', 1);
INSERT INTO Observation (SCIENCE_PROGRAM_ID, OBSERVATION_ID, TITLE, COLLECTION, PROPOSAL_PI, PRIORITY, SATUS, SCHEDULING, FITS_FILE, NOTE_FILE, CALIBRATION) VALUES (1000, 2, '', 'OT_Library_UT1', 'dtouzan@gmail.com', NULL, NULL, '2017-04-23T21:20:00', '9-20170423-2120-15x60s-f200.fits', 'fits', 1);

-- Tableau : ObservingConditions
DROP TABLE IF EXISTS ObservingConditions;
CREATE TABLE IF NOT EXISTS ObservingConditions ( 
	OBSERVATION_ID       INTEGER     ,
	SKY_BACKGROUND       INTEGER  DEFAULT (50)   ,
	CLOUD_COVER          INTEGER  DEFAULT (0)   ,
	IMAGE_QUALITY        INTEGER  DEFAULT (50)   ,
	WATER_VAPOR          INTEGER  DEFAULT (50)   ,
	ELEVATION_CONSTRAINT INTEGER  DEFAULT (0)   ,
	TIMMING_WINDOW       TEXT(1024)     ,
	FOREIGN KEY ( OBSERVATION_ID ) REFERENCES Observation( OBSERVATION_ID )  
 );

-- Tableau : ObservingLog
DROP TABLE IF EXISTS ObservingLog;
CREATE TABLE IF NOT EXISTS ObservingLog ( 
	OBSERVATION_ID       INTEGER     ,
	LABEL                TEXT(1024)     ,
	FILENAME             TEXT(1024)     ,
	COMMENT              TEXT(1024)     ,
	FOREIGN KEY ( OBSERVATION_ID ) REFERENCES Observation( OBSERVATION_ID )  
 );

-- Tableau : ScienceProgram
DROP TABLE IF EXISTS ScienceProgram;
CREATE TABLE IF NOT EXISTS ScienceProgram (SCIENCE_PROGRAM_ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, TITLE TEXT (1024), STATUS INTEGER DEFAULT (1), CONTACT TEXT (1024) DEFAULT "dtouzan@gmail.com", OBSERVING_TIME REAL, TYPE TEXT (1024) DEFAULT science, DATASET TEXT (1024) DEFAULT dataset);
INSERT INTO ScienceProgram (SCIENCE_PROGRAM_ID, TITLE, STATUS, CONTACT, OBSERVING_TIME, TYPE, DATASET) VALUES (1000, 'UT1 science program 2016-2023', 0, 'dtouzan@gmail.com', 0.0, 'science', 'dataset/archives');
INSERT INTO ScienceProgram (SCIENCE_PROGRAM_ID, TITLE, STATUS, CONTACT, OBSERVING_TIME, TYPE, DATASET) VALUES (1001, 'UT1 science program 2024', 1, 'dtouzan@gmail.com', 0.0, 'science', 'dataset/archives');

-- Tableau : Sequence
DROP TABLE IF EXISTS Sequence;
CREATE TABLE IF NOT EXISTS Sequence (OBSERVATION_ID INTEGER, TITLE TEXT (1024) DEFAULT 'sequence', LABEL TEXT (1024) DEFAULT "001", TYPE TEXT (1024) DEFAULT 'light', TIMELINE_MIN REAL, TIMELINE_MAX REAL, COMPOMENT TEXT (1024) DEFAULT 'IR-CUT', FOREIGN KEY (OBSERVATION_ID) REFERENCES Observation (OBSERVATION_ID));
INSERT INTO Sequence (OBSERVATION_ID, TITLE, LABEL, TYPE, TIMELINE_MIN, TIMELINE_MAX, COMPOMENT) VALUES (1, 'sequence', '001', 'light', 58634.98333333333, 58634.98680555555, 'IR-CUT');
INSERT INTO Sequence (OBSERVATION_ID, TITLE, LABEL, TYPE, TIMELINE_MIN, TIMELINE_MAX, COMPOMENT) VALUES (2, 'sequence', '001', 'light', 57866.88888888889, 57866.899305555555, 'IR-CUT');

-- Tableau : Target
DROP TABLE IF EXISTS Target;
CREATE TABLE IF NOT EXISTS Target (OBSERVATION_ID INTEGER, NAME TEXT (1024), CLASS TEXT (1024), RA REAL, DEC REAL, NOTES TEXT (1024), FOREIGN KEY (OBSERVATION_ID) REFERENCES Observation (OBSERVATION_ID));
INSERT INTO Target (OBSERVATION_ID, NAME, CLASS, RA, DEC, NOTES) VALUES (1, 'ngc5350', 'GinPair', 208.34009666666668, 40.36394055555556, '');
INSERT INTO Target (OBSERVATION_ID, NAME, CLASS, RA, DEC, NOTES) VALUES (2, '9', 'Asteroid', 152.27041666666665, 19.17416666666667, NULL);

-- Vue : collection_select
DROP VIEW IF EXISTS collection_select;
CREATE VIEW IF NOT EXISTS collection_select AS SELECT * FROM collection;

-- Vue : filter_header
DROP VIEW IF EXISTS filter_header;
CREATE VIEW IF NOT EXISTS filter_header AS SELECT data FROM header WHERE name='filter';

-- Vue : instrument_mast_values
DROP VIEW IF EXISTS instrument_mast_values;
CREATE VIEW IF NOT EXISTS instrument_mast_values AS SELECT name,filter,disperser,exposure_time,camera FROM instrument;

-- Vue : mast_header
DROP VIEW IF EXISTS mast_header;
CREATE VIEW IF NOT EXISTS mast_header AS SELECT data FROM header WHERE name='mast';

-- Vue : mast_select
DROP VIEW IF EXISTS mast_select;
CREATE VIEW IF NOT EXISTS mast_select AS SELECT ScienceProgram.type, collection, instrument.name, filter, disperser, target.name, class, Observation.observation_id, ra, dec, proposal_pi, Sequence.type, calibration, scheduling, timeline_min, timeline_max, exposure_time, Observation.title, instrument.camera, note_file, fits_file FROM ScienceProgram , Observation , instrument , target , Sequence WHERE Observation.science_program_id = ScienceProgram.science_program_id AND Observation.observation_id = instrument.observation_id AND Observation.observation_id = Sequence.observation_id AND Observation.observation_id = target.observation_id;

-- Vue : observation_last_id
DROP VIEW IF EXISTS observation_last_id;
CREATE VIEW IF NOT EXISTS observation_last_id AS SELECT * FROM Observation ORDER BY observation_id DESC LIMIT 1;

-- Vue : observation_mast_values
DROP VIEW IF EXISTS observation_mast_values;
CREATE VIEW IF NOT EXISTS observation_mast_values AS SELECT collection, observation_id, proposal_pi, calibration, scheduling, title, note_file, fits_file FROM Observation;

-- Vue : scienceprogram_mast_values
DROP VIEW IF EXISTS scienceprogram_mast_values;
CREATE VIEW IF NOT EXISTS scienceprogram_mast_values AS SELECT type FROM ScienceProgram;

-- Vue : scienceprogram_select
DROP VIEW IF EXISTS scienceprogram_select;
CREATE VIEW IF NOT EXISTS scienceprogram_select AS SELECT science_program_id, title, contact, observing_time, type, dataset FROM ScienceProgram;

-- Vue : sequence_mast_values
DROP VIEW IF EXISTS sequence_mast_values;
CREATE VIEW IF NOT EXISTS sequence_mast_values AS SELECT type, timeline_min, timeline_max FROM Sequence;

-- Vue : target_mast_values
DROP VIEW IF EXISTS target_mast_values;
CREATE VIEW IF NOT EXISTS target_mast_values AS SELECT name,class,ra,dec FROM target;

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
