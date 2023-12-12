--
-- Fichier généré par SQLiteStudio v3.4.4 sur mar. déc. 12 11:48:59 2023
--
-- Encodage texte utilisé : System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tableau : Camera
DROP TABLE IF EXISTS Camera;
CREATE TABLE IF NOT EXISTS Camera (ID INTEGER UNIQUE, NAME TEXT (1024), SIZE_X INTEGER DEFAULT (0), SIZE_Y INTEGER DEFAULT (0), SIZE_PIXEL REAL, COLD INTEGER DEFAULT (0));

-- Tableau : Collection
DROP TABLE IF EXISTS Collection;
CREATE TABLE IF NOT EXISTS Collection (NAME TEXT (1024) DEFAULT OT_Library_UT1);

-- Tableau : Database
DROP TABLE IF EXISTS Database;
CREATE TABLE IF NOT EXISTS Database (NAME TEXT (1024), RELEASE TEXT (1024));

-- Tableau : Disperser
DROP TABLE IF EXISTS Disperser;
CREATE TABLE IF NOT EXISTS Disperser (ID INTEGER UNIQUE, NAME TEXT (1024) DEFAULT SA200, LINES INTEGER DEFAULT (200), GRISM INTEGER DEFAULT (0), DIAMETER REAL DEFAULT (25));

-- Tableau : Filter
DROP TABLE IF EXISTS Filter;
CREATE TABLE IF NOT EXISTS Filter (ID INTEGER UNIQUE, NAME TEXT (1024), DATA TEXT (1024), WAVELENGTH_MIN REAL, WAVELENGTH_MAX REAL);

-- Tableau : FilterWheel
DROP TABLE IF EXISTS FilterWheel;
CREATE TABLE IF NOT EXISTS FilterWheel (ID UNIQUE, NAME TEXT (1024), DATA TEXT (1024), SLOTS INTEGER DEFAULT (5), DIAMETER REAL, DATASET TEXT (1024) DEFAULT "L;CLS;Ha;OIII;V");

-- Tableau : Header
DROP TABLE IF EXISTS Header;
CREATE TABLE IF NOT EXISTS Header (NAME TEXT (1024), DATA TEXT (1024), RELEASE TEXT (1024) DEFAULT (1.0));

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

-- Tableau : Observation
DROP TABLE IF EXISTS Observation;
CREATE TABLE IF NOT EXISTS Observation (SCIENCE_PROGRAM_ID INTEGER NOT NULL, OBSERVATION_ID INTEGER NOT NULL, TITLE TEXT (1024), COLLECTION TEXT (1024) NOT NULL, PROPOSAL_PI TEXT (1024), PRIORITY INTEGER, SATUS INTEGER, SCHEDULING TEXT (1024) DEFAULT ('2023-01-01T00:00:00'), FITS_FILE TEXT (1024), NOTE_FILE TEXT (1024), CALIBRATION INTEGER, CONSTRAINT unq_Observation_OBSERVATION_ID UNIQUE (OBSERVATION_ID), FOREIGN KEY (SCIENCE_PROGRAM_ID) REFERENCES ScienceProgram (SCIENCE_PROGRAM_ID));

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

-- Tableau : Sequence
DROP TABLE IF EXISTS Sequence;
CREATE TABLE IF NOT EXISTS Sequence (OBSERVATION_ID INTEGER, TITLE TEXT (1024) DEFAULT 'sequence', LABEL TEXT (1024) DEFAULT "001", TYPE TEXT (1024) DEFAULT 'light', TIMELINE_MIN REAL, TIMELINE_MAX REAL, COMPOMENT TEXT (1024) DEFAULT 'IR-CUT', FOREIGN KEY (OBSERVATION_ID) REFERENCES Observation (OBSERVATION_ID));

-- Tableau : Target
DROP TABLE IF EXISTS Target;
CREATE TABLE IF NOT EXISTS Target (OBSERVATION_ID INTEGER, NAME TEXT (1024), CLASS TEXT (1024), RA REAL, DEC REAL, NOTES TEXT (1024), FOREIGN KEY (OBSERVATION_ID) REFERENCES Observation (OBSERVATION_ID));

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
