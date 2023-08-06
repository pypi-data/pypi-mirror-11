*******************************
Australian NTv2 Grid Conversion
*******************************

The Australian NTv2 Grid Conversion module and command line script enables conversions between AGD66/AGD84 and GDA94 coordinates using national grid files.
It is intended as a partial replacement of the `GDAit transformation software <http://www.dtpli.vic.gov.au/property-and-land-titles/geodesy/geocentric-datum-of-australia-1994-gda94/gda94-useful-tools>`_ provided by The Office of Surveyor-General Victoria.
National grid files obtained from the `ANZLIC Committee on Surveying & Mapping <http://www.icsm.gov.au/gda/tech.html>`_ are bundled with this application.

Tested in Python 3.4 and Python 2.7

This module is available on `pypi <https://pypi.python.org/pypi/australian_ntv2_grid_conversion>`_ or via *pip install australian-ntv2-grid-conversion*.

`Redfearn's formula <https://bitbucket.org/plaintech/redfearn>`_ in the pypi module `redfearn <https://pypi.python.org/pypi/redfearn>`_ is used to convert between lat/lon and grid coordinate systems.

A web based application of this software is available at `plaintech.net.au <https://plaintech.net.au/australian_ntv2_grid_conversion>`_.

Compiled exe files for command line use on Windows are available (`Win 32bit <https://sydney-downloads.s3.amazonaws.com/PlainTech/australian_ntv2_grid_conversion/v1.1.4/australian_ntv2_grid_conversion_v1.1.4_win_32bit.zip>`_ | `Win 64bit <https://sydney-downloads.s3.amazonaws.com/PlainTech/australian_ntv2_grid_conversion/v1.1.4/australian_ntv2_grid_conversion_v1.1.4_win_64bit.zip>`_)
These are compiled with `py2exe <http://www.py2exe.org/>`_, all files within the zip archive must remain in the same folder.

This module will read and convert csv files of data points.
The csv file should have a single header row of either 'latitude, longitude' or 'easting, northing, zone'.
Latitude and longitude values should be in decimal degrees.

Example Module Usage:

