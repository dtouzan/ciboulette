"""
Constents 
"""

CBL_binning                   = 'binning'
API_version                   = 2000
starshight                    = [5,50,50,40,40,40,30,30,20,20,20,15,15,15,8,8,8,4,4,1,1,1,1,1,1,1,1,1,1,1,1,1]
starslow                      = [5,150,150,100,100,80,80,80,40,40,40,15,15,8,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
RA_J2000                      = 'RA (J2000)' 
DEC_J2000                     = 'DEC (J2000)'

"""
MAST constents 
 Is used for downloaded MAST files    
"""
MAST_header_name              = '#Observation Type, Mission, Instrument, Detector, Project, Filters, Waveband, Target Name, Target Classification, Observation ID, RA, Dec, Proposal ID, Principal Investigator, Product Type, Calibration Level, Start Time, End Time, Exposure Length, Min. Wavelength, Max. Wavelength, Observation Title, Release Date, Proposal Type, Sequence Number, Region,Focale, Format, Seeing, Moon, jpegURL, url'
MAST_header_type              = '#@string,string,string,string,string,string,string,string,string,string,ra,dec,string,string,string,int,float,float,float,string,string,string,float,string,int,string,float,string,float,float,string,string'
MAST_header                   = 'intentType,obs_collection,instrument_name,Detector,project,filters,wavelength_region,target_name,target_classification,obs_id,s_ra,s_dec,proposal_id,proposal_pi,dataproduct_type,calib_level,t_min,t_max,t_exptime,em_min,em_max,obs_title,t_obs_release,proposal_type,sequence_number,s_region,focale,format,Seeing,Moon,jpegURL,url'

MAST_filters                  = 'filters'
MAST_target_name              = 'target_name'
MAST_obs_id                   = 'obs_id'
MAST_s_ra                     = 's_ra'
MAST_s_dec                    = 's_dec'
MAST_t_exptime                = 't_exptime'
MAST_dataproduct_type         = 'dataproduct_type'
MAST_obs_title                = 'obs_title'

