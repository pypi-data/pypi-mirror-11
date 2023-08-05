=====
Django Tribe Client
=====

Tribe client is a simple Django app to connect your server to the 'Tribe' web service
(located at http://tribe.greenelab.com).

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "tribe-client" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'tribe_client',
    )


2. Include the tribe-client URLconf in your project urls.py like this::

    url(r'^tribe_client/', include('tribe_client.urls')),


3. Register your client server at http://tribe-new.greenelab.com/oauth2/applications/. Make sure to:

   a. Select "Confidential" under "Client type" and
   b. Select "Authorization Code" under "Authorization grant type"
   c. Enter the client server address plus "tribe_client/get_token" in the "Redirect uris" box


4. Write down the Client id in the "TRIBE_ID" setting and the Client secret in the TRIBE_SECRET setting
   in the settings.py file


5. TRIBE_REDIRECT_URI setting should be the address of the client server plus "tribe_client/get_token"


6. Make sure that you have a base.html template that the tribe_client templates can extend


7. Make a link that takes the user to the '/tribe_client/' url of your website for them to log in using Tribe


