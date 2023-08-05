# Change Log
All changes to 'hpelm' toolbox will be documented in this file.

## [0.6.13] - 18-08-2015
### Fixed
- Fixed a bug (typo) which caused HPELM to skip the last batch of data in training/predicting/etc.

## [0.6.14] - 19-08-2015
### New
- Added asyncronous HDF5 file reading in HPELM.predict(). The program must be able to spawn a separate process.

## [0.6.15] - 19-08-2015
### Fixed
- Asyncronous HDF5 file reading now enabled by "async" flag in HPELM initialization. On Windows, make sure you use 'if __name__ == "__main__"' construction in your main code, or async reader will not start.
