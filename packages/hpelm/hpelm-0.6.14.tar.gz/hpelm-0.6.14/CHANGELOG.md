# Change Log
All changes to 'hpelm' toolbox will be documented in this file.

## [0.6.13] - 18-08-2015
### Fixed
- Fixed a bug (typo) which caused HPELM to skip the last batch of data in training/predicting/etc.

## [0.6.14] - 19-08-2015
### New
- Added asyncronous HDF5 file reading in HPELM.predict(). The program must be able to spawn a separate process.
