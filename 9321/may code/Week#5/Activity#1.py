import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields

app=Flask(__name__)
api=Api(app)



Book_model=api.model('book',{'Place_of_Publication':fields.String, 'Date_of_Publication':fields.String,
                             'Publisher':fields.String, 'Title':fields.String,
       'Author':fields.String, 'Flickr_URL':fields.String,'Identifier':fields.Integer})




@api.route('/book/<int:id>')
class books(Resource):
    def get(self,id):
        if id not in df.index:
            api.abort(400,"Book {} doesnt exist".format(id))
        book=dict(df.loc[id])
        return book


    def delete(self,id):
        if id not in df.index:
            api.abort(400, "Book {} doesnt exist".format(id))
        df.drop(id,inplace=True)
        return {"message":"Book {} is removed".format(id)},200




    @api.expect(Book_model)

    def put(self,id):
        if id not in df.index:
            api.abort(400, "Book {} doesnt exist".format(id))
        book=request.json

        for key in book:
            if key not in Book_model.keys():
                return {"message": "property {} is invalid ".format(key)}, 400
            df.loc[id,key]=book[key]
        return {"message": "Book {} is updated ".format(id)}, 200





if __name__ == '__main__':
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    # drop unnecessary columns
    df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date

    # replace spaces in the name of columns
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # set the index column; this will help us to find books with their ids
    df.set_index('Identifier', inplace=True)

    # run the application
    app.run(debug=True)




