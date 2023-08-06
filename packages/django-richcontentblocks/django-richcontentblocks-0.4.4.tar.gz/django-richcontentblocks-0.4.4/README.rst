=====
django-richcontentblocks
=====

Very simple CMS-like content blocks for use in a django project.  

Features:

1. Admin interface for creating/managing content blocks (including a rich text editor)

2. Template tag for retrieving/displaying content block in a django project template. Django cache is leveraged, when possible, in loading content block.

Inspiration and more full featured version: django-tinycontent_

Installation
------------
Run: ``pip install django-richcontentblocks``

Quick start
-----------
1. Follow configuration instructions for ckeditor_ (skip this step if ckeditor is already configured).

2. Run migrations:: 

    manage.py migrate

3. Add "richcontent" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'richcontentblocks',
    )

You should now have an admin tool with the ability to create rich content blocks.

Usage in template
------------------
An example of loading a rich content block, with a key value of ``my-block`` in a template::

    {% load rich_content_block_tags %}
    <div>
        the content block will be in next div
    </div>
    <div>
        {% rich_content_block 'my-block' %}
    </div>

The first time a content block loads, it will be placed in cache. Subsequent loads of the content block will use the cached item.

If an invalid content block key is used to when attempting to load a content object, an error message is displayed.


.. _ckeditor: https://github.com/django-ckeditor/django-ckeditor
.. _django-tinycontent: https://github.com/dominicrodger/django-tinycontent