import requests
# this function to Convert the content of the response object to a python dictionary
def print_book(book):
    print("Book {")
    for key in book.keys():
        attr=str(key)
        val=str(book[key])
        print("\t" + attr + ":" + val)
    print("}")




if __name__=='__main__':
#Send a GET request (URL: " http://127.0.0.1:5000/books ") and get the books ordered by 'Date_of_Publication' in an ascending order
    r=requests.get("http://127.0.0.1:5000/books",params={'order':'Date_of_Publication','ascending':True})
#Print the status code (HTTP response code) of response object
    print("Status codes:"+str(r.status_code))
#put the dataset in json format
    books=r.json()
#Print top 5 books
    for i in range(1,5):
       print_book(books[i])

