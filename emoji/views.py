import os
import urllib
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageSequence
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from .models import AsciiEmoji, Tag, EmojiSeries, SeriesElement
from .models import User
from .myForms import RegisterForm, LoginForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def validate(request):
    if request.method == 'GET':
        form = LoginForm(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            psd = form.cleaned_data['password']
            user = authenticate(username=user, password=psd)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return render(request, 'index.html', {
                        'user': user
                    })
                else:
                    return HttpResponse("用户不可用")
            else:
                return HttpResponse("用户未验证")
        else:
            return HttpResponse("表单无效")


def register(request):
    registerForm = RegisterForm()
    return render(request, 'register.html', {
        'registerForm': registerForm
    })


def createUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            psd = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=user, password=psd, email=email)
            user.save()
            return render(request, 'index.html', {
                'user': user
            })
        else:
            return HttpResponse('not validate')
    else:
        print('not post')


def login(request):
    form = LoginForm()
    return render(request, 'login.html', {
        'form': form
    })


def search(request):
    keyword = request.GET['content']
    if keyword:
        emoji_list = []
        mode = request.GET['search-type']
        # 连接到阿里云主机上的es进行查询
        es = Elasticsearch(hosts=["120.77.148.37"])
        # 指定index和doc_type
        search = Search(using=es, index='emoji', doc_type='emojis')
        # 关键字匹配,并返回所有结果
        if mode == 'all':
            res = search.query('match', type=keyword).execute()
            res = search.query('match', type=keyword)[0:res.hits.total].execute()
        elif mode == 'static':
            res = search.query('match', type=keyword).exclude('term', filetype='gif').execute()
            res = search.query('match', type=keyword).exclude('term', filetype='gif')[0:res.hits.total].execute()
        elif mode == 'gif':
            res = search.query('match', type=keyword).query('match', filetype='gif').execute()
            res = search.query('match', type=keyword).query('match', filetype='gif')[0:res.hits.total].execute()

        # 把查询结果以字典的形式返回，并提取出需要的数据
        dict = res.to_dict()['hits']['hits']
        # 将提取的数据添加到emoji_list
        for item in dict:
            emoji_list.append(item['_source']['path'])

        return render(request, 'result.html',
                      {'keyword': keyword, 'emoji_list': emoji_list})
    else:
        # 返回主页并提示没有输入任何关键字
        return render(request, 'index.html',
                      {'error_message': "你还没输入任何关键字呢  ╮(╯▽╰)╭"})


# 返回数据库中类似的关键词，生成下拉提示框
def ajax(request):
    result = []
    es = Elasticsearch(hosts=["120.77.148.37"])
    # 指定index和doc_type
    search = Search(using=es, index='emoji', doc_type='emojis')
    # 关键字匹配,并返回至多100个结果
    res = search.query('match', type=request.GET['data']).execute()
    # 把查询结果以字典的形式返回，并提取出需要的数据
    dict = res.to_dict()['hits']['hits']
    # 将提取的数据添加到emoji_list
    for item in dict:
        result.append(item['_source']['type'])

    data = {
        'result': list(set(result))
    }
    return JsonResponse(data)


def asciiAjax(request):
    result = Tag.objects.filter(name__icontains=request.GET['data']).values_list('name')
    data = {
        'result': list(result)
    }
    return JsonResponse(data)


def asciiEmoji(request, page):
    # 返回数据库里的前30个标签
    tag_per_page = 30
    tag_list = get_list_or_404(Tag)
    pages = range(int(len(tag_list) / tag_per_page))
    return render(request, 'asciiEmoji.html', {
        'tag_list': tag_list[page * tag_per_page:(page + 1) * tag_per_page],
        'pages': pages,
    })


def asciiEmojiSearch(request):
    keyword = request.GET['content']
    if keyword:
        tag = get_object_or_404(Tag, name=keyword)
        if tag.emojis.count() >= 1:
            tag.hits += 1
            tag.save()
            ascii_list = get_list_or_404(AsciiEmoji, tag=tag)
            return render(request, 'asciiEmoji.html', {
                'keyword': keyword,
                'list': ascii_list
            })
        else:
            tag_per_page = 30
            tag_list = get_list_or_404(Tag)
            pages = range(int(len(tag_list) / tag_per_page))
            return render(request, 'asciiEmoji.html', {
                'error_message': '没有这种颜文字喔，试试其他吧  (*ﾟーﾟ)',
                'tag_list': tag_list[:tag_per_page],
                'pages': pages,
            })
    else:
        return render(request, 'asciiEmoji.html', {
            'error_message': '你还没输入任何关键字呢  ╮(╯▽╰)╭'
        })


# 获取某一页的表情系列
def emojiSet(reqeust, page):
    page_list = get_list_or_404(EmojiSeries)
    series_per_page = 5
    emoji_per_series = 5
    series_list = page_list[page * series_per_page: page * series_per_page + series_per_page]
    # 获取该系列的前5个表情
    for series in series_list:
        series.elements = get_list_or_404(SeriesElement, series=series)[:emoji_per_series]
    if page > 5:
        # 确定底部的页面导航栏共有几页
        if page < int(len(page_list) / series_per_page) - 4:
            pages = list(range(page - 4, page + 4))
        else:
            pages = list(range(page - 8, page))

        pages.insert(0, 0)
        pages.append(int(len(page_list) / series_per_page))
    else:
        pages = list(range(9))
    return render(reqeust, 'EmojiSet.html', {
        'series_list': series_list,
        'pages': pages
    })

