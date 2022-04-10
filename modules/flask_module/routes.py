name_id = '/<int:name_id>'

routes = dict({
    "general": '/',
    "slct_rm_gen": '/slct_rm_gen',
    "exclude": '/exclude_name' + name_id,
})