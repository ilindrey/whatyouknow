import json

from random import randint, choice

from whatyouknow.blog.models import CATEGORY_CHOICES

from mimesis.providers.text import Text

prov = Text()


def get_category():
    int_value_list_categories = [x[0] for x in CATEGORY_CHOICES]
    return choice(int_value_list_categories)


def get_image_url(min_width=500, min_height=250, max_width=None, max_height=None):

    url_list = [
        'https://picsum.photos/{}/{}',
        ]

    url = choice(url_list)

    if not max_width:
        max_width = 4096
    width = randint(min_width, max_width)

    if not max_height:
        max_height = width
    height = randint(min_height, max_height)

    return url.format(width, height)


def get_post_params():

    text = ''
    feed_cover = None
    # feed_cover_caption = None
    # feed_article_preview = None
    # feed_read_more_button_name = None

    html_template_text_block = '<p>{}<br></p>'

    html_template_header = '<h3>{}<br></h3>'
    html_template_subheader = '<h4>{}. {}<br></h4>'

    html_template_list_item = '<li>{}</li>'
    html_template_ordered_list = '<ol>{}</ol>'
    html_template_unordered_list = '<ul>{}</ul>'

    html_template_image = '<img style="width: 100%;" src="{}">'
    html_template_image_align_without_captions = '<p align="center">{}<br></p>'
    html_template_image_align_with_captions = """
                    <div align="center">
                        <figure class="">
                            {}
                        <figcaption class=""><i>{}</i></figcaption>
                        </figure>
                    </div>
                    """

    read_more_button_name_list = [
        'Read more...',
        'Continue',
        'Continue...',
        'Click to view',
        'Click to view...',
        'Click to continue',
        'Click to continue...',
        'With this post we start a series of articles, click to continue',
        ]

    gen_headers = randint(0, 2) in [i for i in range(2)]
    gen_subheaders = gen_headers and randint(0, 5) == 0

    gen_ordered_list = randint(0, 2) == 0
    gen_unordered_list = randint(0, 2) == 0

    gen_image_first = randint(0, 1) == 0
    gen_image_captions = randint(0, 10) == 0
    gen_several_images_in_row = randint(0, 10) == 0

    # gen_feed_cover = randint(0, 10) == 0 if gen_image_first else randint(0, 100) == 0
    # gen_feed_article_preview = randint(0, 10) == 0 if gen_feed_cover else randint(0, 100) == 0
    gen_feed_cover = 1
    gen_feed_article_preview = 1

    gen_feed_read_more_button_name = randint(0, 100) == 0

    generation_list = [
        'image',
        'text',
        ]

    if gen_headers:
        generation_list += ['header', ]
    if gen_subheaders:
        generation_list += ['subheader', ]
    if gen_ordered_list:
        generation_list += ['ordered_list', ]
    if gen_unordered_list:
        generation_list += ['unordered_list', ]

    i = 0
    length = randint(10, 50)
    previous_gen_type = ''
    subheader_current_iteration = 0
    current_header_contains_text = False
    feed_article_preview_value = ''
    feed_article_preview_html_template = ''
    max_length_feed_article_preview = randint(500, 2000)
    while i < length:

        if i == 0 and gen_image_first:
            current_gen_type = 'image'
        elif i == length - 1:
            current_gen_type = 'text'
            previous_gen_type = ''
        elif i + 3 >= length and subheader_current_iteration == 1 and previous_gen_type == 'text':
            current_gen_type = 'subheader'
            previous_gen_type = ''
            generation_list.remove('subheader')
        else:
            current_gen_type = choice(generation_list)

        if i == 1 and gen_image_first and current_gen_type == 'image':
            continue

        if current_gen_type == previous_gen_type and not (current_gen_type == 'image' and gen_several_images_in_row):
            continue

        if current_gen_type == 'image' and previous_gen_type in ('ordered_list', 'unordered_list'):
            continue

        if current_gen_type in ('header', 'subheader') and not current_header_contains_text:
            continue

        if current_gen_type in ('header', 'subheader') and previous_gen_type == 'image':
            continue

        if current_gen_type == 'header' and subheader_current_iteration == 1:
            continue

        if current_gen_type in ('ordered_list', 'unordered_list') and previous_gen_type != 'text':
            continue

        caption = None
        value = ''
        value_with_html_template = ''
        if current_gen_type == 'image':
            if not gen_feed_cover and (i == 0 and current_gen_type == 'image'):
                value = get_image_url(410, 250, 1200, 250)
            else:
                value = get_image_url()
            image_tag = html_template_image.format(value)
            if gen_image_captions:
                caption = prov.title()
                value_with_html_template = html_template_image_align_with_captions.format(image_tag, caption)
            else:
                value_with_html_template = html_template_image_align_without_captions.format(image_tag)
        elif current_gen_type == 'text':
            value = prov.text(quantity=randint(3, 50))
            value_with_html_template = html_template_text_block.format(value)
            current_header_contains_text = True
        elif current_gen_type == 'header':
            value = prov.title()
            value_with_html_template = html_template_header.format(value)
            subheader_current_iteration = 0
            current_header_contains_text = False
        elif current_gen_type == 'subheader':
            value = prov.title()
            subheader_current_iteration += 1
            value_with_html_template = html_template_subheader.format(subheader_current_iteration, value)
            current_header_contains_text = False
        elif current_gen_type == 'ordered_list':
            items_list_str = ''
            for item in range(randint(2, 20)):
                value = prov.title()
                items_list_str += html_template_list_item.format(value)
            value_with_html_template = html_template_ordered_list.format(items_list_str)
        elif current_gen_type == 'unordered_list':
            items_list_str = ''
            for item in range(randint(2, 20)):
                value = prov.title()
                items_list_str += html_template_list_item.format(value)
            value_with_html_template = html_template_unordered_list.format(items_list_str)

        if not gen_feed_cover and (i == 0 and current_gen_type == 'image'):
            feed_cover = value
            # if gen_image_captions:
            #     feed_cover_caption = caption
        elif not gen_feed_article_preview and len(feed_article_preview_value) <= max_length_feed_article_preview:
            feed_article_preview_value += value
            feed_article_preview_html_template += value_with_html_template

        text += value_with_html_template
        previous_gen_type = current_gen_type
        i += 1

    if gen_feed_cover:
        feed_cover = get_image_url(410, 250, 1200, 250)
        # if gen_image_captions:
        #     feed_cover_caption = prov.title()

    if gen_feed_article_preview:
        value = ''
        while 0 <= len(value) <= max_length_feed_article_preview:
            value = prov.text(quantity=randint(3, 50))
        feed_article_preview = html_template_text_block.format(value)
    else:
        feed_article_preview = feed_article_preview_html_template

    if gen_feed_read_more_button_name:
        feed_read_more_button_name = choice(read_more_button_name_list)
    else:
        feed_read_more_button_name = 'Read more'

    return {
        'text': text,
        'feed_cover': feed_cover,
        # 'feed_cover_caption': feed_cover_caption,
        'feed_article_preview': feed_article_preview,
        'feed_read_more_button_name': feed_read_more_button_name
        }


def get_tags(index_category):

    category = CATEGORY_CHOICES[index_category][1]

    with open('./tests/tags.json', 'r') as file:
        data = json.load(file)
        tag_set = data[category]
    i = 0
    length = randint(1, 7)
    tag_list = []
    while i <= length:
        tag_list.append(choice(tag_set))
        i += 1
    return tag_list