# 获取一个套图所有的图片
def detail(request, series_name):
    series = get_object_or_404(EmojiSeries, name=series_name)
    emojis = get_list_or_404(SeriesElement, series=series)
    return render(request, 'series-detail.html', {
        'name': series.name,
        'emojis': emojis,
    })


@login_required()
def templates(request, page):
    template_dir = '../Crawler/Crawler/datas/material'
    template_list = os.listdir(template_dir)
    row = 4
    column = 6
    max_page = int(len(template_list) / (row * column))
    template_list = template_list[page * row * column:(page + 1) * row * column]
    if page < 5:
        pages = list(range(8))
        pages.append(max_page)

    elif page <= max_page - 5:
        pages = list(range(page - 5, page + 5))
        pages.insert(0, 0)
        pages.append(max_page)
    else:
        pages = list(range(page - 5, max_page))
        pages.insert(0, 0)
    # pages = range(int(len(template_list) / (row * column)))
    return render(request, 'templates.html', {
        'list': template_list,
        'pages': pages
    })


@login_required()
def diy(request, img):
    colors = ['red', 'blue', 'purple', 'yellow', 'black', 'orange']
    fonts = ['msyh', 'STCAIYUN', 'FZSTK', 'STHUPO', 'simsunb']
    return render(request, 'diy.html', {
        'img': img,
        'colors': colors,
        'fonts': fonts
    })


def add_text_to_image(image, text, font, color='black'):
    rgba_image = image.convert('RGBA')
    # 生成白底的图片
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = ((rgba_image.size[0] - text_size_x) / 2, rgba_image.size[1] - text_size_y - 50)
    # 设置文本的颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=color)
    # 合成
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text


def add_text_to_gif(file, image, text, font, color='black', email='None'):
    frames = []
    # Loop over each frame in the animated image
    for frame in ImageSequence.Iterator(image):
        # 在每一帧上都添加文字
        d = ImageDraw.Draw(frame)
        # 解决中文乱码问题
        d.ink = 0 + 255 * 256 + 0 * 255 * 256

        x_size, y_size = image.size
        text_size_x, text_size_y = d.textsize(text, font=font)
        text_xy = ((x_size - text_size_x) / 2, y_size - text_size_y - 50)
        d.text(text_xy, text=text, font=font, fill=10)

        del d

        # 以bytesio来保存图片，比以文件保存更高效
        b = BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)

    # 将所有帧组合成一个gif
    if email == "None":
        stream = BytesIO()
        frames[0].save(stream, 'GIF', save_all=True, append_images=frames[1:])
        return stream.getvalue()
    else:
        dir = '../Crawler/Crawler/datas/userEmojis'
        if not os.path.exists('%s/%s' % (dir, email)):
            os.makedirs('%s/%s' % (dir, email))
        path = '%s/%s/%s' % (dir, email, file)
        frames[0].save(path, save_all=True, append_images=frames[1:])


# 将数据传递到新的html页面，新页面的img发请求生成
@login_required()
def submitData(request):
    if request.method == 'GET':
        material = urllib.parse.unquote(request.GET['material'])[29:]
        text = request.GET['text']
        font_size = request.GET['font-size'][:-2]
        color = request.GET['color']
        font = request.GET['font']

        return render(request, 'newEmoji.html', {
            'name': material[:-4],
            'material': material,
            'text': text,
            'font_size': font_size,
            'color': color,
            'font': font,
            'file': material
        })
    else:
        print("not get")


def process_template(request, material, text, font_size, color, font, email):
    if request.method == 'GET':
        font_dir = 'C:\Windows\Fonts'
        font_path = font_dir + '/' + font + '.ttf'
        if not os.path.exists(font_path):
            font_path = font_dir + '/' + font + '.ttc'
        # 浏览器的字体大小和图像的字体大小不一致，需要放缩
        defaultFont = ImageFont.truetype(font_path, int(int(font_size) * 2))
        dir = "../Crawler/Crawler/datas/material"
        if material[-3:] == 'gif':
            if email != "None":
                add_text_to_gif(material, Image.open(dir + "/" + material), text, defaultFont, color, email)
                return HttpResponse("保存成功")
            else:
                img = add_text_to_gif(material, Image.open(dir + "/" + material), text, defaultFont, color, "None")
                return HttpResponse(img, content_type='image/gif')

        else:
            img = add_text_to_image(Image.open(dir + "/" + material), text, defaultFont, color)
            if email != "None":
                dir = '../../GraduationProject/Crawler/Crawler/datas/userEmojis'
                if not os.path.exists('%s/%s' % (dir, email)):
                    os.makedirs('%s/%s' % (dir, email))
                path = '%s/%s/%s' % (dir, email, material.replace("jpg", "png"))
                img.save(path)
                return HttpResponse("保存成功")
            else:
                stream = BytesIO()
                img.save(stream, 'PNG')
                return HttpResponse(stream.getvalue(), content_type="image/png")
