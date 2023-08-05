=====================
Vanilla Theme (Diazo)
=====================

*This installable Diazo Theme product delivers a general and mobile-ready implementation of a html5 template for Plone with activated Listing embedding tools. It is intended to deliver a library of standard features, which can be re-used in different customized variations.*

:Platform:  
    - Plone CMS > 4.3

:Features:
    - mobile-ready
    - configurable via Diazo Parameters
    - feature-library for custom implementations
    - Carousel support
    - Covers support and improvements
    - full support of propertyshelfs embedding features 

:Dependencies:
    - plone.app.theming (Diazo support)
    - *plone.mls.listing* *[1]*
    - *ps.plone.mls* *[1]*
    - *mls.apiclient* *[1]*
    - *collective.cover* *[1]*
    - *Products.Carousel* *[1]*
    [**1** *optional but needed for full features*]

:Setup Steps:
    *DEACTIVATE Plone default css files*
    - reset.css
    - public.css

:Parameter:
    *You can adjust the following Diazo parameters in Advanced settings of the "Theming" in Site Setup*

    *header_class:*
        - normal
        - light
        - dark
        - *Default:* header_class = string:normal

    *nr_phone_show:*
        - This phone number shows on header contact information
        - *Default:* nr_phone_show = string:+166 1418 7657

    *nr_phone:*
        - Is dialed by apps when click on header phone number
        - *Default:* nr_phone = string:16614187657

    *email:*
        - This email is use in the header contact imformation
        - *Default:* email = string:info@propertyshelf.com

    *slider_fullscreen:*
        - true
        - false
        - *Default:* slider_fullscreen = string:false
    

:Contact:
    *development@propertyshelf.com*

:Implementation:
  - Propertyshelf, Inc. [development@propertyshelf.com]
  - Kantanart Wanichkajornkul [kantanart@propertyshelf.com]
  - Jens Krause [jens@propertyshelf.com]
