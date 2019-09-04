def validate_keys(obj, keys):
    for key in keys:
        if not obj[key]:
            return jsonify({'result': f'need inform a value for {key}'})
