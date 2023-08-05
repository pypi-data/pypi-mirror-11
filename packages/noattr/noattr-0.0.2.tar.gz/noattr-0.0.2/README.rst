======
NoAttr
======

When you access an object with chained attributes ::

    info = obj.a.b.c.d or 'Unknown'
    
Usually, it will failed when one intermediate attribute return ‘None‘ ::
    
    if obj.a returns None
    obj.a.b.c.d will fail with that exception :
    AttributeError: 'NoneType' object has no attribute 'xxx'
    
To avoid that, instead of returning a ‘None‘ value, one should return ‘NoAttr‘, by this way, 
even next chained attribute will return ‘NoAttr‘ ::

    if obj.a returns NoAttr
    obj.a.b.c.d will not fail and will return NoAttr
    
‘NoAttr‘ can be seen as False, '', [], {} depending on the context, so ::

    if obj.a returns NoAttr
    obj.a.b.c.d or 'Unknown' will return 'Unknown'
    