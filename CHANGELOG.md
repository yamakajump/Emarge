# Changelog

## [v2.3] - 2025-03-05

### Added
- Random user agent on linux
- Request the API to emarge at 7h
- Can only emarge between 8h and 18h

### Changed
- Switch to BeautifulSoup

### Fixed
- Wierd bug on the reset part
- Fixed TimeZone filtering on API

## [v2.2] - 2025-02-26

### Added
- Blacklist used from the environment variables

### Changed
- Emerge from 15-25 min

### Fixed
- Fix emerge keep past event

## [v2.1] - 2025-02-24

### Added
- Integration with PlanningSup API for automatic schedule fetching
- Event filtering logic for special activities
- Random attendance check-in delays (5-15 minutes)
- Daily schedule refresh at midnight
- Changelog file
- FORMATION variable

### Changed
- Moved from static to dynamic scheduling
- Optimized API calls by checking weekdays first
- Removed CourseID and AttendanceID specification
- Removed SEMESTRE specification
- Sort list of time to emarge

### Fixed
- Resolved Selenium timing issues with additional delays
- Resolved schedule timing issues
- Corrected timezone discrepancies in schedule fetching
- Adjusted some timing with wooden connection like eduroam

## [v2.0] - 2024-12-15

### Added
- Docker containerization support
- Environment variable configuration in the docker-compose
- Weekend detection
- Colored console output

### Changed
- Automated browser interactions

### Fixed
- Browser compatibility issues
- Location of log files
- Support for Windows, Mac and VPS 

## [v1.0] - 2024-10-01

### Added
- Initial release
- Manual attendance tracking
- Basic web interface interaction
- Command-line interface
- Crontab possibility
- .env file