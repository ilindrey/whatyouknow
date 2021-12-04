
from json import load as json_load
from requests import get as requests_get
from random import choice, randint, randrange
from io import BytesIO

from django.conf import settings
from django.utils.timezone import get_current_timezone
from django.core.files.images import ImageFile

from faker import Faker
from django_summernote.models import Attachment

from apps.blog.models import CategoryTypes


CUR_TZ = get_current_timezone()
FAKER = Faker()


def get_image_url(min_width=500, min_height=500, max_width=None, max_height=None):

    url_list = [
        # 'https://picsum.photos/{}/{}',  # bug
        # 'https://loremflickr.com/{}/{}/all',
        # 'https://placeimg.com/{}/{}/any',
        'https://source.unsplash.com/random/{}x{}/'
    ]

    url = choice(url_list)

    if not max_width:
        max_width = 4096
    width = randint(min_width, max_width)

    if not max_height:
        max_height = width
    height = randint(min_height, max_height)

    return url.format(width, height)


def get_image(min_width=500, min_height=500, max_width=None, max_height=None):
    image_url = get_image_url(min_width, min_height, max_width, max_height=max_height)
    i = 0
    response = None
    while i < 5 and (response is None or not response.ok):
        try:
            response = requests_get(image_url, stream=True)
        except Exception as e:
            print(f'Image file load failed: {e}')
        i += 1
    try:
        return response.url, response.content
    except:
        return '', None


def get_image_data(min_width=500, min_height=500, max_width=None, max_height=None):
    return get_image(min_width, min_height, max_width, max_height)[1]


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

    gen_headers = randrange(2) == 0
    gen_subheaders = gen_headers and randrange(10) == 0

    gen_ordered_list = randrange(10) == 0
    gen_unordered_list = randrange(10) == 0

    gen_image_first = randrange(1) == 0
    gen_image_captions = randrange(10) == 0
    gen_several_images_in_row = randrange(10) == 0

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

    previous_gen_type = ''
    subheader_current_iteration = 0
    current_header_contains_text = False

    length = randint(10, 50)
    for i in range(length):

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
        match current_gen_type:
            case 'image':
                url, data = get_image(max_width=2048)
                if not url and not data:
                    continue
                gen_image_as_file = data and randrange(10) > 5
                if gen_image_as_file:
                    try:
                        img_file = ImageFile(BytesIO(data), name=f'text_{randint(1000000, 9999999)}.jpg')
                        img = Attachment._default_manager.create(file=img_file)
                        value = img.file.url
                    except:
                        value = url
                        gen_image_as_file = False
                else:
                    value = url
                image_tag = html_template_image.format(value)
                if gen_image_captions:
                    caption = FAKER.sentence()
                    value_with_html_template = html_template_image_align_with_captions.format(image_tag, caption)
                else:
                    value_with_html_template = html_template_image_align_without_captions.format(image_tag)
            case 'text':
                value = FAKER.text(max_nb_chars=randint(500, 5000))
                value_with_html_template = html_template_text_block.format(value)
                current_header_contains_text = True
            case 'header':
                value = FAKER.sentence()
                value_with_html_template = html_template_header.format(value)
                subheader_current_iteration = 0
                current_header_contains_text = False
            case 'subheader':
                value = FAKER.sentence()
                subheader_current_iteration += 1
                value_with_html_template = html_template_subheader.format(
                    subheader_current_iteration, value)
                current_header_contains_text = False
            case 'ordered_list':
                items_list_str = ''
                for j in range(randint(2, 20)):
                    value = FAKER.sentence()
                    items_list_str += html_template_list_item.format(value)
                value_with_html_template = html_template_ordered_list.format(items_list_str)
            case 'unordered_list':
                items_list_str = ''
                for j in range(randint(2, 20)):
                    value = FAKER.sentence()
                    items_list_str += html_template_list_item.format(value)
                value_with_html_template = html_template_unordered_list.format(items_list_str)

        text += value_with_html_template
        previous_gen_type = current_gen_type

    return text


def get_tags(index_category):

    category_name = CategoryTypes.get_value(index_category, 'index')['full_name']

    with open(settings.BASE_DIR / 'data_gen/assets/tags.json', 'r') as file:
        data = json_load(file)
        tag_set = data[category_name.lower().replace(' ', '_')]

    tag_list = []
    length = randint(1, 7)
    for i in range(length):
        tag_list.append(choice(tag_set))

    return tag_list
