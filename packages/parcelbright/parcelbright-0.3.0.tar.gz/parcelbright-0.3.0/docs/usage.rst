========
Usage
========

To use ParcelBrigh API wrapper in a project::

    >>> import parcelbright
    >>> parcelbright.api_key = 'myapikey'
    >>> parcelbright.sandbox = True  # use sandbox version

    >>> # Create Parcel
    >>> parcel = parcelbright.Parcel({
    ...     'width': 10, 'height': 10, 'length': 10, 'weight': 1
    ... })

    >>> # Create from Address
    >>> from_address = parcelbright.Address({
    ...     'name': 'office', 'postcode': 'NW1 0DU', 'town': 'London',
    ...     'phone': '07800000000', 'country_code': 'GB',
    ...     'line1': '19 Mandela Street'
    ... })

    >>> # Create to Address
    >>> to_address = parcelbright.Address({
    ...     'name': 'John Doe', 'postcode': 'E2 8RS', 'town': 'London',
    ...     'phone': '07411111111', 'country_code': 'GB',
    ...     'line1': '19 Mandela Street'
    ... })

    >>> # Create shipment
    >>>    shipment = parcelbright.Shipment({
    ...     'customer_reference': '123455667', 'estimated_value': 100,
    ...     'contents': 'books', 'pickup_date': '2025-01-29',
    ...     'parcel': parcel, 'from_address': from_address,
    ...     'to_address': to_address
    ... })
    >>>  print shipment.id
    None

    # Call API to create
    >>> shipment.create()
    >>> print shipment.id

    >>> print shipment.rates

    >>> # Find previously created shipment
    >>> shipment = parcelbright.Shipment.find('prb6c8c0')

    >>> # Book created or found shipment using rates code
    >>> shipment.book(rate_code='N')

    >>> print shipment.label_url
    >>> print shipment.consignment
    >>> print shipment.pickup_confirmation

    >>> # Get tracking data
    >>> tracking = shipment.track()
    >>> print tracking

    >>> # Cancell shipment
    >>> shipment.cancel()
