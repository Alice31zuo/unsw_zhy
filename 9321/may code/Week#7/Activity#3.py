import requests


def print_book(book):
    print("Book {")
    for key in book.keys():
        attr = str(key)
        val = str(book[key])
        print("\t" + attr + ":" + val)

    print("}")


def get_book(id):
    #Send a get request to get the book with id=206 (URL: " http://127.0.0.1:5000/books/206 ")
    r = requests.get("http://127.0.0.1:5000/books/" + str(id))
    book = r.json()
    #
    print("Get status Code:" + str(r.status_code))
    #print the book
    if r.ok:
        print_book(book)
        return book
    else:
        print('Error:' + book['message'])


if __name__ == '__main__':

    print("***** Book information before update *****")
    book = get_book(206)

    # update the book information
    print("***** Updating Book Information *****")
    book['Author'] = 'Nobody'
    #Send a PUT request to update the book
    r = requests.put("http://127.0.0.1:5000/books/206", json=book)
    #Print the status code
    print("Put status Code:" + str(r.status_code))
    #the message returned by the service
    print(r.json()['message'])
#print the returned book to see if the book has been successfully updated
    print("***** Book information after update *****")
    book = get_book(206)