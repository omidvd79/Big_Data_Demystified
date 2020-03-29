def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):

    try:
        storage_client = storage.Client()

        blobs = storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        dicom_list=[]
        for blob in blobs:
                txt = blob.name       
                if  ".txt" in txt:
                        txt_list.append(txt)
        dist_txt_list = set(txt_list)
    except Exception as inst:
            print type(inst)  # the exception instance
            print inst.args  # arguments stored in .args
            print inst  # __str__ allows args to be printed directly
    return dist_txt_list   

def save_blob_list_in_csv(bucket,list):
  text=""
  for blob in list:
        text=text+"gs://"+bucket+"/"+blob+"\n"
  text_file = open("/tmp/blob_list.csv", "w")
  n = text_file.write(text)
  text_file.close()
