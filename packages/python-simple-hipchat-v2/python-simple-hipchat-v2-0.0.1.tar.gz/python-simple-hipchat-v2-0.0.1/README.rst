Python HipChat-v2
=============================

Description
-----------
Stripped down version of python-simple-hipchat for v2 hipchat api.  Currently only supports sending a message to a room.


Dependencies
------------
None beyond the Python standard library.


Usage
-----

Install::

    pip install python-simple-hipchat-v2

Instantiate::

    import hipchat_v2
    hipster = hipchat_v2.HipChat(url='https://url.to.hipchat')

Example::

    # Post a message to a HipChat room
    hipster.message_room(
      room_id=1234, 
      message='all your base', 
      color='yellow', 
      token='abcdefg', 
      notify=True)

Changelog
---------

**v0.1.x**

- Added shortcut method for messaging a room
