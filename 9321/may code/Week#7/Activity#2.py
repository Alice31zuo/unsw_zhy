import requests


if __name__=='__main__':

    #Create a python dictionary with the expected keys and custom values
    book={"Date_of_Publication": 2018,
        "Publisher": "UNSW",
        "Author": "Nobody",
        "Title": "Nothing",
        "Flickr_URL": "http://somewhere",
        "Identifier": 2,
        "Place_of_Publication": "Sydney"}
    #end a POST request (URL: " http://127.0.0.1:5000/books ")
    r=requests.post("http://127.0.0.1:5000/books",json=book)
    # #Print the status code
    print("Status_code:"+str(r.status_code))
    resp=r.json()
    #Print the message returned by the service
    print (resp['message'])

