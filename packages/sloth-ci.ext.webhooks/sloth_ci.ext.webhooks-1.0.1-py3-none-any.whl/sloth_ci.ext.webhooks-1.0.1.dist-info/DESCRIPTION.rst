Sloth CI extension that sends POST requests on build events in Sloth CI apps.

Extension params::

    # Use the module sloth-ci.ext.webhooks.
    module: webhooks

    # Log level (number or valid Python logging level name).
    # ERROR includes only build fails, WARNING adds partial completions,
    # INFO adds completion, and DEBUG adds trigger notifications.
    # Default is WARNING.
    level: INFO

    # URL to send the requests to.
    url: http://example.com


