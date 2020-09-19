def extract_recipe_info(recipe):
    recipe = recipe['_source']
    image_1_1 = recipe['images'][0]['ratios'][4]['stack'].replace('{stack}', 'medium')
    image_16_9 = recipe['images'][0]['ratios'][1]['stack'].replace('{stack}', 'medium')
    size = recipe['available_sizes'][0]
    if size != 2:
        factor = size / 2
        for i, ingredient in enumerate(recipe['sizes'][0]['ingredient_blocks'][0]['ingredients']):
            recipe['sizes'][0]['ingredient_blocks'][0]['ingredients'][i]['amount']['quantity'] = \
                recipe['sizes'][0]['ingredient_blocks'][0]['ingredients'][i]['amount']['quantity'] / factor
    return {
        'id': recipe['id'],
        'title': recipe['title'],
        'teasertext': recipe['teasertext'],
        'duration': recipe['duration_total_in_minutes'],
        'steps': recipe['steps'],
        'nutrients': recipe['nutrients'],
        'ingredients': recipe['sizes'][0]['ingredient_blocks'][0]['ingredients'],
        'images': {'1:1': image_1_1, '16:9': image_16_9}
    }
