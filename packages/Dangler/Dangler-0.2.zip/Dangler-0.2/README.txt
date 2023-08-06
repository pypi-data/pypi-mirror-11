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

This will not work, because the last line, 'more content' will 
get added to the content inside the span. Because indention of 
text node is taken from the start of the node. For this, to work
just leave a blank line. This causes the indentation to be
calculated for the following text node. Like this

::

   <html>
        <body>
            <div>
                Here is some content
                <span>
                    content inside span

                more content

Usage -
=======
dangler path/to/file/with/unclosed/tags.html

This will print out html, with tags closed and beautified.


Have fun!
