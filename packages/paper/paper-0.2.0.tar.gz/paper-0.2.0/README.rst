Paper
=====

.. image:: https://travis-ci.org/ActivKonnect/paper.svg?branch=develop
    :target: https://travis-ci.org/ActivKonnect/paper

Keep generated fields in cache for your Django models.

Usage
~~~~~

You have two options: ``@paper`` will help you to create a calculated field that is stored in
Django's cache, and ``@cardboard`` will create a regular field in your model and update it in
database automatically.

@paper
------

Just like the ``@property`` decorator, you just need to use the ``@paper`` decorator, that will
transform a method of your class into a cached property.

.. code-block:: python

   class ModelA(models.Model):
       name = models.TextField()

       @paper(1, [
           ('testpaper.ModelB', lambda i: ModelA.objects.filter(children=i)),
       ])
       def count(self):
           return ModelA.objects\
               .filter(pk=self.pk)\
               .annotate(count=Coalesce(Sum('children__count'), 0))\
               .values_list('count', flat=True)[0]


   class ModelB(models.Model):
       parent = models.ForeignKey('ModelA', related_name='children')
       count = models.IntegerField()

``@paper`` takes 2 arguments:

- The method's version number, in case you want to change the format of what is returned. By
  example, imagine you're returning a complex denormalized data structure. If at some point you
  want to add some data in it, you can simply bump the version number and it will invalidate the
  caches automatically.
- A list of model/lister couples.
  - The model is either a model class, either an 'app.Model' string
  - The lister takes a single argument which is an instance of the updated model (here a ModelB
  objet) and returns a list of affected objects to invalidate (here a queryset of ModelA objects).

The value will be cached using Django's default cache. Please note that this requires the cache to
be shared across all your web worker instances, otherwise invalidation won't have any the intended
effect.

Invalidation is based on Django signals, so it requires ``save()`` or ``delete()`` to be called in
order to work correctly. Bulk/SQL operations won't be detected automatically.

@cardboard
----------

Use is very similar to ``@paper``, the main differences being the absence of versioning and the fact
that result is going to be stored in the model itself instead of caching it.

.. code-block:: python

   class ModelA(models.Model):
       name = models.TextField()

       @cardboard(models.IntegerField(default=0), [
           ('testpaper.ModelB', lambda i: ModelA.objects.filter(children=i)),
       ])
       def count(self):
           return ModelA.objects\
               .filter(pk=self.pk)\
               .annotate(count=Coalesce(Sum('children__count'), 0))\
               .values_list('count', flat=True)[0]


   class ModelB(models.Model):
       parent = models.ForeignKey('ModelA', related_name='children')
       count = models.IntegerField()

``@cardboard`` takes two arguments:

- The field that will be used to store results. You have to give it a sensible default value,
  because no calculation will be made upon object creation. Calculation are only triggered by the
  ``dependencies`` functions.
- A list of dependencies, just like in ``@paper``.

The same remark goes for this technique being ``save()``/``delete()`` driven: bulk or SQL operations
won't trigger recalculation.

Licence
~~~~~~~

This software is licenced by ActivKonnect under the terms of the WTFPL.
