import os
import pathlib
import random
import sys
from datetime import timedelta

import faker
import django


# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname  # 文件夹名称
BASE_DIR = back(back(back(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


def clean_database():
    # blog
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()
    # poll
    Question.objects.all().delete()
    Choice.objects.all().delete()
    # user
    User.objects.all().delete()


def create_user():
    user = User.objects.create_superuser(
        'admin', 'admin@morningstar529.com', 'admin')
    User.objects.create_user(
        'staff', 'staff@morningstar529.com', 'staff', is_staff=True)
    User.objects.create_user('guest', 'guest@morningstar529.com', 'guest')
    return user


def create_blog(user):
    """ 创建分类和标签 """
    print('create categories and tags')
    category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    tag_list = ['django', 'Python', 'Virtualenv', 'Docker', 'Nginx',
                'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
    a_year_ago = timezone.now() - timedelta(days=365)
    for cate in category_list:
        Category.objects.create(name=cate)
    for tag in tag_list:
        Tag.objects.create(name=tag)

    """ 创建博文 """
    print('create a markdown sample post')
    Post.objects.create(
        title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath(
            'scripts', 'fake', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
    )
    print('create some faked posts published within the past year')
    # 一百篇英文
    fake = faker.Faker()
    for _ in range(100):
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created = fake.date_time_between(start_date='-1y', end_date="now",
                                         tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created=created,
            category=cate,
        )
        post.tags.add(tag1, tag2)
        post.save()
    # 一百篇中文
    fake = faker.Faker('zh_CN')
    for _ in range(100):  # Chinese
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created = fake.date_time_between(start_date='-1y', end_date="now",
                                         tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created=created,
            category=cate,
        )
        post.tags.add(tag1, tag2)
        post.save()

    """ 添加评论 """
    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created = post.created
        delta_in_days = '-' + \
            str((timezone.now() - post_created).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                body=fake.paragraph(),
                created=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "Morningstar.settings.dev")
    django.setup()
    from blog.models import Category, Post, Tag, Comment
    from poll.models import Question, Choice
    from django.utils import timezone
    from Morningstar.models import User

    """ 清除旧数据 """
    print('clean database')
    clean_database()

    """ 创建超管 """
    print('create a user')
    superuser = create_user()

    """ 创建博客数据 """
    print('create a blog user')
    create_blog(user=superuser)

    print('done!')
