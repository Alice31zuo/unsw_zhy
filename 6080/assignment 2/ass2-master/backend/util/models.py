from app import api
from flask_restplus import fields

comment_details = api.model('comment_details',{
    "author": fields.String(example="Becky"),
    "published": fields.String(example="1539476785.0"),
    "comment": fields.String(example="Cute Photo!")
})

new_comment_details = api.model('new_comment_details',{
    "comment": fields.String(example="Cute Photo!")
})

token_details = api.model('token_details',{
    'token': fields.String()
})

post_id_details = api.model('post_id_details',{
    "post_id": fields.String()
})

post_meta_details = api.model('post_meta_details',{
    "author": fields.String(),
    "description_text": fields.String(),
    "published": fields.String(),
    "likes": fields.List(fields.Integer())
})

post_details = api.model('post_details',{
  "id": fields.Integer(),
  "meta": fields.Nested(post_meta_details),
  "thumbnail": fields.String(),
  "src": fields.String(),
  "comments": fields.List(fields.Nested(comment_details))
})

new_post_details = api.model('new_post_details',{
  "description_text": fields.String(required=True, example='i had a fun time!'),
  "src": fields.String(required=True, example='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')
})

post_list_details = api.model('post_list_details',{
    "posts" : fields.List(fields.Nested(post_details))
})

login_details = api.model('login_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})

user_details = api.model('user_details', {
    'id': fields.Integer(min=0),
    'username': fields.String(example='xX_greginator_Xx'),
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'posts': fields.List(fields.Integer(min=0)),
    'following': fields.List(fields.Integer(min=0)),
    'followed_num': fields.Integer(min=0)
})
user_update_details = api.model('user_update_details', {
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'password': fields.String(example='1234')
})
signup_details = api.model('signup_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'name':  fields.String(required=True, example='greg')
})

auth_details = api.parser().add_argument('Authorization', help="Your Authorization Token in the form 'Token <AUTH_TOKEN>'",location='headers')
