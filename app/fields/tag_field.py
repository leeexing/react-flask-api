from flask_restplus import fields

tag_detail_field = {
    'tag_name': fields.String(example='OST', description='标签名称'),
    'start': fields.Integer(example=0, description='开始查询数'),
    'type': fields.String(example='T', description='排序类型')
}