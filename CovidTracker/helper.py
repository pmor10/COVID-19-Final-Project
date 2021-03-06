def format_data(d, key):
    """Formats database data to in dict format
    
    Parameters:
    -----------
    d: crud query results

    key: string
        values: ('test_id', 'vaccine_id')

    Returns:
        dict
        Returns a dict() of the query results from the testing or vaccine data.
    
    """
    # Checks to see if the key passed in matches the primary key from the
    # VaccineLocation or TestingLocation model.
    # assert key in ['test_id', 'vaccine_id', 'symptom_id'], "Please use the correct attribute."

    # This will hold our data from the crud query.
    data = {}

    # row is the query object that is returned from crud.
    # d is the query results that come in as a list of query objects.
    for row in d:
        # r is a temporary variable that will hold the attributes for each test_id/vaccine_id
        # For example, r will store the {'address': '1725 S Bascom'} for each key value pair
        # found in the object. This connects back to the repr that is defined in the model.py
        r = {}

        # Here we use dir to return all the attributes associated with the object row (query object).
        for attribute in dir(row):

            # Here is a list of attributes that we would like to ignore.
            if not (
                    attribute.startswith('__') or attribute.startswith('_') or \
                    attribute.startswith('query') or attribute.startswith('metadata') or \
                    attribute.startswith(key)
                    ):

                # For all other attributes we want to add them to our `r` dictionary. 
                # We use the getattr builtin function to return the value for an attribute from a given object.
                # This is similar to using row.attribute dot access. For example, if you wanted to get the address
                # from a query object you would access it with testing_info.address but instead we format like this
                # getattr(testing_info, 'address')

                r[attribute] = getattr(row, attribute)

                # Printing the attributes to make sure we are not bringing in anything we don't want.
                
        # Lastly, we want to tie each r dict(), that stores our data, to the test_id/vaccine_id found in our `key` parameter.

        data[getattr(row, key)] = r
    # Return the dict data to the app.
    return data 