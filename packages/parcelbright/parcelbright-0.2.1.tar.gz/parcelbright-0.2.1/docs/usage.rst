========
Usage
========

To use ParcelBrigh API wrapper in a project::

    import parcelbright

    parcelbright.api_key = 'myapikey'
    parcelbright.sandbox = True  # use sandbox version

    # Create entities
    parcel = parcelbright.parcel(
        width=10, height=10, length=10, weight=1
    )
    from_address = parcelbright.Address(
        name="office", postcode="NW1 0DU",
        town="London", phone="07800000000",
        line1="19 Mandela Street",
        country_code="GB"
    )
    to_address = parcelbright.Address(
        name="John Doe", postcode="E2 8RS",
        town="London", phone="07411111111",
        line1="19 Mandela Street",
        country_code="GB"
    )

    # Call API to create shipment and get rates
    shipment = parcelbright.Shipment.create(
        customer_reference='123455667', estimated_value=100,
        contents='books', pickup_date='2025-01-29',
        parcel=parcel, from_address=from_address,
        to_address=to_address
    )
    print shipment.rates

    # Find previously created shipment
    shipment = parcelbright.Shipment.find('prb6c8c0')

    # Book created or found shipment
    shipment.book(rate_code='N')

    print shipment.label
    print shipment.consignment
    print shipment.confirmation_number

    # Get tracking data
    tracking = shipment.track()
    print tracking

    # Cancell shipment
    shipment.cancel()