.. code:: python

    from australian_ntv2_grid_conversion import australian_ntv2_grid_conversion
    ntv2 = australian_ntv2_grid_conversion.ntv2()

    # Convert from lat/lon to lat/lon
    # usage: latlon_to_latlon(latitude, longitude, from_system, to_system)
    ntv2.latlon_to_latlon(-27.4667, 153.0333, 'agd84', 'gda94')
    ntv2.latlon_to_latlon(-27.465103686137034, 153.0343661751207, 'gda94', 'agd66')
    ntv2.latlon_to_latlon(-27.46668817104357, 153.0333048970482, 'agd66', 'gda94')
    ntv2.latlon_to_latlon(-27.465103686137034, 153.0343661751207, 'gda94', 'agd84')
    # results:
    # {'lat_trans_acc': 0.0037210114794467347, 'lon_trans_acc': 0.0021168627299100505, 'latitude': -27.465103686137034, 'longitude': 153.0343661751207}
    # {'lat_trans_acc': 0.004446575182746488, 'lon_trans_acc': 0.0039787268242746695, 'latitude': -27.46668817104357, 'longitude': 153.0333048970482}
    # {'lat_trans_acc': 0.004446575182746488, 'lon_trans_acc': 0.0039787268242746695, 'latitude': -27.465103686137034, 'longitude': 153.0343661751207}
    # {'lat_trans_acc': 0.0037210114794467347, 'lon_trans_acc': 0.0021168627299100505, 'latitude': -27.4667, 'longitude': 153.0333}

    # Other conversions
    # usage: latlon_to_grid(latitude, longitude, from_system, to_system)
    # usage: grid_to_grid(easting, northing, zone, from_system, to_system)
    # usage: grid_to_latlon(easting, northing, zone, from_system, to_system)
    ntv2.latlon_to_grid(-27.4667, 153.0333, 'agd84', 'gda94')
    ntv2.grid_to_grid(503395.5069452213, 6962048.068551116, 56, 'gda94', 'agd66')
    ntv2.grid_to_grid(503290.6135552996, 6961862.07437364, 56, 'agd66', 'gda94')
    ntv2.grid_to_grid(503395.50694522355, 6962048.068518826, 56, 'gda94', 'agd84')
    ntv2.grid_to_latlon(503290.129362482, 6961860.764213287, 56, 'agd84', 'agd84')
    # results:
    # {'zone': 56, 'northing': 6962048.068551116, 'lat_trans_acc': 0.0037210114794467347, 'lon_trans_acc': 0.0021168627299100505, 'easting': 503395.5069452213}
    # {'zone': 56, 'northing': 6961862.07437364, 'lat_trans_acc': 0.004446575198236321, 'lon_trans_acc': 0.003978726821685475, 'easting': 503290.6135552996}
    # {'zone': 56, 'northing': 6962048.068518826, 'lat_trans_acc': 0.004446575213734464, 'lon_trans_acc': 0.003978726819093661, 'easting': 503395.50694522355}
    # {'zone': 56, 'northing': 6961860.764213287, 'lat_trans_acc': 0.0037210114810668823, 'lon_trans_acc': 0.002116862746774709, 'easting': 503290.1293624824}
    # {'lat_trans_acc': 0, 'lon_trans_acc': 0, 'latitude': -27.466700000583025, 'longitude': 153.0333000000002}

    # Convert csv files
    # usage: ntv2.convert_csv_file(from_system, to_system, input_file_path, output_file_path=None, output_format='', suppress_accuracy=False)
    #           output_file_path    : Defaults to [input_file_name]_[to_system].csv
    #           output_format       : Default is same as input
    #           suppress_accuracy   : Set True to not print the accuracy values
    #       returns True if output file written successfully
    # any data that cannot be calculated is written as '***'. Some coordinates will not be able to be converted as they may be invalid data, or fall outside the grid file area.

Command line usage is very similar

.. code:: python

    # usage: australian_ntv2_grid_conversion.py --help
    # usage: australian_ntv2_grid_conversion.py [input_type] [from_system] [to_system] {-variable_parameters}

    Three positional arguments are required

    positional arguments:
        INPUT_TYPE
        {grid,latlon,file}      The type of conversion required where
                                grid   = Grid coordinate - Must provide EASTING, NORTHING and ZONE
                                latlon = Latitude and Longitude - Must provide LATITUDE and LONGITUDE in decimal degrees
                                file   = Convert all coordinates in input file - Must provide INPUT_FILE
        FROM_SYSTEM
        {agd66,agd84,gda94}     The coordinate system you wish to convert FROM
        TO_SYSTEM
        {agd66,agd84,gda94}     The coordinate system you wish to convert TO

    optional arguments:
        -h, --help              show this help message and exit
        -latitude LATITUDE, -a LATITUDE
                                Latitude in decimal degrees format e.g. -37.8136
        -longitude LONGITUDE, -o LONGITUDE
                                Longitude in decimal degrees format e.g. 144.9631
        -easting EASTING, -e EASTING
                                Easting in decimal format e.g. 320704.446
        -northing NORTHING, -n NORTHING
                                Northing in decimal format e.g. 5812911.7
        -zone ZONE, -z ZONE     Zone (integer)
        -input_file INPUT_FILE, -f INPUT_FILE
                                Full path to input file
        -output_file OUTPUT_FILE, -g OUTPUT_FILE
                                Full path to output file (defaults to [INPUT_FILE]_[TO_SYSTEM].csv
        -output_format {grid,latlon}, -p {grid,latlon}
                                Defaults to the same as the input format
        --suppress_accuracy     Conversion accuracies are not printed (default FALSE)
        -ntv2_file NTV2_FILE    Full path to ntv2 data file to use (instead of
                                defaults)