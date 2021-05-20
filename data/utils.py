from json import load as json_load
from requests import get as requests_get
from random import choice, randint

from django.utils.timezone import get_current_timezone

from faker import Faker

from storages import AssetsStorage
from apps.blog.models import CategoryTypes

CURRENT_TZ = get_current_timezone()

FAKE = Faker()


def get_image_url(min_width=500, min_height=500, max_width=None, max_height=None):

    url_list = [
        # 'https://picsum.photos/{}/{}',  # bug
        # 'https://loremflickr.com/{}/{}',  # only cats
        'https://placeimg.com/{}/{}/any',
        ]

    url = choice(url_list)

    if not max_width:
        max_width = 4096
    width = randint(min_width, max_width)

    if not max_height:
        max_height = width
    height = randint(min_height, max_height)

    return url.format(width, height)


def get_image_file_data(min_width=500, min_height=500):

    image_url = get_image_url(min_width=min_width, min_height=min_height)

    response = requests_get(image_url, stream=True)

    return response.content


def get_post_text():

    text = ''

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

    gen_headers = randint(0, 2) in [i for i in range(2)]
    gen_subheaders = gen_headers and randint(0, 5) == 0

    gen_ordered_list = randint(0, 2) == 0
    gen_unordered_list = randint(0, 2) == 0

    gen_image_first = randint(0, 1) == 0
    gen_image_captions = randint(0, 10) == 0
    gen_several_images_in_row = randint(0, 10) == 0

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

        value_with_html_template = ''
        if current_gen_type == 'image':
            value = get_image_url()
            image_tag = html_template_image.format(value)
            if gen_image_captions:
                caption = FAKE.sentence()
                value_with_html_template = html_template_image_align_with_captions.format(image_tag, caption)
            else:
                value_with_html_template = html_template_image_align_without_captions.format(image_tag)
        elif current_gen_type == 'text':
            value = FAKE.text(max_nb_chars=randint(500, 5000))
            value_with_html_template = html_template_text_block.format(value)
            current_header_contains_text = True
        elif current_gen_type == 'header':
            value = FAKE.sentence()
            value_with_html_template = html_template_header.format(value)
            subheader_current_iteration = 0
            current_header_contains_text = False
        elif current_gen_type == 'subheader':
            value = FAKE.sentence()
            subheader_current_iteration += 1
            value_with_html_template = html_template_subheader.format(subheader_current_iteration, value)
            current_header_contains_text = False
        elif current_gen_type == 'ordered_list':
            items_list_str = ''
            for item in range(randint(2, 20)):
                value = FAKE.sentence()
                items_list_str += html_template_list_item.format(value)
            value_with_html_template = html_template_ordered_list.format(items_list_str)
        elif current_gen_type == 'unordered_list':
            items_list_str = ''
            for item in range(randint(2, 20)):
                value = FAKE.sentence()
                items_list_str += html_template_list_item.format(value)
            value_with_html_template = html_template_unordered_list.format(items_list_str)

        text += value_with_html_template
        previous_gen_type = current_gen_type
        i += 1

    return text


def get_tags(category):

    category_name = CategoryTypes.get_name(category)
    assets_storage = AssetsStorage()

    with assets_storage.open('tests/tags.json', 'r') as file:
        data = json_load(file)
        tag_set = data[category_name.lower().replace(' ', '_')]
    i = 0
    length = randint(1, 7)
    tag_list = []
    while i <= length:
        tag_list.append(choice(tag_set))
        i += 1
    return tag_list
