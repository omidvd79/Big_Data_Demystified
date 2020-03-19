import getopt
import sys

from google.cloud import storage

usage="""script.py --bucket gs://myBucket \n or \n
        script.py --bucket gs://myBucket --prefix a \n or \n
        script.py --bucket gs://myBucket --prefix a --delimiter /
      """
help =  """Lists all the blobs in the bucket that begin with the prefix.

    This can be used to list all blobs in a "folder", e.g. "public/".

    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:

        a/1.txt
        a/b/2.txt

    If you just specify prefix = 'a', you'll get back:

        a/1.txt
        a/b/2.txt

    However, if you specify prefix='a' and delimiter='/', you'll get back:

        a/1.txt

    Additionally, the same request will return blobs.prefixes populated with:

        a/b/
    """
def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):

    try:
        storage_client = storage.Client()

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        print("Blobs:")
        for blob in blobs:
            print(blob.name)

        if delimiter:
            print("Prefixes:")
            for prefix in blobs.prefixes:
                print(prefix)

    except Exception as inst:
            print type(inst)  # the exception instance
            print inst.args  # arguments stored in .args
            print inst  # __str__ allows args to be printed directly


def validate_bucket(arg):
    if ("gs://" in arg):
        print ("Bucket name should not contain prefix : gs://")
        sys.exit(1)
    else:
        return arg


def parse_argv(argv):
    bucket = ''
    prefix = ''
    delimeter =''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["bucket=" ,"prefix=","delimeter="])
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (help)
            sys.exit(0)
        elif opt in ("--bucket"):
            bucket=validate_bucket(arg)
        elif opt in ("--prefix"):
            prefix=arg
        elif opt in ("--delimeter"):
            delimeter=arg

    return bucket,prefix,delimeter

def main(argv):
    bucket,prefix,delimeter=parse_argv(argv)
    list_blobs_with_prefix(bucket,prefix,delimeter)

if __name__ == "__main__":
    #print "This is the name of the script: ", sys.argv[0]
    #print "Number of arguments: ", len(sys.argv)
    #print "The arguments are: ", str(sys.argv)

    #validate 2 arguments, the first is filename_arg+ 3X(kel,val)  = 7
    if(len(sys.argv)==7 or len(sys.argv)==5 or len(sys.argv)==3):
        main(sys.argv[1:])
    else:
        print "Error in arguments, try : "+(usage)
        sys.exit(1)
