    try:
        storage_client = storage.Client()
    except Exception as inst:
            print type(inst)  # the exception instance
            print inst.args  # arguments stored in .args
            print inst  # __str__ allows args to be printed directly
