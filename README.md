Univision
=========

Example API for showing relationships between shows, producers, and movie clips

## Installation

git clone https://github.com/mwcollins/Univision.git

### Requirements

	* Python 2.7
	* MySql

### Setup Required Python Libs
```
pip install MySQL-python
pip install pyquery
```

### Setup Database
```
cd Univision
./setup.sh
```
Note: This command will drop any database called 'univision'

## Test Api

Test parsing of thrones.xml file
```
python test-parse-xml.py
```

Test printing of show text representation
```
python test-print-show.py
```

Test printing of show xml representation
```
python test-print-xml.py
```

Test printing of producers text representation
```
python test-print-producers.py
```

Test printing of clips text representation
```
python test-print-clips.py
```

Test sum of total clip durations
```
python test-clip-duration.py
```

