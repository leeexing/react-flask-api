from flask_restplus import fields

# *用于显示返回数据是什么格式
topic_res_field = {

}

# *获取更多主题的参数
topic_more_field = {
    'start': fields.Integer(example=8, min=8, description='The topic query start number'),
    'limit': fields.Integer(required=True, example=16, min=16, description='最少16，且是8的倍数'),
}