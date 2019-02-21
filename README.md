# PhoenixPythonDB

[RESOURCES]

o| Google Cloud Documentation: https://cloud.google.com/appengine/docs/standard/python/

Several of the libraries in use are specific to Google, including the datastore. Also documented
here are the app configuration files: app.yaml, index.yaml and cron.yaml. Some important
subsections of this documentation:
	
	o| Installing the SDK: https://cloud.google.com/appengine/docs/standard/python/download
	o| Google Cloud Datastore: https://cloud.google.com/appengine/docs/standard/python/datastore/
	o| Datastore Property Reference: https://cloud.google.com/appengine/docs/standard/python/ndb/entity-property-reference

o| Jinja2 Documentation: http://jinja.pocoo.org

You will see many instances of {% <something> %} and {{ something }} in the HTML files associated 
to this project. These are Jinja expressions that get parsed by the Jinja template loader prior to 
render. Consult the documentation to understand what it's doing. In general, you can do a lot of 
cool stuff with it and save yourself the trouble of doing things like sorting and filtering in your 
application code. Let Jinja handle it.

o| Skeleton CSS: http://getskeleton.com

Dead simple CSS framework. The base version has been somewhat modified, but this will show you how
to use the basic features of Skeleton, especially the grid.

[DATABASE MODEL]

The entire database model lives in database.py. Consult the Google Cloud Datastore reference to
understand the syntax and property definitions. Notable properties:

	o| kill_list: This is a Pickle property. It's a serialized version of a Python list, so it
		looks like gibberish in the Entity viewer on the Cloud console. Basically, in the
		runtime environment it will be un-pickled into a standard Python list. This property is
		set up as a list of 30 numbers in reverse order representing a member's kill totals on each 
		of the last 30 days. To update it, set the property value to that of a Python list with 30
		integer values in it. The datatype doesn't enforce that exact format, but that's what the
		runtime code expects.