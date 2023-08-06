===============================================================================================
Dangler - A Python script to expand hamlet templates file (Html without closing tags) into html 
===============================================================================================

The problem -
=============

Writing HTML can be a pain if you are doing it by hand. Things can be considerable improved if
you can write Html in python style, using indentation instead closing tags to delimit blocks
This is something that is shamelessly copied from Haskell's hamlet templates.

How to use -
============

::

 <!DOCTYPE html>
 <html>
    <body>
        <div>
            Here is some content
            
will be expanded to

::

   <!DOCTYPE html>
   <html>
       <body>
           <div>
               Here is some content
           </div>
       </body>
   </html>

A special case -
================

Suppose you want to create this html structure

::

    <html>
        <body>
            <div>
                Here is some content
                <span>
                    content inside span
                </span>
                More content
            </div>
        </body>
    </html>

If you attempt to make this using Dangler,

::

   <html>
        <body>
            <div>
                Here is some content
                <span>
                    content inside span
                more content

This will not work. The last line, 'more content' will 
not get added to the content inside the span. Instead it will
get added to the parent div because it's indentation matches the 
child elements of the div rather than the span. To add content that does not care about
indentation, put a line with """ only. This will start the 'gather mode'
Which gathers all lines that follow until another """, all by itself in a line
The indentation for the content collected in the gather mode, is taken from the
very first line after the first """ is seen. So for our example, we can do something
like this

::

   <html>
        <body>
            <div>
                Here is some content
                <span>
                """
                    content inside span
                more content
                """

If you want to have a line with """ only, just escape it with a backslash.

Using with other template systems -
===================================

Dangler does not do Html parsing. It just arranges the contents of a text file
into a set of nested blocks. Things like closing the tags is done by extensions
that process these nested blocks. Right now, Dangler has two extensions enabled
by default that will work for Html and for Jinja2 files.

If you run Dangler on this text,


::

  <html>
    <body>
        <div>
            Here is some content
            <span>
                content inside span
            more content
            {% if something %}
                <div>
                    do this
            {% elif %}
                <div>
                    do that
                {% if otherthing %}
                    <span>
                        so and so
                    {% set a = f %}
                    {% if not something %}
                        {% set nav %}
                            <div>
                                something here
                        {% for a = b %}
                            <div>
                                <div>
                                    do a
                    {% elif other thing%}
                        <table>
                            <tr>
                                <td>
                                    do other thing
                    {% elif other someting %}
                        <p>
                            dont do anything!
                {% else %}
                    <span>
                        get something from user
                    <input type="text"/>
            {% else %}
                <p>
                    do something even nicer!



It will be expanded to

::

  <html>
    <body>
        <div>
            Here is some content
            <span>
                content inside span
            </span>
            more content
            {% if something %}
                <div>
                    do this
                </div>
            {% elif %}
                <div>
                    do that
                </div>
                {% if otherthing %}
                    <span>
                        so and so
                    </span>
                    {% set a = f %}
                    {% if not something %}
                        {% set nav %}
                            <div>
                                something here
                            </div>
                        {% endset %}
                        {% for a = b %}
                            <div>
                                <div>
                                    do a
                                </div>
                            </div>
                        {% endfor %}
                    {% elif other thing%}
                        <table>
                            <tr>
                                <td>
                                    do other thing
                                </td>
                            </tr>
                        </table>
                    {% elif other someting %}
                        <p>
                            dont do anything!
                        </p>
                    {% endif %}
                {% else %}
                    <span>
                        get something from user
                    </span>
                    <input type="text"/>
                {% endif %}
            {% else %}
                <p>
                    do something even nicer!
                </p>
            {% endif %}
        </div>
    </body>
  </html>


Jinja2 support might 
be missing some tags. If you find one please post an issue or pull request.


Usage -
=======
dangler path/to/file/with/unclosed/tags.html

This will print out html, with tags closed and beautified.


Have fun!
