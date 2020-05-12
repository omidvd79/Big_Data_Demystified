def save_to_file(data):
        start_date='1970-01-01'
        path="/tmp/myFile_"+start_date+".txt"
        text_file = open(path, "w")
        n = text_file.write(json_data)
        text_file.close()
        print("file saved: "+path)
