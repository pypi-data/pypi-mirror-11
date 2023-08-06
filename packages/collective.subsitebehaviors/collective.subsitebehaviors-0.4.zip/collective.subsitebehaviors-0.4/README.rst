====================
collective.subsitebehaviors
====================

Features:
---------

Appearance customization for Dexterity types:

- logo applicable to any INavigationRoot, scaled using 'logo' scale if found
- end-user-friendly TTW-customizable CSS styling applicable to any INavigationRoot

Credits:
--------

- viewlets originally copied from ftw.subsite
- inspiration from various subsite packages

How to use:
-----------

- apply behavior to your content types as you wish

To define further appearance customization besides the logo, add 'styling fields to your
Dexterity type:

- field ids must start with the prefix "css_"
- css selector is encoded into field id as tag[tagname]_id[id]_class[classname]
- the CSS style can then be normally entered as the field value in the add / edit form

Here, only the tag value is mandatory, id & class are optional.

- optional css attribute name is encoded likewise as _cssattr[AttrName] suffix

Here, because Dexterity field names cannot contain dash (ie. '-') characters, the
CamelCase notation is used (as in 'AttrName', above). So for example background-color
css attribute is specified 'BackgroundColor'.

If there is no css attribute name found in the field id, it is assumed the field value
contains a full regular 'attribute: value' css style statement, without the ending
semicolon.

An example:

All this may sound complex at first sight, but it's really not- to define a custom
background color for your content, just add a Dexterity field whose id is
'css_tagbody_cssattrBackgroundColor'.

