.. :changelog:

History
-------

0.3.2 (2015-08-14)
------------------

* Added shipment.track to schema

0.3.1 (2015-08-07)
------------------

* Added missing `schematics` requirements at `setup.py`

0.3.0 (2015-08-07)
------------------

* API CHANGED - Entities constructor takes `dict` instead of `kwargs`
* API CHANGED - `Shipment.create` becames instance method instead of class method
* Added entities validation using `schematics` package

0.2.3 (2015-07-29)
---------------------

* Support for `pickup_date` parameter at `Shipment.book()` method
* Added `__repr__` method to `Parcel`, `Address` and `Shipment` entities

0.2.2 (2015-07-29)
---------------------

* Raise `TrackingError` from `Shipment.track()` if shipment has not tracking
  information available

0.2.1 (2015-07-29)
---------------------

* Remove `Shipment.is_booked()` method. Use `Shipment.state` instead.
* Raise `ShipmentNotCompletedException` from `Shipment.track()` method

0.2.0 (2015-07-28)
---------------------

* Added support to track and cancel shipments

0.1.0 (2015-07-27)
---------------------

* First release on PyPI.
