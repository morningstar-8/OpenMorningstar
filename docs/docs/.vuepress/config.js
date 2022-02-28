module.exports = {
  lang: 'zh-CN',
  title: '晨星文档',
  description: '这是OpenMorningstar的官方文档',
  themeConfig: {
    logo: 'https://vuejs.org/images/logo.png',
    sidebar: [
      {
        text: '概述',
        link: '/'
      },
      {
        text: '快速开始',
        link: '/guide/',
        children: [
          { text: '安装', link: '/guide/install.html' },
          { text: '测试', link: '/guide/test.html' },
        ]
      },
      {
        text: '学无止尽',
        link: '/learn/',
        children: [
          { text: 'Git', link: '/learn/git.html' },
          { text: 'CSS', link: '/learn/css.html' },
          { text: 'Sass', link: '/learn/sass.html' },
          { text: 'Bootstrap', link: '/learn/bootstrap.html' },
          { text: 'JavaScript', link: '/learn/javascript.html' },
          { text: 'Django', link: '/learn/django.html' },
        ]
      }

    ],
  },
}
