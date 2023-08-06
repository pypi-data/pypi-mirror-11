********
Redfearn
********

Based on the `Geocentric Datum of Australia - Technical Manual Version 2.3 Amendment 1
<www.icsm.gov.au/gda/gdatm/gdav2.3.pdf>`_

A web based application of this tool is available at `plaintech.net.au <https://plaintech.net.au/redfearn>`_.

Tested in Python 2.7+ and Python 3.3+

Example Usage:

.. code:: python

    latitude_dms = redfearn.DMS(-37, 39, 10.15611)
    # result: DMS(degrees=-37, minutes=39, seconds=10.15611)

    longitude_dms = redfearn.DMS(143, 55, 35.38393)
    # result: DMS(degrees=143, minutes=55, seconds=35.38393)

    latitude_dd = redfearn.dms2decdeg(latitude_dms)
    # result: -37.652821141666664

    longitude_dd = redfearn.dms2decdeg(longitude_dms)
    # result: 143.9264955361111

    grid_coordinates = redfearn.latlon2grid(latitude_dd, longitude_dd, coordinate_system='GDA-MGA')
    # result:   {
    #                'easting': 758173.798005752,
    #                'northing': 5828674.339728091,
    #                'zone': 54,
    #                'grid_convergence': 1.7887112307424733,
    #                'point_scale_factor': 1.0004210730644858
    #            }

    easting = 758173.798
    northing = 5828674.340
    zone = 54

    lat_long = redfearn.grid2latlon(easting, northing, zone, coordinate_system='GDA-MGA')
    # result:   {
    #                'latitude': -37.65282114013244,
    #                'longitude': 143.92649553599782,
    #                'point_scale_factor': 1.0004210730517988,
    #                'grid_convergence': 1.7887112306027275
    #            }

A test suite is included, however further test data is only available for the 'GDA-MGA' coordinate system at this stage.

If you know of valid test data in other coordinate systems please let me know.